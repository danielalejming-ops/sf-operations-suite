import xml.etree.ElementTree as ET
import re, os, shutil
from playwright.sync_api import sync_playwright

# 1. Parse the master SVG which has the TRUE Didone Bézier curves
tree = ET.parse(r'c:\Users\danie\Downloads\SF\web\img\propuestas_logo\propuesta_1_v2_master.svg')
root = tree.getroot()
paths = root.findall('.//{http://www.w3.org/2000/svg}path')

# Path 1 is S (Gold), Path 2 is F (Platinum)
d_s = paths[1].get('d')
d_f = paths[2].get('d')

# Path 3 is ENTRETENIMIENTO + divider
d_ent = paths[3].get('d')

# Parse coordinates to calculate exact bounding box
nums_s = [float(x) for x in re.findall(r'[-+]?\d*\.\d+|\d+', d_s)]
xs_s = nums_s[0::2]
ys_s = nums_s[1::2]

nums_f = [float(x) for x in re.findall(r'[-+]?\d*\.\d+|\d+', d_f)]
xs_f = nums_f[0::2]
ys_f = nums_f[1::2]

min_x = int(min(min(xs_s), min(xs_f))) - 25
max_x = int(max(max(xs_s), max(xs_f))) + 25
min_y = int(min(min(ys_s), min(ys_f))) - 25
max_y = int(max(max(ys_s), max(ys_f))) + 25

w_mono = max_x - min_x
h_mono = max_y - min_y

# --- FILE 1: SF_Monograma_Bordado_Uniformes.svg (Pure Bézier, Transparent Background, 2 embroidery layers) ---
svg_bordado_clean = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="{min_x} {min_y} {w_mono} {h_mono}" width="{w_mono}px" height="{h_mono}px">
  <defs>
    <!-- Gradiente de Hilo Oro 24k para Bordado -->
    <linearGradient id="hiloOro24k" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#FFF6DB"/>
      <stop offset="25%" stop-color="#E5C158"/>
      <stop offset="55%" stop-color="#B88A28"/>
      <stop offset="85%" stop-color="#8C6314"/>
      <stop offset="100%" stop-color="#F3D87E"/>
    </linearGradient>

    <!-- Gradiente de Hilo Platino para Bordado -->
    <linearGradient id="hiloPlatino" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#FFFFFF"/>
      <stop offset="30%" stop-color="#E5E7EB"/>
      <stop offset="60%" stop-color="#C7C9D1"/>
      <stop offset="85%" stop-color="#9C9CA7"/>
      <stop offset="100%" stop-color="#F3F4F6"/>
    </linearGradient>
  </defs>

  <!-- Curvas Bézier Didone Analíticas Puras (Sin fondo para bordadoras Wilcom / Tajima / Brother) -->
  <g id="SF_BORDADO_TEXTIL_DIDONE">
    <!-- CAPA HILO ORO: LETRA S -->
    <g id="Hilo_Oro_Letra_S">
      <path d="{d_s}" fill="url(#hiloOro24k)" stroke="#B88A28" stroke-width="0.8"/>
    </g>

    <!-- CAPA HILO PLATINO: LETRA F -->
    <g id="Hilo_Platino_Letra_F">
      <path d="{d_f}" fill="url(#hiloPlatino)" stroke="#A3A6B4" stroke-width="0.8"/>
    </g>
  </g>
</svg>'''

# --- FILE 2: SF_Monograma_Vinil_Unicolor.svg (Single-color Silhouette for Plotter) ---
svg_vinil_clean = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="{min_x} {min_y} {w_mono} {h_mono}" width="{w_mono}px" height="{h_mono}px">
  <g id="SF_CORTE_VINIL_TEXTIL">
    <path id="S_Oro" d="{d_s}" fill="#D4AF37"/>
    <path id="F_Plata" d="{d_f}" fill="#E5E7EB"/>
  </g>
</svg>'''

# --- FILE 3: SF_Logotipo_Completo_Bordado_y_Prensa.svg (Includes ENTRETENIMIENTO) ---
nums_ent = [float(x) for x in re.findall(r'[-+]?\d*\.\d+|\d+', d_ent)]
xs_ent = nums_ent[0::2]
ys_ent = nums_ent[1::2]
min_x_full = int(min(min_x, min(xs_ent))) - 30
max_x_full = int(max(max_x, max(xs_ent))) + 30
min_y_full = min_y
max_y_full = int(max(ys_ent)) + 30
w_full = max_x_full - min_x_full
h_full = max_y_full - min_y_full

svg_completo_clean = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="{min_x_full} {min_y_full} {w_full} {h_full}" width="{w_full}px" height="{h_full}px">
  <defs>
    <linearGradient id="goldFull" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#FFF6DB"/>
      <stop offset="25%" stop-color="#E5C158"/>
      <stop offset="55%" stop-color="#B88A28"/>
      <stop offset="85%" stop-color="#8C6314"/>
      <stop offset="100%" stop-color="#F3D87E"/>
    </linearGradient>
    <linearGradient id="platFull" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#FFFFFF"/>
      <stop offset="30%" stop-color="#E5E7EB"/>
      <stop offset="60%" stop-color="#C7C9D1"/>
      <stop offset="85%" stop-color="#9C9CA7"/>
      <stop offset="100%" stop-color="#F3F4F6"/>
    </linearGradient>
  </defs>
  <g id="SF_LOGOTIPO_COMPLETO_CURVAS_DIDONE">
    <path id="S_Oro" d="{d_s}" fill="url(#goldFull)"/>
    <path id="F_Platino" d="{d_f}" fill="url(#platFull)" stroke="#A3A6B4" stroke-width="0.8"/>
    <path id="Entretenimiento_Texto" d="{d_ent}" fill="url(#goldFull)"/>
  </g>
</svg>'''

# Save all files to 01_VECTORES_BORDADO_Y_CORTE
dest_dir = r"c:\Users\danie\Downloads\SF\ARCHIVOS_FINALES_CLIENTE\01_VECTORES_BORDADO_Y_CORTE"
dest_subir = r"c:\Users\danie\Downloads\SF\web_lista_para_subir\descargas_cliente"
dest_prop = r"c:\Users\danie\Downloads\SF\web\img\propuestas_logo"

f1 = os.path.join(dest_dir, "SF_Monograma_Bordado_Uniformes.svg")
f2 = os.path.join(dest_dir, "SF_Monograma_Vinil_Unicolor.svg")
f3 = os.path.join(dest_dir, "SF_Logotipo_Completo_Bordado_y_Prensa.svg")
f_prop = os.path.join(dest_prop, "propuesta_1_vector_uniformes_bordado.svg")

with open(f1, "w", encoding="utf-8") as f:
    f.write(svg_bordado_clean)
with open(f2, "w", encoding="utf-8") as f:
    f.write(svg_vinil_clean)
with open(f3, "w", encoding="utf-8") as f:
    f.write(svg_completo_clean)
with open(f_prop, "w", encoding="utf-8") as f:
    f.write(svg_bordado_clean)

# Sync to web_lista_para_subir
for f_path in [f1, f2, f3]:
    shutil.copy2(f_path, dest_subir)
shutil.copy2(f_prop, r"c:\Users\danie\Downloads\SF\web_lista_para_subir\img\propuestas_logo\propuesta_1_vector_uniformes_bordado.svg")

print("Saved clean Bézier SVGs!")

# 2. Render screenshot of the new embroidery SVG on dark background to inspect with read_file
preview_html = f'''<!DOCTYPE html>
<html>
<body style="margin:0; background:#0B080D; display:flex; align-items:center; justify-content:center; height:100vh;">
  <div style="width:700px; height:500px; display:flex; align-items:center; justify-content:center;">
    {svg_bordado_clean}
  </div>
</body>
</html>'''

preview_html_path = r"C:\Users\danie\.gemini\antigravity\brain\c68dc380-8aa2-4180-a684-fbf64042ffc2\test_preview_embroidery.html"
with open(preview_html_path, "w", encoding="utf-8") as f:
    f.write(preview_html)

chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
out_img = r"C:\Users\danie\.gemini\antigravity\brain\c68dc380-8aa2-4180-a684-fbf64042ffc2\verify_true_bezier_embroidery.png"

with sync_playwright() as p:
    browser = p.chromium.launch(executable_path=chrome_path, headless=True)
    page = browser.new_page(viewport={'width': 800, 'height': 600})
    page.goto('file:///' + preview_html_path.replace('\\', '/'))
    page.wait_for_timeout(400)
    page.screenshot(path=out_img)
    browser.close()
    print("Rendered verify_true_bezier_embroidery.png successfully!")
