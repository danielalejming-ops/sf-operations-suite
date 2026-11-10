# -*- coding: utf-8 -*-
import os, sys, math
import numpy as np
import cv2
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import matplotlib.patches as patches
import matplotlib.textpath as textpath
from matplotlib.path import Path
import pyembroidery

# Paths
base_dir = r'c:\Users\danie\Downloads\SF'
client_dir = os.path.join(base_dir, 'archivos_finales_cliente')
bordado_dir = os.path.join(client_dir, '00_bordado_uniformes')
os.makedirs(bordado_dir, exist_ok=True)

font_path = r'C:\Users\danie\.gemini\antigravity\brain\c68dc380-8aa2-4180-a684-fbf64042ffc2\BodoniModa.ttf'
fp = fm.FontProperties(fname=font_path, size=240)

# 1. GENERATE PURE BEZIER SVG
tp_s = textpath.TextPath((0, 0), 'S', prop=fp)
tp_f = textpath.TextPath((145, 0), 'F', prop=fp)

# Bounding box
pts_s = tp_s.vertices
pts_f = tp_f.vertices
min_x = min(pts_s[:, 0].min(), pts_f[:, 0].min())
max_x = max(pts_s[:, 0].max(), pts_f[:, 0].max())
min_y = min(pts_s[:, 1].min(), pts_f[:, 1].min())
max_y = max(pts_s[:, 1].max(), pts_f[:, 1].max())

width = max_x - min_x
height = max_y - min_y
pad = 25
vb_w = width + pad * 2
vb_h = height + pad * 2

def path_to_svg_d(tp, invert_y=True, y_offset=0):
    parts = []
    codes = tp.codes
    verts = tp.vertices
    i = 0
    while i < len(codes):
        code = codes[i]
        v = verts[i]
        y_val = (y_offset - v[1]) if invert_y else v[1]
        if code == Path.MOVETO:
            parts.append(f'M {v[0]:.2f} {y_val:.2f}')
            i += 1
        elif code == Path.LINETO:
            parts.append(f'L {v[0]:.2f} {y_val:.2f}')
            i += 1
        elif code == Path.CURVE3:
            v1 = verts[i]
            v2 = verts[i+1]
            y1 = (y_offset - v1[1]) if invert_y else v1[1]
            y2 = (y_offset - v2[1]) if invert_y else v2[1]
            parts.append(f'Q {v1[0]:.2f} {y1:.2f} {v2[0]:.2f} {y2:.2f}')
            i += 2
        elif code == Path.CURVE4:
            v1 = verts[i]
            v2 = verts[i+1]
            v3 = verts[i+2]
            y1 = (y_offset - v1[1]) if invert_y else v1[1]
            y2 = (y_offset - v2[1]) if invert_y else v2[1]
            y3 = (y_offset - v3[1]) if invert_y else v3[1]
            parts.append(f'C {v1[0]:.2f} {y1:.2f} {v2[0]:.2f} {y2:.2f} {v3[0]:.2f} {y3:.2f}')
            i += 3
        elif code == Path.CLOSEPOLY:
            parts.append('Z')
            i += 1
        else:
            i += 1
    return ' '.join(parts)

y_baseline = max_y + pad
d_s = path_to_svg_d(tp_s, invert_y=True, y_offset=y_baseline)
d_f = path_to_svg_d(tp_f, invert_y=True, y_offset=y_baseline)

svg_bordado = f'''<?xml version="1.0" encoding="UTF-8"?>
<!--
  SF ENTRETENIMIENTO, C.A. - ARCHIVO MAESTRO PARA BORDADO TEXTIL
  Formato: Vectores matematicos limpios (Curvas de Bezier puras Didone)
  Fondo: 100% Transparente (sin recuadros para no bordar parches)
  Capas: Separadas por color de hilo (Oro y Platino)
-->
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {vb_w:.2f} {vb_h:.2f}" width="100%" height="100%">
  <defs>
    <linearGradient id="hilo_oro_s" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#FFF0B3"/>
      <stop offset="30%" stop-color="#D4AF37"/>
      <stop offset="70%" stop-color="#AA8018"/>
      <stop offset="100%" stop-color="#7D5807"/>
    </linearGradient>
    <linearGradient id="hilo_platino_f" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#FFFFFF"/>
      <stop offset="30%" stop-color="#E2E8F0"/>
      <stop offset="70%" stop-color="#94A3B8"/>
      <stop offset="100%" stop-color="#64748B"/>
    </linearGradient>
  </defs>

  <!-- CAPA 1: LETRA S (HILO ORO IMPERIAL - MADEIRA 1070) -->
  <g id="capa_1_hilo_oro_s" data-thread-name="Madeira Classic Rayon 1070 Gold">
    <path d="{d_s}" 
          fill="url(#hilo_oro_s)" 
          stroke="#8C6314" 
          stroke-width="1.2" 
          stroke-linejoin="round"/>
  </g>

  <!-- CAPA 2: LETRA F (HILO PLATINO / TITANIO - MADEIRA 1001) -->
  <g id="capa_2_hilo_platino_f" data-thread-name="Madeira Classic Rayon 1001 Platinum">
    <path d="{d_f}" 
          fill="url(#hilo_platino_f)" 
          stroke="#475569" 
          stroke-width="1.2" 
          stroke-linejoin="round"/>
  </g>
</svg>
'''

svg_file = os.path.join(bordado_dir, 'sf_monograma_bordado_hilos_separados.svg')
with open(svg_file, 'w', encoding='utf-8') as f:
    f.write(svg_bordado)
print('Saved:', svg_file)

# Also update 01_vectores_bordado_y_corte
vect_dir = os.path.join(client_dir, '01_vectores_bordado_y_corte')
with open(os.path.join(vect_dir, 'sf_monograma_bordado_uniformes.svg'), 'w', encoding='utf-8') as f:
    f.write(svg_bordado)

# 2. GENERATE VECTOR PDF FOR EMBROIDERY DIGITIZERS
pdf_file = os.path.join(bordado_dir, 'sf_monograma_bordado_vector.pdf')
fig, ax = plt.subplots(figsize=(8, 6), dpi=300)
fig.patch.set_facecolor('none')
ax.set_facecolor('none')

patch_s = patches.PathPatch(tp_s, facecolor='#D4AF37', edgecolor='#9A7B20', linewidth=1.5, zorder=2)
patch_f = patches.PathPatch(tp_f, facecolor='#CBD5E1', edgecolor='#475569', linewidth=1.5, zorder=3)
ax.add_patch(patch_s)
ax.add_patch(patch_f)

ax.set_xlim(min_x - pad, max_x + pad)
ax.set_ylim(min_y - pad, max_y + pad)
ax.axis('off')
plt.savefig(pdf_file, transparent=True, bbox_inches='tight', pad_inches=0.05)
plt.close()
print('Saved:', pdf_file)

# 3. GENERATE TAJIMA (.DST) AND BROTHER (.PES) EMBROIDERY MACHINE STITCH FILES
def generate_stitches(target_width_mm):
    scale = (target_width_mm * 10.0) / width
    
    res_factor = 4
    mask_w = int(width * res_factor)
    mask_h = int(height * res_factor)
    
    mask_s = np.zeros((mask_h, mask_w), dtype=np.uint8)
    mask_f = np.zeros((mask_h, mask_w), dtype=np.uint8)
    
    for poly in tp_s.to_polygons():
        p_scaled = ((poly - [min_x, min_y]) * res_factor).astype(np.int32)
        cv2.fillPoly(mask_s, [p_scaled], 255)
        
    for poly in tp_f.to_polygons():
        p_scaled = ((poly - [min_x, min_y]) * res_factor).astype(np.int32)
        cv2.fillPoly(mask_f, [p_scaled], 255)
        
    pattern = pyembroidery.EmbPattern()
    
    # THREAD 1: GOLD FOR S
    pattern.add_thread(pyembroidery.EmbThread(0xD4, 0xAF, 0x37, 'Gold S', 'Madeira 1070'))
    
    step_y = max(1, int(0.35 * 10.0 / scale * res_factor))
    
    going_right = True
    for y in range(0, mask_h, step_y):
        row = mask_s[y, :]
        on_indices = np.where(row > 128)[0]
        if len(on_indices) > 0:
            diffs = np.diff(on_indices)
            splits = np.where(diffs > 2)[0] + 1
            segments = np.split(on_indices, splits)
            for seg in segments:
                x_start = seg[0]
                x_end = seg[-1]
                pt_x1 = (x_start / res_factor) * scale - (target_width_mm * 5.0)
                pt_x2 = (x_end / res_factor) * scale - (target_width_mm * 5.0)
                pt_y = (y / res_factor) * scale - ((height * scale) / 2.0)
                
                if going_right:
                    pattern.add_stitch_absolute(pyembroidery.STITCH, pt_x1, pt_y)
                    pattern.add_stitch_absolute(pyembroidery.STITCH, pt_x2, pt_y)
                else:
                    pattern.add_stitch_absolute(pyembroidery.STITCH, pt_x2, pt_y)
                    pattern.add_stitch_absolute(pyembroidery.STITCH, pt_x1, pt_y)
                going_right = not going_right
                
    # COLOR CHANGE FOR F
    pattern.add_command(pyembroidery.COLOR_CHANGE)
    pattern.add_thread(pyembroidery.EmbThread(0xCB, 0xD5, 0xE1, 'Platinum F', 'Madeira 1001'))
    
    for y in range(0, mask_h, step_y):
        row = mask_f[y, :]
        on_indices = np.where(row > 128)[0]
        if len(on_indices) > 0:
            diffs = np.diff(on_indices)
            splits = np.where(diffs > 2)[0] + 1
            segments = np.split(on_indices, splits)
            for seg in segments:
                x_start = seg[0]
                x_end = seg[-1]
                pt_x1 = (x_start / res_factor) * scale - (target_width_mm * 5.0)
                pt_x2 = (x_end / res_factor) * scale - (target_width_mm * 5.0)
                pt_y = (y / res_factor) * scale - ((height * scale) / 2.0)
                
                if going_right:
                    pattern.add_stitch_absolute(pyembroidery.STITCH, pt_x1, pt_y)
                    pattern.add_stitch_absolute(pyembroidery.STITCH, pt_x2, pt_y)
                else:
                    pattern.add_stitch_absolute(pyembroidery.STITCH, pt_x2, pt_y)
                    pattern.add_stitch_absolute(pyembroidery.STITCH, pt_x1, pt_y)
                going_right = not going_right
                
    pattern.add_command(pyembroidery.END)
    return pattern

# Pecho 7cm (70 mm)
pat_7cm = generate_stitches(70.0)
dst_7cm = os.path.join(bordado_dir, 'sf_monograma_pecho_7cm.dst')
pes_7cm = os.path.join(bordado_dir, 'sf_monograma_pecho_7cm.pes')
pyembroidery.write_dst(pat_7cm, dst_7cm)
pyembroidery.write_pes(pat_7cm, pes_7cm)
print(f'Saved 7cm Tajima ({len(pat_7cm.stitches)} stitches) & Brother files')

# Gorra 5.5cm (55 mm)
pat_55cm = generate_stitches(55.0)
dst_55cm = os.path.join(bordado_dir, 'sf_monograma_gorra_5.5cm.dst')
pes_55cm = os.path.join(bordado_dir, 'sf_monograma_gorra_5.5cm.pes')
pyembroidery.write_dst(pat_55cm, dst_55cm)
pyembroidery.write_pes(pat_55cm, pes_55cm)
print(f'Saved 5.5cm Tajima ({len(pat_55cm.stitches)} stitches) & Brother files')

print('All embroidery files created successfully!')
