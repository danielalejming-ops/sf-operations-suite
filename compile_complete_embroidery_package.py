# -*- coding: utf-8 -*-
import os, sys, shutil
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from shapely.geometry import Polygon, MultiPolygon
from shapely.ops import unary_union
import pyembroidery

base_dir = r'c:\Users\danie\Downloads\SF'
client_dir = os.path.join(base_dir, 'archivos_finales_cliente')
bordado_dir = os.path.join(client_dir, '00_bordado_uniformes')
vect_dir = os.path.join(client_dir, '01_vectores_bordado_y_corte')
web_descargas = os.path.join(base_dir, 'web_lista_para_subir', 'descargas_cliente')

os.makedirs(bordado_dir, exist_ok=True)
os.makedirs(vect_dir, exist_ok=True)
os.makedirs(web_descargas, exist_ok=True)

# 1. VECTOR PDF GENERATION
pdf_file = os.path.join(bordado_dir, 'sf_monograma_bordado_uniformes.pdf')
fig, ax = plt.subplots(figsize=(8, 6), dpi=300)
fig.patch.set_facecolor('none')
ax.set_facecolor('none')

# Re-read geometry from build_flawless_embroidery_vector
from build_flawless_embroidery_vector import s_unified, f_unified, s_bounds, f_bounds, total_minx, total_maxx, total_miny, total_maxy

for g in (f_unified.geoms if isinstance(f_unified, MultiPolygon) else [f_unified]):
    ext = np.array(g.exterior.coords)
    ax.fill(ext[:,0], ext[:,1], facecolor='#CBD5E1', edgecolor='#475569', linewidth=1.5, zorder=2)
    for hole in g.interiors:
        h_pts = np.array(hole.coords)
        ax.fill(h_pts[:,0], h_pts[:,1], facecolor='white', zorder=3)

for g in (s_unified.geoms if isinstance(s_unified, MultiPolygon) else [s_unified]):
    ext = np.array(g.exterior.coords)
    ax.fill(ext[:,0], ext[:,1], facecolor='#D4AF37', edgecolor='#8C6314', linewidth=1.5, zorder=4)
    for hole in g.interiors:
        h_pts = np.array(hole.coords)
        ax.fill(h_pts[:,0], h_pts[:,1], facecolor='white', zorder=5)

ax.set_xlim(total_minx, total_maxx)
ax.set_ylim(total_miny, total_maxy)
ax.axis('off')
plt.savefig(pdf_file, transparent=True, bbox_inches='tight', pad_inches=0.05)
plt.close()
print('Saved vector PDF:', pdf_file)

# Also PDF for logotipo completo
pdf_comp = os.path.join(bordado_dir, 'sf_logotipo_completo_bordado.pdf')
shutil.copy2(pdf_file, pdf_comp)

# 2. GENERATE TAJIMA (.DST) AND BROTHER (.PES) EMBROIDERY STITCH MATRICES
def build_stitches(target_width_mm):
    # Width of monogram
    w_pts = total_maxx - total_minx
    h_pts = total_maxy - total_miny
    scale = (target_width_mm * 10.0) / w_pts
    
    # Rasterize to dense grid
    res = 4
    mw = int(w_pts * res)
    mh = int(h_pts * res)
    
    import cv2
    ms = np.zeros((mh, mw), dtype=np.uint8)
    mf = np.zeros((mh, mw), dtype=np.uint8)
    
    # Draw S
    for g in (s_unified.geoms if isinstance(s_unified, MultiPolygon) else [s_unified]):
        pts = (((np.array(g.exterior.coords) - [total_minx, total_miny])) * res).astype(np.int32)
        cv2.fillPoly(ms, [pts], 255)
        for hole in g.interiors:
            h_pts = (((np.array(hole.coords) - [total_minx, total_miny])) * res).astype(np.int32)
            cv2.fillPoly(ms, [h_pts], 0)
            
    # Draw F
    for g in (f_unified.geoms if isinstance(f_unified, MultiPolygon) else [f_unified]):
        pts = (((np.array(g.exterior.coords) - [total_minx, total_miny])) * res).astype(np.int32)
        cv2.fillPoly(mf, [pts], 255)
        for hole in g.interiors:
            h_pts = (((np.array(hole.coords) - [total_minx, total_miny])) * res).astype(np.int32)
            cv2.fillPoly(mf, [h_pts], 0)
            
    pat = pyembroidery.EmbPattern()
    
    # Thread 1: Gold S
    pat.add_thread(pyembroidery.EmbThread(0xD4, 0xAF, 0x37, 'Gold S', 'Madeira 1070'))
    step_y = max(1, int(0.35 * 10.0 / scale * res))
    
    going_right = True
    for y in range(0, mh, step_y):
        row = ms[y, :]
        on_idx = np.where(row > 128)[0]
        if len(on_idx) > 0:
            diffs = np.diff(on_idx)
            splits = np.where(diffs > 2)[0] + 1
            for seg in np.split(on_idx, splits):
                p1_x = (seg[0] / res) * scale - (target_width_mm * 5.0)
                p2_x = (seg[-1] / res) * scale - (target_width_mm * 5.0)
                p_y = (y / res) * scale - ((h_pts * scale) / 2.0)
                if going_right:
                    pat.add_stitch_absolute(pyembroidery.STITCH, p1_x, p_y)
                    pat.add_stitch_absolute(pyembroidery.STITCH, p2_x, p_y)
                else:
                    pat.add_stitch_absolute(pyembroidery.STITCH, p2_x, p_y)
                    pat.add_stitch_absolute(pyembroidery.STITCH, p1_x, p_y)
                going_right = not going_right
                
    # Thread 2: Platinum F
    pat.add_command(pyembroidery.COLOR_CHANGE)
    pat.add_thread(pyembroidery.EmbThread(0xCB, 0xD5, 0xE1, 'Platinum F', 'Madeira 1001'))
    for y in range(0, mh, step_y):
        row = mf[y, :]
        on_idx = np.where(row > 128)[0]
        if len(on_idx) > 0:
            diffs = np.diff(on_idx)
            splits = np.where(diffs > 2)[0] + 1
            for seg in np.split(on_idx, splits):
                p1_x = (seg[0] / res) * scale - (target_width_mm * 5.0)
                p2_x = (seg[-1] / res) * scale - (target_width_mm * 5.0)
                p_y = (y / res) * scale - ((h_pts * scale) / 2.0)
                if going_right:
                    pat.add_stitch_absolute(pyembroidery.STITCH, p1_x, p_y)
                    pat.add_stitch_absolute(pyembroidery.STITCH, p2_x, p_y)
                else:
                    pat.add_stitch_absolute(pyembroidery.STITCH, p2_x, p_y)
                    pat.add_stitch_absolute(pyembroidery.STITCH, p1_x, p_y)
                going_right = not going_right
                
    pat.add_command(pyembroidery.END)
    return pat

# 70 mm Pecho
pat_7cm = build_stitches(70.0)
dst_7 = os.path.join(bordado_dir, 'sf_monograma_pecho_7cm.dst')
pes_7 = os.path.join(bordado_dir, 'sf_monograma_pecho_7cm.pes')
pyembroidery.write_dst(pat_7cm, dst_7)
pyembroidery.write_pes(pat_7cm, pes_7)

# 55 mm Gorra
pat_5cm = build_stitches(55.0)
dst_5 = os.path.join(bordado_dir, 'sf_monograma_gorra_5.5cm.dst')
pes_5 = os.path.join(bordado_dir, 'sf_monograma_gorra_5.5cm.pes')
pyembroidery.write_dst(pat_5cm, dst_5)
pyembroidery.write_pes(pat_5cm, pes_5)

print('Machine files compiled!')

# 3. SYNC ALL EMBROIDERY FILES TO 01_VECTORES AND WEB_LISTA_PARA_SUBIR
sync_targets = [vect_dir, web_descargas]
files_to_sync = [
    'sf_monograma_bordado_uniformes.svg',
    'sf_logotipo_completo_bordado.svg',
    'sf_monograma_bordado_uniformes.pdf',
    'sf_logotipo_completo_bordado.pdf',
    'sf_monograma_pecho_7cm.dst',
    'sf_monograma_pecho_7cm.pes',
    'sf_monograma_gorra_5.5cm.dst',
    'sf_monograma_gorra_5.5cm.pes',
    'vista_previa_uniforme_polo_negro.png',
    'ficha_tecnica_bordado_sf.png'
]

for target in sync_targets:
    for f in files_to_sync:
        src = os.path.join(bordado_dir, f)
        if os.path.exists(src):
            shutil.copy2(src, os.path.join(target, f))
            print(f'Synced {f} -> {target}')

print('Full compilation and synchronization finished successfully!')
