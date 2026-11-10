import os, shutil
from playwright.sync_api import sync_playwright

root_dir = r"c:\Users\danie\Downloads\SF\archivos_finales_cliente"

# 1. Clean out root_dir
for item in os.listdir(root_dir):
    p = os.path.join(root_dir, item)
    if os.path.isdir(p):
        shutil.rmtree(p, ignore_errors=True)
    else:
        try:
            os.remove(p)
        except Exception:
            pass

f_vec = os.path.join(root_dir, "01_vectores_bordado_y_corte")
f_png = os.path.join(root_dir, "02_estampado_dtf_png")
f_web = os.path.join(root_dir, "03_paquete_web")

os.makedirs(f_vec, exist_ok=True)
os.makedirs(f_png, exist_ok=True)
os.makedirs(f_web, exist_ok=True)

# 2. Generate pristine Bodoni Didone SVG paths
import matplotlib.font_manager as fm
from matplotlib.textpath import TextPath

font_path = r'C:\Users\danie\.gemini\antigravity\brain\c68dc380-8aa2-4180-a684-fbf64042ffc2\BodoniModa.ttf'
fp_bold = fm.FontProperties(fname=font_path, weight='bold')

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
        elif c == 3:
            p1 = verts[i]
            p2 = verts[i+1]
            d.append(f"Q {p1[0]+offset_x:.2f},{-p1[1]+offset_y:.2f} {p2[0]+offset_x:.2f},{-p2[1]+offset_y:.2f}")
            i += 2
        elif c == 4:
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

d_s = path_to_svg(tp_s, offset_x=65, offset_y=350)
d_f = path_to_svg(tp_f, offset_x=265, offset_y=350)

# Typography for ENTRETENIMIENTO
fp_sans = fm.FontProperties(family='sans-serif', weight='bold')
tp_ent = TextPath((0, 0), 'ENTRETENIMIENTO', size=34, prop=fp_sans)
d_ent = path_to_svg(tp_ent, offset_x=55, offset_y=455)

# --- SVG 1: sf_monograma_bordado_uniformes.svg (Transparent background, embroidery layers) ---
svg_bordado = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="40 70 480 320" width="100%" height="100%">
  <defs>
    <linearGradient id="hilo_oro" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#FFF6DB"/>
      <stop offset="30%" stop-color="#E5C158"/>
      <stop offset="60%" stop-color="#B88A28"/>
      <stop offset="100%" stop-color="#8C6314"/>
    </linearGradient>
    <linearGradient id="hilo_platino" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#FFFFFF"/>
      <stop offset="35%" stop-color="#E5E7EB"/>
      <stop offset="70%" stop-color="#C7C9D1"/>
      <stop offset="100%" stop-color="#9C9CA7"/>
    </linearGradient>
  </defs>
  <g id="sf_bordado_uniformes_didone">
    <path id="capa_hilo_oro_s" d="{d_s}" fill="url(#hilo_oro)" stroke="#B88A28" stroke-width="0.8"/>
    <path id="capa_hilo_platino_f" d="{d_f}" fill="url(#hilo_platino)" stroke="#A3A6B4" stroke-width="0.8"/>
  </g>
</svg>'''

# --- SVG 2: sf_monograma_vinil_unicolor.svg ---
svg_vinil = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="40 70 480 320" width="100%" height="100%">
  <g id="sf_corte_vinil">
    <path id="s_oro" d="{d_s}" fill="#D4AF37"/>
    <path id="f_plata" d="{d_f}" fill="#E5E7EB"/>
  </g>
</svg>'''

# --- SVG 3: sf_logotipo_completo_bordado.svg ---
svg_completo = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="30 70 500 410" width="100%" height="100%">
  <defs>
    <linearGradient id="hilo_oro_full" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#FFF6DB"/>
      <stop offset="30%" stop-color="#E5C158"/>
      <stop offset="60%" stop-color="#B88A28"/>
      <stop offset="100%" stop-color="#8C6314"/>
    </linearGradient>
    <linearGradient id="hilo_plat_full" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#FFFFFF"/>
      <stop offset="35%" stop-color="#E5E7EB"/>
      <stop offset="70%" stop-color="#C7C9D1"/>
      <stop offset="100%" stop-color="#9C9CA7"/>
    </linearGradient>
  </defs>
  <g id="sf_logotipo_completo">
    <path id="s_letra" d="{d_s}" fill="url(#hilo_oro_full)"/>
    <path id="f_letra" d="{d_f}" fill="url(#hilo_plat_full)" stroke="#A3A6B4" stroke-width="0.8"/>
    <line x1="45" y1="400" x2="515" y2="400" stroke="url(#hilo_oro_full)" stroke-width="2.2"/>
    <path id="texto_entretenimiento" d="{d_ent}" fill="url(#hilo_oro_full)"/>
  </g>
</svg>'''

# --- SVG 4: sf_logotipo_master_con_fondo.svg ---
svg_con_fondo = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 520" width="100%" height="100%">
  <defs>
    <radialGradient id="fondo_rubi_master" cx="50%" cy="38%" r="55%">
      <stop offset="0%" stop-color="#38050F"/>
      <stop offset="60%" stop-color="#140307"/>
      <stop offset="100%" stop-color="#040406"/>
    </radialGradient>
    <linearGradient id="marco_oro_master" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#FFF6DB"/>
      <stop offset="50%" stop-color="#E5C158"/>
      <stop offset="100%" stop-color="#8C6314"/>
    </linearGradient>
  </defs>
  <rect width="100%" height="100%" fill="url(#fondo_rubi_master)"/>
  <rect x="15" y="15" width="570" height="490" rx="14" fill="none" stroke="url(#marco_oro_master)" stroke-width="1.2" stroke-opacity="0.4"/>
  <g transform="translate(20, 20)">
    {svg_completo.split('<g id="sf_logotipo_completo">')[1].split('</svg>')[0]}
</svg>'''

# Save all SVGs in lowercase
with open(os.path.join(f_vec, "sf_monograma_bordado_uniformes.svg"), "w", encoding="utf-8") as f:
    f.write(svg_bordado)
with open(os.path.join(f_vec, "sf_monograma_vinil_unicolor.svg"), "w", encoding="utf-8") as f:
    f.write(svg_vinil)
with open(os.path.join(f_vec, "sf_logotipo_completo_bordado.svg"), "w", encoding="utf-8") as f:
    f.write(svg_completo)
with open(os.path.join(f_vec, "sf_logotipo_master_con_fondo.svg"), "w", encoding="utf-8") as f:
    f.write(svg_con_fondo)

# 3. Copy 4K PNGs to 02_estampado_dtf_png
png_master_s = r"c:\Users\danie\Downloads\SF\web\img\logo_layers\piece_s_p1.png"
png_master_f = r"c:\Users\danie\Downloads\SF\web\img\logo_layers\piece_f_p1.png"
png_master_ent = r"c:\Users\danie\Downloads\SF\web\img\logo_layers\piece_ent_p1.png"

from PIL import Image
s_im = Image.open(png_master_s).convert("RGBA")
f_im = Image.open(png_master_f).convert("RGBA")
ent_im = Image.open(png_master_ent).convert("RGBA")

# Monogram 4K
mono = Image.new("RGBA", s_im.size, (0, 0, 0, 0))
mono.alpha_composite(s_im)
mono.alpha_composite(f_im)
mono_crop = mono.crop(mono.getbbox())
mono_4k = mono_crop.resize((mono_crop.width * 3, mono_crop.height * 3), Image.Resampling.LANCZOS)
mono_4k.save(os.path.join(f_png, "sf_monograma_3d_estampado_dtf_4k.png"), quality=100)

# Full logo 4K (excluding reflection for textile print)
full = Image.new("RGBA", s_im.size, (0, 0, 0, 0))
full.alpha_composite(s_im)
full.alpha_composite(f_im)
import numpy as np
ent_arr = np.array(ent_im)
ent_arr[598:, :, 3] = 0
ent_clean = Image.fromarray(ent_arr)
full.alpha_composite(ent_clean)
full_crop = full.crop(full.getbbox())
full_4k = full_crop.resize((full_crop.width * 3, full_crop.height * 3), Image.Resampling.LANCZOS)
full_4k.save(os.path.join(f_png, "sf_logotipo_completo_3d_estampado_dtf_4k.png"), quality=100)

# 4. Copy web files to 03_paquete_web
shutil.copy2(r"c:\Users\danie\Downloads\SF\web\index.html", os.path.join(f_web, "index.html"))
shutil.copy2(r"c:\Users\danie\Downloads\SF\web\index_propuesta_a.html", os.path.join(f_web, "index_propuesta_a.html"))
shutil.copy2(r"c:\Users\danie\Downloads\SF\web\animaciones_logo.html", os.path.join(f_web, "animaciones_logo.html"))

# 5. Sync to web_lista_para_subir/descargas_cliente in lowercase
descargas_subir = r"c:\Users\danie\Downloads\SF\web_lista_para_subir\descargas_cliente"
os.makedirs(descargas_subir, exist_ok=True)
for fname in os.listdir(f_vec):
    shutil.copy2(os.path.join(f_vec, fname), os.path.join(descargas_subir, fname))
for fname in os.listdir(f_png):
    shutil.copy2(os.path.join(f_png, fname), os.path.join(descargas_subir, fname))

# Render preview of sf_monograma_bordado_uniformes.svg on black
preview_html = f'''<!DOCTYPE html>
<html>
<body style="margin:0; background:#0A070D; display:flex; align-items:center; justify-content:center; height:100vh;">
  <div style="width:650px; height:420px;">
    {svg_bordado}
  </div>
</body>
</html>'''

preview_path = r"C:\Users\danie\.gemini\antigravity\brain\c68dc380-8aa2-4180-a684-fbf64042ffc2\preview_verified_bordado.html"
with open(preview_path, "w", encoding="utf-8") as f:
    f.write(preview_html)

chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
out_img = r"C:\Users\danie\.gemini\antigravity\brain\c68dc380-8aa2-4180-a684-fbf64042ffc2\preview_verified_bordado.png"

with sync_playwright() as p:
    browser = p.chromium.launch(executable_path=chrome_path, headless=True)
    page = browser.new_page(viewport={'width': 750, 'height': 500})
    page.goto('file:///' + preview_path.replace('\\', '/'))
    page.screenshot(path=out_img)
    browser.close()

print("All tasks completed! All filenames are 100% lowercase!")
