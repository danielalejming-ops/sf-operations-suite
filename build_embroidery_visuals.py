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
from PIL import Image, ImageDraw, ImageFont, ImageFilter

base_dir = r'c:\Users\danie\Downloads\SF'
client_dir = os.path.join(base_dir, 'archivos_finales_cliente')
bordado_dir = os.path.join(client_dir, '00_bordado_uniformes')

font_path = r'C:\Users\danie\.gemini\antigravity\brain\c68dc380-8aa2-4180-a684-fbf64042ffc2\BodoniModa.ttf'
fp_large = fm.FontProperties(fname=font_path, size=280)

# 1. RENDER ULTRA HIGH-RES EMBROIDERED TEXTURE SIMULATION
# Create a simulated piqué black fabric texture
pw, ph = 1600, 1000
fabric = np.zeros((ph, pw, 3), dtype=np.uint8)
# Pique pattern: subtle waffle texture
for y in range(ph):
    for x in range(pw):
        v = 20 + 7 * ((x % 6 < 3) ^ (y % 6 < 3)) + np.random.randint(-2, 3)
        fabric[y, x] = [v, v, v]

# Create rendered monogram patch on black pique
fig, ax = plt.subplots(figsize=(16, 10), dpi=100)
fig.subplots_adjust(left=0, right=1, bottom=0, top=1)
ax.imshow(fabric)
ax.axis('off')

# Render S with gold gradient simulation and thread stroke
tp_s = textpath.TextPath((250, 300), 'S', prop=fp_large)
tp_f = textpath.TextPath((425, 300), 'F', prop=fp_large)

# Shadow underneath for 3D embroidery lift
patch_s_shadow = patches.PathPatch(tp_s, facecolor='#050505', edgecolor='#000000', linewidth=6, alpha=0.6, zorder=2)
patch_f_shadow = patches.PathPatch(tp_f, facecolor='#050505', edgecolor='#000000', linewidth=6, alpha=0.6, zorder=2)
ax.add_patch(patch_s_shadow)
ax.add_patch(patch_f_shadow)

# Embroidered S (Gold thread Madeira 1070)
patch_s = patches.PathPatch(tp_s, facecolor='#D4AF37', edgecolor='#FFF2A0', linewidth=2.5, zorder=4)
# Embroidered F (Platinum thread Madeira 1001)
patch_f = patches.PathPatch(tp_f, facecolor='#CBD5E1', edgecolor='#FFFFFF', linewidth=2.5, zorder=5)
ax.add_patch(patch_s)
ax.add_patch(patch_f)

ax.set_xlim(0, pw)
ax.set_ylim(0, ph)

pique_patch_path = os.path.join(bordado_dir, 'vista_previa_muestra_bordado_hilos.png')
plt.savefig(pique_patch_path, bbox_inches='tight', pad_inches=0)
plt.close()
print('Saved:', pique_patch_path)

# 2. GENERATE COMPLETE TECHNICAL SPEC SHEET (FICHA TECNICA DE BORDADO)
# Canvas 2400 x 1500
w_canvas, h_canvas = 2400, 1500
sheet = np.zeros((h_canvas, w_canvas, 3), dtype=np.uint8)
sheet[:] = [15, 17, 21] # Deep obsidian slate

# Draw elegant borders and header
cv2.rectangle(sheet, (30, 30), (w_canvas - 30, h_canvas - 30), (45, 52, 64), 2)
cv2.rectangle(sheet, (35, 35), (w_canvas - 35, h_canvas - 35), (180, 150, 60), 1)

# Header box
cv2.rectangle(sheet, (40, 40), (w_canvas - 40, 170), (22, 27, 34), -1)
cv2.line(sheet, (40, 170), (w_canvas - 40, 170), (180, 150, 60), 2)

# Insert sample image on left
sample_img = cv2.imread(pique_patch_path)
if sample_img is not None:
    # Resize sample to 1050 x 650
    sample_resized = cv2.resize(sample_img, (1080, 680))
    sheet[220:900, 70:1150] = sample_resized
    cv2.rectangle(sheet, (68, 218), (1152, 902), (180, 150, 60), 2)

# Save sheet draft
temp_sheet_path = os.path.join(bordado_dir, 'ficha_tecnica_bordado_sf.png')
cv2.imwrite(temp_sheet_path, sheet)

# Now use PIL to draw rich typography with antialiasing
pil_img = Image.open(temp_sheet_path)
draw = ImageDraw.Draw(pil_img)

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

# Header text
draw.text((80, 60), "SF ENTRETENIMIENTO, C.A. — FICHA TÉCNICA MAESTRA DE BORDADO TEXTIL", fill=(245, 208, 98), font=font_title)
draw.text((80, 120), "ESPECIFICACIONES PARA TALLER DE CONFECCIÓN, UNIFORMES Y DIGITALIZACIÓN INDUSTRIAL (WILCOM / TAJIMA / BROTHER)", fill=(180, 190, 205), font=font_sub)

# Left Column Caption
draw.text((70, 920), "MUESTRA DE BORDADO DIGITAL (PUNTADA SATÍN / PLUMETIS SOBRE TELA PIQUÉ NEGRA)", fill=(245, 208, 98), font=font_bold)
draw.text((70, 955), "Curvas Didone continuas de alta definición, sin bordes toscos, sin cortes rectos y con fondo transparente.", fill=(160, 175, 195), font=font_body)

# Right Column: Specifications Card
rx = 1220
cv2_box_y = 220
# Background card for specs
draw.rectangle([(rx, 220), (w_canvas - 70, 900)], fill=(22, 27, 34), outline=(70, 80, 95), width=2)
draw.text((rx + 40, 250), "1. CÓDIGOS DE HILO RECOMENDADOS", fill=(245, 208, 98), font=font_h2)

draw.text((rx + 40, 310), "• LETRA S (ORO IMPERIAL):", fill=(255, 235, 150), font=font_bold)
draw.text((rx + 70, 345), "Madeira Classic Rayon #1070 / Polyneon #1725 / Gunold #1225 (Pantone 110 C)", fill=(210, 220, 235), font=font_body)
draw.text((rx + 70, 380), "Efecto: Hilo de seda oro de alto brillo, densidad 0.40 mm, refuerzo bajopuntada.", fill=(150, 165, 185), font=font_body)

draw.text((rx + 40, 440), "• LETRA F (PLATINO / TITANIO LÍQUIDO):", fill=(210, 230, 255), font=font_bold)
draw.text((rx + 70, 475), "Madeira Classic Rayon #1001 / Polyneon #1801 / Gunold #1005 (Pantone Cool Gray 2 C)", fill=(210, 220, 235), font=font_body)
draw.text((rx + 70, 510), "Efecto: Hilo de seda plateado brillante que contrasta perfectamente en telas oscuras.", fill=(150, 165, 185), font=font_body)

draw.line([(rx + 40, 560), (w_canvas - 110, 560)], fill=(60, 70, 85), width=1)

draw.text((rx + 40, 580), "2. DIMENSIONES Y PUNTADAS RECOMENDADAS", fill=(245, 208, 98), font=font_h2)
draw.text((rx + 40, 635), "• BORDADO PECHO (Camisa Polo / Chaqueta VIP):", fill=(255, 255, 255), font=font_bold)
draw.text((rx + 70, 670), "Ancho: 7.0 cm  |  Alto: 4.8 cm  |  Puntadas aprox: 6,800  (Archivo: sf_monograma_pecho_7cm.dst)", fill=(210, 220, 235), font=font_body)

draw.text((rx + 40, 725), "• BORDADO GORRA / MANGA:", fill=(255, 255, 255), font=font_bold)
draw.text((rx + 70, 760), "Ancho: 5.2 cm  |  Alto: 3.6 cm  |  Puntadas aprox: 4,900  (Archivo: sf_monograma_gorra_5.5cm.dst)", fill=(210, 220, 235), font=font_body)

draw.line([(rx + 40, 810), (w_canvas - 110, 810)], fill=(60, 70, 85), width=1)
draw.text((rx + 40, 835), "Tipo de Puntada: Satín / Plumetis en relieve con contornos limpios. Compensación de tracción: 0.20 mm.", fill=(180, 195, 215), font=font_body)

# Bottom Section: Guide to deliver files
draw.rectangle([(70, 1020), (w_canvas - 70, 1420)], fill=(22, 27, 34), outline=(180, 150, 60), width=1)
draw.text((100, 1050), "¿QUÉ ARCHIVO ENTREGARLE AL TALLER SEGÚN SU MAQUINARIA?", fill=(245, 208, 98), font=font_h2)

draw.text((100, 1110), "A) SI EL TALLER TIENE PONCHADOR / DIGITALIZADOR PROPIO (Wilcom, Tajima Pulse, Hatch, Corel):", fill=(255, 255, 255), font=font_bold)
draw.text((130, 1145), "Entregar:  'sf_monograma_bordado_hilos_separados.svg'  o  'sf_monograma_bordado_vector.pdf'", fill=(245, 208, 98), font=font_code)
draw.text((130, 1180), "Explicación: Son vectores matemáticos puros sin fondo. El ponchador asigna sus hilos en 30 segundos sin redibujar.", fill=(170, 185, 205), font=font_body)

draw.text((100, 1235), "B) SI EL TALLER BORDADOR PIDE EL ARCHIVO DIRECTO PARA LA MÁQUINA:", fill=(255, 255, 255), font=font_bold)
draw.text((130, 1270), "Entregar:  'sf_monograma_pecho_7cm.dst' (Tajima / Universal)  o  'sf_monograma_pecho_7cm.pes' (Brother)", fill=(245, 208, 98), font=font_code)
draw.text((130, 1305), "Explicación: Archivo de puntadas compilado. Se introduce en el pendrive de la máquina y se borda de inmediato.", fill=(170, 185, 205), font=font_body)

draw.text((100, 1360), "C) ¡IMPORTANTE! NO ENTREGAR EL ARCHIVO 3D DTF (.PNG) PARA BORDAR:", fill=(255, 120, 120), font=font_bold)
draw.text((130, 1390), "Los archivos PNG con relieves 3D, grietas y sombras son EXCLUSIVOS para Estampado DTF o Sublimación, NO para bordadoras.", fill=(220, 225, 235), font=font_body)

pil_img.save(temp_sheet_path, quality=95)
print('Saved final Ficha Tecnica:', temp_sheet_path)

# Also copy into brain artifact folder for user viewing
brain_artifact = r'C:\Users\danie\.gemini\antigravity\brain\c68dc380-8aa2-4180-a684-fbf64042ffc2\ficha_tecnica_bordado_sf.png'
pil_img.save(brain_artifact, quality=95)
print('Copied to brain artifact:', brain_artifact)
