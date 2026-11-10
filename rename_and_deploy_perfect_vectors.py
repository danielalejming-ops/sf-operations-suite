import os, shutil, re
import matplotlib.font_manager as fm
from matplotlib.textpath import TextPath
from playwright.sync_api import sync_playwright

base_dir = r"c:\Users\danie\Downloads\SF"
client_dir = os.path.join(base_dir, "archivos_finales_cliente")

# Remove old uppercase directory if exists
old_client_dir = os.path.join(base_dir, "ARCHIVOS_FINALES_CLIENTE")
if os.path.exists(old_client_dir) and old_client_dir != client_dir:
    # On Windows, renaming case might require temporary name
    temp_dir = os.path.join(base_dir, "temp_client_archive_case")
    os.rename(old_client_dir, temp_dir)
    os.rename(temp_dir, client_dir)
else:
    os.makedirs(client_dir, exist_ok=True)

folder_vec = os.path.join(client_dir, "01_vectores_bordado_y_corte")
folder_png = os.path.join(client_dir, "02_estampado_dtf_alta_resolucion_png")
folder_web = os.path.join(client_dir, "03_paquete_web_y_animaciones")

os.makedirs(folder_vec, exist_ok=True)
os.makedirs(folder_png, exist_ok=True)
os.makedirs(folder_web, exist_ok=True)

# 1. Generate mathematically perfect Bodoni Didone curves
font_path = r'C:\Users\danie\.gemini\antigravity\brain\c68dc380-8aa2-4180-a684-fbf64042ffc2\BodoniModa.ttf'
fp_bold = fm.FontProperties(fname=font_path, weight='bold')

# Typography for S and F (proportioned to interlock gracefully)
size_val = 360
tp_s = TextPath((0, 0), 'S', size=size_val, prop=fp_bold)
tp_f = TextPath((0, 0), 'F', size=size_val, prop=fp_bold)

def path_to_svg(tp, offset_x=0, offset_y=0):
    codes = tp.codes
    verts = tp.vertices
    d = []
    i = 0
    while i < len(codes):
        c = codes[i]
        if c == 1:
            d.append(f"M {verts[i][0]+offset_x:.2f},{-verts[i][1]+offset_y:.2f}")
            i += 1
        elif c == 2:
            d.append(f"L {verts[i][0]+offset_x:.2f},{-verts[i][1]+offset_y:.2f}")
            i += 1
        elif c == 3: # Quadratic Bezier (1 control, 1 endpoint)
            p1 = verts[i]
            p2 = verts[i+1]
            d.append(f"Q {p1[0]+offset_x:.2f},{-p1[1]+offset_y:.2f} {p2[0]+offset_x:.2f},{-p2[1]+offset_y:.2f}")
            i += 2
        elif c == 4: # Cubic Bezier (2 controls, 1 endpoint)
            p1 = verts[i]
            p2 = verts[i+1]
            p3 = verts[i+2]
            d.append(f"C {p1[0]+offset_x:.2f},{-p1[1]+offset_y:.2f} {p2[0]+offset_x:.2f},{-p2[1]+offset_y:.2f} {p3[0]+offset_x:.2f},{-p3[1]+offset_y:.2f}")
            i += 3
        elif c == 79:
            d.append("Z")
            i += 1
        else:
            i += 1
    return " ".join(d)

# Positioning for elegant interlocking Didone monogram
d_s = path_to_svg(tp_s, offset_x=80, offset_y=360)
d_f = path_to_svg(tp_f, offset_x=280, offset_y=360)

# Typography for ENTRETENIMIENTO in Montserrat / Sans bold
fp_sans = fm.FontProperties(family='sans-serif', weight='bold')
tp_ent = TextPath((0, 0), 'ENTRETENIMIENTO', size=36, prop=fp_sans)
d_ent = path_to_svg(tp_ent, offset_x=70, offset_y=465)

# --- FILE 1: sf_monograma_bordado_uniformes.svg (Pure Bézier, Transparent Background, Embroidery Layers) ---
svg_bordado = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="50 70 500 340" width="100%" height="100%">
  <defs>
    <!-- Gradiente Hilo Oro 24k para Bordado -->
    <linearGradient id="hilo_oro_24k" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#FFF6DB"/>
      <stop offset="25%" stop-color="#E5C158"/>
      <stop offset="55%" stop-color="#B88A28"/>
      <stop offset="85%" stop-color="#8C6314"/>
      <stop offset="100%" stop-color="#F3D87E"/>
    </linearGradient>

    <!-- Gradiente Hilo Platino para Bordado -->
    <linearGradient id="hilo_platino" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#FFFFFF"/>
      <stop offset="30%" stop-color="#E5E7EB"/>
      <stop offset="60%" stop-color="#C7C9D1"/>
      <stop offset="85%" stop-color="#9C9CA7"/>
      <stop offset="100%" stop-color="#F3F4F6"/>
    </linearGradient>
  </defs>

  <g id="sf_bordado_uniformes_didone">
    <!-- Capa Hilo Oro: Letra S Didone con Curvatura Analítica Perfecta -->
    <g id="capa_hilo_oro_s">
      <path d="{d_s}" fill="url(#hilo_oro_24k)" stroke="#B88A28" stroke-width="0.8"/>
    </g>

    <!-- Capa Hilo Platino: Letra F Didone -->
    <g id="capa_hilo_platino_f">
      <path d="{d_f}" fill="url(#hilo_platino)" stroke="#A3A6B4" stroke-width="0.8"/>
    </g>
  </g>
</svg>'''

# --- FILE 2: sf_monograma_vinil_unicolor.svg (Plotter Cut Silhouette) ---
svg_vinil = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="50 70 500 340" width="100%" height="100%">
  <g id="sf_corte_vinil_textil">
    <path id="letra_s_oro" d="{d_s}" fill="#D4AF37"/>
    <path id="letra_f_plata" d="{d_f}" fill="#E5E7EB"/>
  </g>
</svg>'''

# --- FILE 3: sf_logotipo_completo_bordado.svg (Includes Divider & Text) ---
svg_completo = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="40 70 520 420" width="100%" height="100%">
  <defs>
    <linearGradient id="gold_full" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#FFF6DB"/>
      <stop offset="25%" stop-color="#E5C158"/>
      <stop offset="55%" stop-color="#B88A28"/>
      <stop offset="85%" stop-color="#8C6314"/>
      <stop offset="100%" stop-color="#F3D87E"/>
    </linearGradient>
    <linearGradient id="plat_full" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#FFFFFF"/>
      <stop offset="30%" stop-color="#E5E7EB"/>
      <stop offset="60%" stop-color="#C7C9D1"/>
      <stop offset="85%" stop-color="#9C9CA7"/>
      <stop offset="100%" stop-color="#F3F4F6"/>
    </linearGradient>
  </defs>
  <g id="sf_logotipo_completo_didone">
    <path id="letra_s" d="{d_s}" fill="url(#gold_full)"/>
    <path id="letra_f" d="{d_f}" fill="url(#plat_full)" stroke="#A3A6B4" stroke-width="0.8"/>
    <!-- Linea divisoria -->
    <line x1="60" y1="410" x2="540" y2="410" stroke="url(#gold_full)" stroke-width="2.5"/>
    <!-- Texto Entretenimiento -->
    <path id="texto_entretenimiento" d="{d_ent}" fill="url(#gold_full)"/>
  </g>
</svg>'''

# --- FILE 4: sf_logotipo_master_vector_con_fondo.svg (Includes Luxury Dark Background) ---
svg_con_fondo = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 620 540" width="100%" height="100%">
  <defs>
    <radialGradient id="fondo_rubi" cx="50%" cy="40%" r="55%">
      <stop offset="0%" stop-color="#38050F"/>
      <stop offset="60%" stop-color="#140307"/>
      <stop offset="100%" stop-color="#040406"/>
    </radialGradient>
    <linearGradient id="marco_oro" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#FFF6DB"/>
      <stop offset="50%" stop-color="#E5C158"/>
      <stop offset="100%" stop-color="#8C6314"/>
    </linearGradient>
  </defs>
  <rect width="100%" height="100%" fill="url(#fondo_rubi)"/>
  <rect x="15" y="15" width="590" height="510" rx="14" fill="none" stroke="url(#marco_oro)" stroke-width="1.2" stroke-opacity="0.4"/>
  <g transform="translate(10, 20)">
    {svg_completo.split('<g id="sf_logotipo_completo_didone">')[1].split('</svg>')[0]}
</svg>'''

# Write SVG files in lowercase
f_b1 = os.path.join(folder_vec, "sf_monograma_bordado_uniformes.svg")
f_b2 = os.path.join(folder_vec, "sf_monograma_vinil_unicolor.svg")
f_b3 = os.path.join(folder_vec, "sf_logotipo_completo_bordado.svg")
f_b4 = os.path.join(folder_vec, "sf_logotipo_master_vector_con_fondo.svg")

with open(f_b1, "w", encoding="utf-8") as f:
    f.write(svg_bordado)
with open(f_b2, "w", encoding="utf-8") as f:
    f.write(svg_vinil)
with open(f_b3, "w", encoding="utf-8") as f:
    f.write(svg_completo)
with open(f_b4, "w", encoding="utf-8") as f:
    f.write(svg_con_fondo)

# Copy 4K PNGs with lowercase names
png_src1 = r"c:\Users\danie\Downloads\SF\ARCHIVOS_FINALES_CLIENTE\02_ESTAMPADO_DTF_ALTA_RESOLUCION_PNG\SF_Monograma_3D_Estampado_DTF_4K.png"
png_src2 = r"c:\Users\danie\Downloads\SF\ARCHIVOS_FINALES_CLIENTE\02_ESTAMPADO_DTF_ALTA_RESOLUCION_PNG\SF_Logotipo_Completo_3D_Estampado_DTF_4K.png"

if os.path.exists(png_src1):
    shutil.copy2(png_src1, os.path.join(folder_png, "sf_monograma_3d_estampado_dtf_4k.png"))
if os.path.exists(png_src2):
    shutil.copy2(png_src2, os.path.join(folder_png, "sf_logotipo_completo_3d_estampado_dtf_4k.png"))

# Copy web files to 03_paquete_web_y_animaciones
shutil.copy2(r"c:\Users\danie\Downloads\SF\web\index.html", os.path.join(folder_web, "index.html"))
shutil.copy2(r"c:\Users\danie\Downloads\SF\web\index_propuesta_a.html", os.path.join(folder_web, "index_propuesta_a.html"))
shutil.copy2(r"c:\Users\danie\Downloads\SF\web\animaciones_logo.html", os.path.join(folder_web, "animaciones_logo.html"))

# Sync to web_lista_para_subir/descargas_cliente
subir_descargas = r"c:\Users\danie\Downloads\SF\web_lista_para_subir\descargas_cliente"
os.makedirs(subir_descargas, exist_ok=True)
for f_item in [f_b1, f_b2, f_b3, f_b4]:
    shutil.copy2(f_item, subir_descargas)

print("Generated clean lowercase package!")

# Render preview of sf_monograma_bordado_uniformes.svg on black background to verify
test_html = f'''<!DOCTYPE html>
<html>
<body style="margin:0; background:#0B080D; display:flex; align-items:center; justify-content:center; height:100vh;">
  <div style="width:700px; height:450px;">
    {svg_bordado}
  </div>
</body>
</html>'''

preview_html = r"C:\Users\danie\.gemini\antigravity\brain\c68dc380-8aa2-4180-a684-fbf64042ffc2\test_lowercase_bordado.html"
with open(preview_html, "w", encoding="utf-8") as f:
    f.write(test_html)

chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
out_img = r"C:\Users\danie\.gemini\antigravity\brain\c68dc380-8aa2-4180-a684-fbf64042ffc2\verify_perfect_didone_bordado.png"

with sync_playwright() as p:
    browser = p.chromium.launch(executable_path=chrome_path, headless=True)
    page = browser.new_page(viewport={'width': 800, 'height': 500})
    page.goto('file:///' + preview_html.replace('\\', '/'))
    page.wait_for_timeout(300)
    page.screenshot(path=out_img)
    browser.close()
    print("Rendered verify_perfect_didone_bordado.png!")
