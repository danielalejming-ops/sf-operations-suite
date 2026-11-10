# -*- coding: utf-8 -*-
import os, sys
import numpy as np
import cv2
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import matplotlib.patches as patches
import matplotlib.textpath as textpath
from matplotlib.path import Path
from shapely.geometry import Polygon, MultiPolygon
from shapely.ops import unary_union
import pyembroidery

base_dir = r'c:\Users\danie\Downloads\SF'
client_dir = os.path.join(base_dir, 'archivos_finales_cliente')
bordado_dir = os.path.join(client_dir, '00_bordado_uniformes')
vect_dir = os.path.join(client_dir, '01_vectores_bordado_y_corte')
os.makedirs(bordado_dir, exist_ok=True)
os.makedirs(vect_dir, exist_ok=True)

font_path = r'C:\Users\danie\.gemini\antigravity\brain\c68dc380-8aa2-4180-a684-fbf64042ffc2\BodoniModa.ttf'
fp_monogram = fm.FontProperties(fname=font_path, size=240, weight='bold')
fp_text = fm.FontProperties(fname='arialbd.ttf', size=36)

# 1. GENERATE CLEAN PATHS
tp_s = textpath.TextPath((60, 100), 'S', prop=fp_monogram)
tp_f = textpath.TextPath((215, 100), 'F', prop=fp_monogram)

# Convert tp_f to a unified shapely polygon to eliminate ANY internal seams or overlapping boxes
f_polys = []
for poly in tp_f.to_polygons():
    if len(poly) >= 3:
        p = Polygon(poly)
        if p.is_valid:
            f_polys.append(p)
f_unified = unary_union(f_polys)

# Same for S
s_polys = []
for poly in tp_s.to_polygons():
    if len(poly) >= 3:
        p = Polygon(poly)
        if p.is_valid:
            s_polys.append(p)
s_unified = unary_union(s_polys)

# Convert shapely polygon to SVG path string
def shapely_to_svg_d(geom, invert_y=True, y_max=350):
    if geom.is_empty:
        return ""
    paths = []
    if isinstance(geom, Polygon):
        geoms = [geom]
    elif isinstance(geom, MultiPolygon):
        geoms = list(geom.geoms)
    else:
        return ""

    for g in geoms:
        # Exterior
        ext = np.array(g.exterior.coords)
        if invert_y:
            ext[:, 1] = y_max - ext[:, 1]
        p_str = f"M {ext[0,0]:.2f},{ext[0,1]:.2f} " + " ".join([f"L {pt[0]:.2f},{pt[1]:.2f}" for pt in ext[1:]]) + " Z"
        paths.append(p_str)
        # Interiors (holes)
        for hole in g.interiors:
            h_pts = np.array(hole.coords)
            if invert_y:
                h_pts[:, 1] = y_max - h_pts[:, 1]
            h_str = f"M {h_pts[0,0]:.2f},{h_pts[0,1]:.2f} " + " ".join([f"L {pt[0]:.2f},{pt[1]:.2f}" for pt in h_pts[1:]]) + " Z"
            paths.append(h_str)

    return " ".join(paths)

# Calculate bounding boxes
s_bounds = s_unified.bounds # minx, miny, maxx, maxy
f_bounds = f_unified.bounds
total_minx = min(s_bounds[0], f_bounds[0]) - 30
total_maxx = max(s_bounds[2], f_bounds[2]) + 30
total_miny = min(s_bounds[1], f_bounds[1]) - 30
total_maxy = max(s_bounds[3], f_bounds[3]) + 30

# Height for SVG inversion
canvas_h = total_maxy + 20
d_s = shapely_to_svg_d(s_unified, invert_y=True, y_max=canvas_h)
d_f = shapely_to_svg_d(f_unified, invert_y=True, y_max=canvas_h)

# MONOGRAM SVG
view_w = int(total_maxx - total_minx)
view_h = int(canvas_h - total_miny) + 30

svg_monogram = f'''<?xml version="1.0" encoding="UTF-8"?>
<!-- SF ENTRETENIMIENTO - MONOGRAMA VECTORIAL MAESTRO PARA BORDADO TEXTIL -->
<svg xmlns="http://www.w3.org/2000/svg" viewBox="{total_minx:.1f} 20 {view_w:.1f} {view_h:.1f}" width="100%" height="100%">
  <defs>
    <!-- Hilo Oro Madeira 1070 -->
    <linearGradient id="hilo_oro" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#FFE89E"/>
      <stop offset="40%" stop-color="#D4AF37"/>
      <stop offset="80%" stop-color="#AA8018"/>
      <stop offset="100%" stop-color="#7A5606"/>
    </linearGradient>
    <!-- Hilo Platino Madeira 1001 (con alto contraste en fondo blanco y negro) -->
    <linearGradient id="hilo_platino" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#FFFFFF"/>
      <stop offset="35%" stop-color="#E2E8F0"/>
      <stop offset="70%" stop-color="#94A3B8"/>
      <stop offset="100%" stop-color="#64748B"/>
    </linearGradient>
  </defs>

  <!-- CAPA 2: LETRA F (PLATINO) UNIFICADA SIN LINEAS INTERNAS -->
  <g id="capa_hilo_platino_letra_f">
    <path d="{d_f}" 
          fill="url(#hilo_platino)" 
          stroke="#475569" 
          stroke-width="1.8" 
          stroke-linejoin="round"/>
  </g>

  <!-- CAPA 1: LETRA S (ORO) CURVATURA CONTINUA SUPERIOR -->
  <g id="capa_hilo_oro_letra_s">
    <path d="{d_s}" 
          fill="url(#hilo_oro)" 
          stroke="#8C6314" 
          stroke-width="1.8" 
          stroke-linejoin="round"/>
  </g>
</svg>
'''

monogram_svg_file = os.path.join(bordado_dir, 'sf_monograma_bordado_uniformes.svg')
with open(monogram_svg_file, 'w', encoding='utf-8') as f:
    f.write(svg_monogram)
# Also copy to 01_vectores
with open(os.path.join(vect_dir, 'sf_monograma_bordado_uniformes.svg'), 'w', encoding='utf-8') as f:
    f.write(svg_monogram)
print('Saved flawless monogram SVG:', monogram_svg_file)

# 2. LOGOTIPO COMPLETO: MONOGRAMA + DIVISOR + ENTRETENIMIENTO
# Let's generate the ENTRETENIMIENTO text with wide tracking, perfectly centered
text_cx = (s_bounds[0] + f_bounds[2]) / 2.0
text_y = canvas_h + 35

svg_completo = f'''<?xml version="1.0" encoding="UTF-8"?>
<!-- SF ENTRETENIMIENTO - LOGOTIPO COMPLETO VECTORIAL PARA BORDADO Y PRENSA -->
<svg xmlns="http://www.w3.org/2000/svg" viewBox="{total_minx:.1f} 20 {view_w:.1f} {view_h + 80:.1f}" width="100%" height="100%">
  <defs>
    <linearGradient id="hilo_oro" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#FFE89E"/>
      <stop offset="40%" stop-color="#D4AF37"/>
      <stop offset="80%" stop-color="#AA8018"/>
      <stop offset="100%" stop-color="#7A5606"/>
    </linearGradient>
    <linearGradient id="hilo_platino" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#FFFFFF"/>
      <stop offset="35%" stop-color="#E2E8F0"/>
      <stop offset="70%" stop-color="#94A3B8"/>
      <stop offset="100%" stop-color="#64748B"/>
    </linearGradient>
  </defs>

  <!-- F PLATINO -->
  <g id="capa_f_platino">
    <path d="{d_f}" 
          fill="url(#hilo_platino)" 
          stroke="#475569" 
          stroke-width="1.8" 
          stroke-linejoin="round"/>
  </g>

  <!-- S ORO -->
  <g id="capa_s_oro">
    <path d="{d_s}" 
          fill="url(#hilo_oro)" 
          stroke="#8C6314" 
          stroke-width="1.8" 
          stroke-linejoin="round"/>
  </g>

  <!-- LINEA DIVISORIA DORADA -->
  <line x1="{s_bounds[0]:.1f}" y1="{canvas_h + 10:.1f}" x2="{f_bounds[2]:.1f}" y2="{canvas_h + 10:.1f}" 
        stroke="url(#hilo_oro)" stroke-width="2.5" stroke-linecap="round"/>

  <!-- TEXTO ENTRETENIMIENTO CENTRADO CON KERNING VIP -->
  <text x="{text_cx:.1f}" y="{text_y + 25:.1f}" 
        text-anchor="middle" 
        fill="url(#hilo_oro)" 
        stroke="#8C6314" 
        stroke-width="0.8"
        font-family="'Montserrat', 'Arial', sans-serif" 
        font-size="28" 
        font-weight="800" 
        letter-spacing="9">ENTRETENIMIENTO</text>
</svg>
'''

completo_svg_file = os.path.join(bordado_dir, 'sf_logotipo_completo_bordado.svg')
with open(completo_svg_file, 'w', encoding='utf-8') as f:
    f.write(svg_completo)
with open(os.path.join(vect_dir, 'sf_logotipo_completo_bordado.svg'), 'w', encoding='utf-8') as f:
    f.write(svg_completo)
print('Saved flawless completo SVG:', completo_svg_file)

# 3. GENERATE HIGH RESOLUTION PREVIEW ON BLACK PIQUE POLO FABRIC
w_prev, h_prev = 1800, 1200
pique = np.zeros((h_prev, w_prev, 3), dtype=np.uint8)
# Realistic dark pique weave
for y in range(h_prev):
    for x in range(w_prev):
        v = 18 + 6 * ((x % 6 < 3) ^ (y % 6 < 3))
        pique[y, x] = [v, v, v]

# Save background
pique_bg_path = os.path.join(bordado_dir, 'polo_pique_bg.png')
cv2.imwrite(pique_bg_path, pique)

# Render complete logo with matplotlib on top of pique
fig, ax = plt.subplots(figsize=(18, 12), dpi=100)
fig.subplots_adjust(left=0, right=1, bottom=0, top=1)
ax.imshow(pique)
ax.axis('off')

# Plot patches with drop shadow
# F shadow & fill
for g in (f_unified.geoms if isinstance(f_unified, MultiPolygon) else [f_unified]):
    ext = np.array(g.exterior.coords)
    ax.fill(ext[:,0], ext[:,1], facecolor='#CBD5E1', edgecolor='#FFFFFF', linewidth=2.5, zorder=3)
    for hole in g.interiors:
        h_pts = np.array(hole.coords)
        ax.fill(h_pts[:,0], h_pts[:,1], facecolor='#121214', zorder=4)

# S shadow & fill
for g in (s_unified.geoms if isinstance(s_unified, MultiPolygon) else [s_unified]):
    ext = np.array(g.exterior.coords)
    ax.fill(ext[:,0], ext[:,1], facecolor='#D4AF37', edgecolor='#FFF0A0', linewidth=2.5, zorder=5)
    for hole in g.interiors:
        h_pts = np.array(hole.coords)
        ax.fill(h_pts[:,0], h_pts[:,1], facecolor='#121214', zorder=6)

# Divider line
ax.plot([s_bounds[0], f_bounds[2]], [total_miny - 15, total_miny - 15], color='#D4AF37', linewidth=4, zorder=7)

# Text ENTRETENIMIENTO
ax.text(text_cx, total_miny - 55, "ENTRETENIMIENTO", 
        color='#D4AF37', fontsize=26, fontweight='bold', 
        ha='center', va='top', fontname='sans-serif', zorder=7)

ax.set_xlim(total_minx - 80, total_maxx + 80)
ax.set_ylim(total_miny - 120, total_maxy + 60)

polo_preview_path = os.path.join(bordado_dir, 'vista_previa_uniforme_polo_negro.png')
plt.savefig(polo_preview_path, bbox_inches='tight', pad_inches=0.1)
plt.close()
print('Saved polo preview:', polo_preview_path)

# Also copy to brain artifact for inspection
brain_polo = r'C:\Users\danie\.gemini\antigravity\brain\c68dc380-8aa2-4180-a684-fbf64042ffc2\vista_previa_uniforme_polo_negro.png'
import shutil
shutil.copy2(polo_preview_path, brain_polo)

print('All flawless embroidery assets created!')
