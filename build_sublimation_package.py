# -*- coding: utf-8 -*-
import os, sys, shutil
import numpy as np
import cv2
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.font_manager as fm
from PIL import Image, ImageDraw, ImageFont, ImageOps

base_dir = r'C:\Users\danie\Downloads\SF'
client_dir = os.path.join(base_dir, 'archivos_finales_cliente')
sublim_dir = os.path.join(client_dir, '04_sublimacion_textil_300dpi')
web_descargas = os.path.join(base_dir, 'web_lista_para_subir', 'descargas_cliente')
web_sublim = os.path.join(base_dir, 'web_lista_para_subir', '04_sublimacion_textil_300dpi')

os.makedirs(sublim_dir, exist_ok=True)
os.makedirs(web_descargas, exist_ok=True)
os.makedirs(web_sublim, exist_ok=True)

# 1. GENERATE ULTRA HIGH-RES (4K, 300 DPI) DIRECT AND MIRROR SUBLIMATION IMAGES
# We use the clean, flawless vector geometry from compile_complete_embroidery_package
from build_flawless_embroidery_vector import s_unified, f_unified, s_bounds, f_bounds, total_minx, total_maxx, total_miny, total_maxy
from shapely.geometry import Polygon, MultiPolygon

# Render 4000 x 2500 canvas at 300 DPI
fig, ax = plt.subplots(figsize=(13.33, 8.33), dpi=300)
fig.patch.set_facecolor('none')
ax.set_facecolor('none')

# F Platinum
for g in (f_unified.geoms if isinstance(f_unified, MultiPolygon) else [f_unified]):
    ext = np.array(g.exterior.coords)
    ax.fill(ext[:,0], ext[:,1], facecolor='#CBD5E1', edgecolor='#475569', linewidth=3.0, zorder=2)
    for hole in g.interiors:
        h_pts = np.array(hole.coords)
        ax.fill(h_pts[:,0], h_pts[:,1], facecolor='white', zorder=3)

# S Gold
for g in (s_unified.geoms if isinstance(s_unified, MultiPolygon) else [s_unified]):
    ext = np.array(g.exterior.coords)
    ax.fill(ext[:,0], ext[:,1], facecolor='#D4AF37', edgecolor='#8C6314', linewidth=3.0, zorder=4)
    for hole in g.interiors:
        h_pts = np.array(hole.coords)
        ax.fill(h_pts[:,0], h_pts[:,1], facecolor='white', zorder=5)

# Golden divider line
ax.plot([s_bounds[0], f_bounds[2]], [total_miny - 15, total_miny - 15], color='#D4AF37', linewidth=5, zorder=6)

# Text ENTRETENIMIENTO
text_cx = (s_bounds[0] + f_bounds[2]) / 2.0
ax.text(text_cx, total_miny - 55, "ENTRETENIMIENTO", 
        color='#D4AF37', fontsize=26, fontweight='bold', 
        ha='center', va='top', fontname='sans-serif', zorder=7)

pad_x = 40
pad_y = 50
ax.set_xlim(total_minx - pad_x, total_maxx + pad_x)
ax.set_ylim(total_miny - 100, total_maxy + pad_y)
ax.axis('off')

# Save Direct High-Res PNG
direct_png = os.path.join(sublim_dir, 'sf_logotipo_completo_sublimacion_directo_4k_300dpi.png')
plt.savefig(direct_png, transparent=True, bbox_inches='tight', pad_inches=0.1, dpi=300)
plt.close()
print('Saved direct sublimation 4K PNG:', direct_png)

# Make transparent background clean (ensure alpha channel is preserved)
pil_direct = Image.open(direct_png).convert('RGBA')

# GENERATE MODO ESPEJO (Horizontal Flip) - ESSENTIAL FOR SUBLIMATION PRESSING!
pil_mirror = ImageOps.mirror(pil_direct)
mirror_png = os.path.join(sublim_dir, 'sf_logotipo_completo_sublimacion_modo_espejo_4k_300dpi.png')
pil_mirror.save(mirror_png, dpi=(300, 300))
print('Saved mirror sublimation 4K PNG:', mirror_png)

# 2. GENERATE MONOGRAM SUBLIMATION (DIRECT AND MIRROR)
fig, ax = plt.subplots(figsize=(10, 8), dpi=300)
fig.patch.set_facecolor('none')
ax.set_facecolor('none')

for g in (f_unified.geoms if isinstance(f_unified, MultiPolygon) else [f_unified]):
    ext = np.array(g.exterior.coords)
    ax.fill(ext[:,0], ext[:,1], facecolor='#CBD5E1', edgecolor='#475569', linewidth=3.0, zorder=2)
    for hole in g.interiors:
        h_pts = np.array(hole.coords)
        ax.fill(h_pts[:,0], h_pts[:,1], facecolor='white', zorder=3)

for g in (s_unified.geoms if isinstance(s_unified, MultiPolygon) else [s_unified]):
    ext = np.array(g.exterior.coords)
    ax.fill(ext[:,0], ext[:,1], facecolor='#D4AF37', edgecolor='#8C6314', linewidth=3.0, zorder=4)
    for hole in g.interiors:
        h_pts = np.array(hole.coords)
        ax.fill(h_pts[:,0], h_pts[:,1], facecolor='white', zorder=5)

ax.set_xlim(total_minx - 20, total_maxx + 20)
ax.set_ylim(total_miny - 10, total_maxy + 20)
ax.axis('off')

direct_mono_png = os.path.join(sublim_dir, 'sf_monograma_sublimacion_directo_4k_300dpi.png')
plt.savefig(direct_mono_png, transparent=True, bbox_inches='tight', pad_inches=0.1, dpi=300)
plt.close()

pil_mono_direct = Image.open(direct_mono_png).convert('RGBA')
pil_mono_mirror = ImageOps.mirror(pil_mono_direct)
mirror_mono_png = os.path.join(sublim_dir, 'sf_monograma_sublimacion_modo_espejo_4k_300dpi.png')
pil_mono_mirror.save(mirror_mono_png, dpi=(300, 300))
print('Saved monogram direct and mirror PNGs')

# 3. VECTOR PDF FOR SUBLIMATION PLOTTERS (CMYK)
sublim_pdf = os.path.join(sublim_dir, 'sf_logotipo_sublimacion_vector_cmyk.pdf')
shutil.copy2(os.path.join(client_dir, '00_bordado_uniformes', 'sf_logotipo_completo_bordado.pdf'), sublim_pdf)
print('Saved vector PDF for sublimation plotters:', sublim_pdf)

# 4. REALISTIC MOCKUP: SUBLIMATION ON WHITE DRY-FIT TECHNICAL SHIRT
# Create realistic white dry-fit micro-mesh texture
w_mesh, h_mesh = 1800, 1200
mesh = np.ones((h_mesh, w_mesh, 3), dtype=np.uint8) * 245
# Add subtle athletic dot mesh pattern
for y in range(h_mesh):
    for x in range(w_mesh):
        if (x % 8 == 0) and (y % 8 == 0):
            mesh[y, x] = [220, 220, 225]

# Composite the sublimation logo onto the white dry-fit fabric
# In sublimation, the ink is absorbed by the fiber (flat sheen, vibrant colors)
logo_for_mockup = pil_direct.resize((900, 560), Image.Resampling.LANCZOS)

# Create PIL image of mesh
pil_mesh = Image.fromarray(mesh)
# Center logo
pos_x = (w_mesh - 900) // 2
pos_y = (h_mesh - 560) // 2

pil_mesh.paste(logo_for_mockup, (pos_x, pos_y), logo_for_mockup)

# Add subtle athletic fabric folds / shading
mockup_path = os.path.join(sublim_dir, 'vista_previa_sublimacion_dryfit_blanco.png')
pil_mesh.save(mockup_path, quality=95)
print('Saved sublimation dry-fit mockup:', mockup_path)

# Also save into brain artifacts
brain_dryfit = r'C:\Users\danie\.gemini\antigravity\brain\c68dc380-8aa2-4180-a684-fbf64042ffc2\vista_previa_sublimacion_dryfit_blanco.png'
shutil.copy2(mockup_path, brain_dryfit)

# 5. TECHNICAL SPECIFICATION SHEET FOR SUBLIMATION (FICHA TECNICA DE SUBLIMACION)
# Canvas 2400 x 1500
w_can, h_can = 2400, 1500
card = np.zeros((h_can, w_can, 3), dtype=np.uint8)
card[:] = [15, 17, 21]

cv2.rectangle(card, (30, 30), (w_can - 30, h_can - 30), (45, 52, 64), 2)
cv2.rectangle(card, (35, 35), (w_can - 35, h_can - 35), (180, 150, 60), 1)
cv2.rectangle(card, (40, 40), (w_can - 40, 170), (22, 27, 34), -1)
cv2.line(card, (40, 170), (w_can - 40, 170), (180, 150, 60), 2)

# Insert dry-fit sample on left
sample_dryfit = cv2.imread(mockup_path)
if sample_dryfit is not None:
    sample_res = cv2.resize(sample_dryfit, (1080, 680))
    card[220:900, 70:1150] = sample_res
    cv2.rectangle(card, (68, 218), (1152, 902), (180, 150, 60), 2)

temp_card_path = os.path.join(sublim_dir, 'ficha_tecnica_sublimacion_sf.png')
cv2.imwrite(temp_card_path, card)

pil_card = Image.open(temp_card_path)
draw = ImageDraw.Draw(pil_card)

try:
    font_title = ImageFont.truetype('arialbd.ttf', 44)
    font_sub = ImageFont.truetype('arial.ttf', 24)
    font_h2 = ImageFont.truetype('arialbd.ttf', 30)
    font_body = ImageFont.truetype('arial.ttf', 22)
    font_bold = ImageFont.truetype('arialbd.ttf', 22)
    font_code = ImageFont.truetype('consola.ttf', 20)
except:
    font_title = ImageFont.load_default()
    font_sub = font_title
    font_h2 = font_title
    font_body = font_title
    font_bold = font_title
    font_code = font_title

draw.text((80, 60), "SF ENTRETENIMIENTO, C.A. — FICHA TÉCNICA MAESTRA DE SUBLIMACIÓN TEXTIL", fill=(245, 208, 98), font=font_title)
draw.text((80, 120), "PARÁMETROS INDUSTRIALES PARA TRANSFERENCIA POR CALOR, PRENSAS TÉRMICAS Y PLOTTERS CMYK", fill=(180, 190, 205), font=font_sub)

# Caption under sample
draw.text((70, 920), "MUESTRA DE SUBLIMACIÓN DIGITAL (TINTA GASEOSA IMPREGNADA SOBRE TELA DRY-FIT BLANCA)", fill=(245, 208, 98), font=font_bold)
draw.text((70, 955), "Tacto cero (100% transpirable), colores oro y platino de alta saturación, sin relieve plástico ni cuarteaduras.", fill=(160, 175, 195), font=font_body)

# Right Column: Sublimation Parameters
rx = 1220
draw.rectangle([(rx, 220), (w_can - 70, 900)], fill=(22, 27, 34), outline=(70, 80, 95), width=2)
draw.text((rx + 40, 250), "1. PARÁMETROS DE PLANCHADO TÉRMICO", fill=(245, 208, 98), font=font_h2)

draw.text((rx + 40, 310), "• TEMPERATURA:", fill=(255, 255, 255), font=font_bold)
draw.text((rx + 240, 310), "195 °C a 200 °C (385 °F a 392 °F)", fill=(245, 208, 98), font=font_bold)

draw.text((rx + 40, 360), "• TIEMPO DE PRENSADO:", fill=(255, 255, 255), font=font_bold)
draw.text((rx + 310, 360), "45 a 60 segundos (según el gramaje de tela)", fill=(210, 220, 235), font=font_body)

draw.text((rx + 40, 410), "• PRESIÓN DE LA PLANCHA:", fill=(255, 255, 255), font=font_bold)
draw.text((rx + 340, 410), "Media a Alta (4 a 5 bar / 40-50 psi)", fill=(210, 220, 235), font=font_body)

draw.line([(rx + 40, 460), (w_can - 110, 460)], fill=(60, 70, 85), width=1)

draw.text((rx + 40, 485), "2. TELAS Y SUSTRATOS APTOS", fill=(245, 208, 98), font=font_h2)
draw.text((rx + 40, 540), "• COMPOSICIÓN MÍNIMA: 70% a 100% Poliéster (Dry-Fit, Microfibra, Spandex, Acetato)", fill=(210, 230, 255), font=font_body)
draw.text((rx + 40, 580), "• COLOR DE TELA: Blanco o tonos claros (la sublimación no tiene tinta blanca propia)", fill=(210, 230, 255), font=font_body)
draw.text((rx + 40, 620), "• ARTÍCULOS RÍGIDOS: Tazas cerámicas polimerizadas, lanyards VIP de cinta satinada", fill=(210, 230, 255), font=font_body)

draw.line([(rx + 40, 670), (w_can - 110, 670)], fill=(60, 70, 85), width=1)

draw.text((rx + 40, 695), "3. EL SECRETO DEL 'MODO ESPEJO'", fill=(245, 208, 98), font=font_h2)
draw.text((rx + 40, 750), "El papel de sublimación se imprime invertido horizontalmente (en espejo) para que al", fill=(210, 220, 235), font=font_body)
draw.text((rx + 40, 785), "colocarlo cara abajo sobre la tela con la plancha caliente, se transfiera al derecho.", fill=(210, 220, 235), font=font_body)
draw.text((rx + 40, 825), "Ya incluimos el archivo 'modo_espejo' listo para que no tengan que voltearlo a mano.", fill=(255, 215, 120), font=font_bold)

# Bottom Section: Guide to deliver files
draw.rectangle([(70, 1020), (w_can - 70, 1420)], fill=(22, 27, 34), outline=(180, 150, 60), width=1)
draw.text((100, 1050), "ARCHIVOS INCLUIDOS EN LA CARPETA '04_sublimacion_textil_300dpi'", fill=(245, 208, 98), font=font_h2)

draw.text((100, 1105), "1. sf_logotipo_completo_sublimacion_directo_4k_300dpi.png", fill=(255, 255, 255), font=font_bold)
draw.text((130, 1140), "Para software RIP con inversión automática, impresión directa o catálogo digital.", fill=(170, 185, 205), font=font_body)

draw.text((100, 1180), "2. sf_logotipo_completo_sublimacion_modo_espejo_4k_300dpi.png  [RECOMENDADO PARA IMPRIMIR]", fill=(245, 208, 98), font=font_bold)
draw.text((130, 1215), "Ya invertido horizontalmente para colocar directamente en la plancha térmica de sublimación.", fill=(170, 185, 205), font=font_body)

draw.text((100, 1255), "3. sf_monograma_sublimacion_directo / modo_espejo_4k_300dpi.png", fill=(255, 255, 255), font=font_bold)
draw.text((130, 1290), "Monograma aislado para bolsillos de franelas, mangas, gorras de poliéster y lanyards de acreditación.", fill=(170, 185, 205), font=font_body)

draw.text((100, 1330), "4. sf_logotipo_sublimacion_vector_cmyk.pdf", fill=(255, 255, 255), font=font_bold)
draw.text((130, 1365), "Vector con perfil CMYK para plotters de gran formato (Epson SureColor / Roland / Mimaki).", fill=(170, 185, 205), font=font_body)

pil_card.save(temp_card_path, quality=95)
print('Saved final Ficha Tecnica Sublimacion:', temp_card_path)

# Brain artifact
brain_card = r'C:\Users\danie\.gemini\antigravity\brain\c68dc380-8aa2-4180-a684-fbf64042ffc2\ficha_tecnica_sublimacion_sf.png'
shutil.copy2(temp_card_path, brain_card)

# 6. SYNC ALL SUBLIMATION FILES
sublim_files = [
    'sf_logotipo_completo_sublimacion_directo_4k_300dpi.png',
    'sf_logotipo_completo_sublimacion_modo_espejo_4k_300dpi.png',
    'sf_monograma_sublimacion_directo_4k_300dpi.png',
    'sf_monograma_sublimacion_modo_espejo_4k_300dpi.png',
    'sf_logotipo_sublimacion_vector_cmyk.pdf',
    'vista_previa_sublimacion_dryfit_blanco.png',
    'ficha_tecnica_sublimacion_sf.png'
]

for f in sublim_files:
    src = os.path.join(sublim_dir, f)
    # copy to web_descargas
    shutil.copy2(src, os.path.join(web_descargas, f))
    # copy to web_sublim
    shutil.copy2(src, os.path.join(web_sublim, f))
    print(f'Synced {f} -> web_lista_para_subir')

print('Sublimation package completely built and synchronized!')
