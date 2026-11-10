# -*- coding: utf-8 -*-
import os, base64, subprocess

base_dir = r'C:\Users\danie\Downloads\SF'
web_root = os.path.join(base_dir, 'web_lista_para_subir')
client_root = os.path.join(base_dir, 'archivos_finales_cliente')

# Read polo image as base64
polo_img_path = os.path.join(web_root, 'descargas_cliente', 'vista_previa_uniforme_polo_negro.png')
with open(polo_img_path, 'rb') as f:
    b64_polo = base64.b64encode(f.read()).decode('utf-8')
data_uri_polo = f'data:image/png;base64,{b64_polo}'

# Read dryfit image as base64
dryfit_img_path = os.path.join(web_root, 'descargas_cliente', 'vista_previa_sublimacion_dryfit_blanco.png')
with open(dryfit_img_path, 'rb') as f:
    b64_dryfit = base64.b64encode(f.read()).decode('utf-8')
data_uri_dryfit = f'data:image/png;base64,{b64_dryfit}'

html_content = f'''<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>SF Entretenimiento — Guía Maestra de Archivos de Marca, Bordado y Sublimación</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Bodoni+Moda:wght@600;700;800&family=Montserrat:wght@400;500;600;700;800&display=swap" rel="stylesheet">
  <style>
    :root {{
      --bg: #0B0E14;
      --card-bg: #151921;
      --card-border: #242B38;
      --gold: #D4AF37;
      --gold-light: #F3E5AB;
      --platinum: #CBD5E1;
      --text-muted: #8E9BAE;
      --text: #F1F5F9;
      --accent-purple: #C084FC;
    }}
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{
      background: var(--bg);
      color: var(--text);
      font-family: 'Montserrat', sans-serif;
      line-height: 1.6;
      padding: 40px 20px;
    }}
    .container {{
      max-width: 1280px;
      margin: 0 auto;
    }}
    header {{
      text-align: center;
      margin-bottom: 35px;
      border-bottom: 1px solid var(--card-border);
      padding-bottom: 30px;
    }}
    .badge {{
      display: inline-block;
      padding: 6px 16px;
      background: rgba(212, 175, 55, 0.12);
      border: 1px solid var(--gold);
      border-radius: 20px;
      color: var(--gold);
      font-size: 12px;
      font-weight: 700;
      letter-spacing: 2px;
      text-transform: uppercase;
      margin-bottom: 15px;
    }}
    h1 {{
      font-family: 'Bodoni Moda', serif;
      font-size: 38px;
      color: #fff;
      font-weight: 700;
      letter-spacing: 1px;
      margin-bottom: 10px;
    }}
    p.lead {{
      color: var(--text-muted);
      font-size: 16px;
      max-width: 820px;
      margin: 0 auto;
    }}

    /* Differences Banner */
    .differences-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(360px, 1fr));
      gap: 20px;
      margin-bottom: 35px;
    }}
    .diff-box {{
      background: rgba(22, 27, 34, 0.9);
      border-radius: 12px;
      padding: 20px 24px;
      border-left: 4px solid var(--gold);
    }}
    .diff-box.sublim {{
      border-left-color: var(--accent-purple);
    }}
    .diff-box h4 {{
      font-size: 16px;
      margin-bottom: 6px;
      color: #fff;
      font-weight: 700;
    }}
    .diff-box p {{
      font-size: 13.5px;
      color: var(--text-muted);
      line-height: 1.5;
    }}

    /* Visual preview */
    .preview-grid {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 25px;
      margin-bottom: 40px;
    }}
    @media (max-width: 860px) {{
      .preview-grid {{ grid-template-columns: 1fr; }}
    }}
    .preview-card {{
      background: var(--card-bg);
      border: 1px solid var(--card-border);
      border-radius: 16px;
      padding: 24px;
      box-shadow: 0 10px 30px rgba(0,0,0,0.5);
    }}
    .preview-header {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 18px;
      padding-bottom: 12px;
      border-bottom: 1px solid var(--card-border);
    }}
    .preview-title {{
      font-size: 17px;
      font-weight: 700;
      color: var(--gold);
    }}
    .stage-img-wrap {{
      border-radius: 10px;
      overflow: hidden;
      border: 1px solid var(--card-border);
      text-align: center;
      background: #000;
      padding: 8px;
    }}
    .stage-img-wrap img {{
      width: 100%;
      max-height: 340px;
      object-fit: contain;
      display: block;
      margin: 0 auto;
      border-radius: 6px;
    }}

    /* Grid of 4 file categories */
    .grid-4 {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(290px, 1fr));
      gap: 20px;
      margin-bottom: 40px;
    }}
    .card {{
      background: var(--card-bg);
      border: 1px solid var(--card-border);
      border-radius: 14px;
      padding: 22px;
      display: flex;
      flex-direction: column;
    }}
    .card-badge {{
      display: inline-block;
      align-self: flex-start;
      font-size: 11px;
      font-weight: 700;
      padding: 4px 10px;
      border-radius: 6px;
      margin-bottom: 12px;
      text-transform: uppercase;
      letter-spacing: 1px;
    }}
    .card-badge.gold {{ background: rgba(212, 175, 55, 0.15); color: var(--gold); border: 1px solid rgba(212, 175, 55, 0.4); }}
    .card-badge.blue {{ background: rgba(56, 189, 248, 0.15); color: #38BDF8; border: 1px solid rgba(56, 189, 248, 0.4); }}
    .card-badge.purple {{ background: rgba(192, 132, 252, 0.15); color: var(--accent-purple); border: 1px solid rgba(192, 132, 252, 0.4); }}
    .card-badge.green {{ background: rgba(74, 222, 128, 0.15); color: #4ADE80; border: 1px solid rgba(74, 222, 128, 0.4); }}

    .card h2 {{
      font-size: 18px;
      font-weight: 700;
      color: #fff;
      margin-bottom: 8px;
    }}
    .card p.desc {{
      color: var(--text-muted);
      font-size: 13px;
      margin-bottom: 16px;
      flex-grow: 1;
    }}
    .file-list {{
      list-style: none;
      border-top: 1px solid var(--card-border);
      padding-top: 12px;
    }}
    .file-item {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 10px 0;
      border-bottom: 1px solid rgba(255,255,255,0.05);
      font-size: 12.5px;
    }}
    .file-name {{
      color: #E2E8F0;
      font-weight: 600;
      font-family: monospace;
      word-break: break-all;
    }}
    .file-link {{
      color: var(--gold);
      text-decoration: none;
      font-size: 11.5px;
      font-weight: 600;
      padding: 4px 10px;
      border: 1px solid var(--gold);
      border-radius: 6px;
      transition: all 0.2s;
      white-space: nowrap;
      margin-left: 8px;
    }}
    .file-link:hover {{
      background: var(--gold);
      color: #000;
    }}
    .file-link.purple {{
      color: var(--accent-purple);
      border-color: var(--accent-purple);
    }}
    .file-link.purple:hover {{
      background: var(--accent-purple);
      color: #000;
    }}

    footer {{
      text-align: center;
      color: var(--text-muted);
      font-size: 13px;
      margin-top: 50px;
      padding-top: 20px;
      border-top: 1px solid var(--card-border);
    }}
  </style>
</head>
<body>

  <div class="container">
    <header>
      <div class="badge">SF Entretenimiento — Producción y Marca</div>
      <h1>Directorio Maestro de Archivos: Web, Bordado y Sublimación</h1>
      <p class="lead">Paquete definitivo actualizado con la versión oficial solicitada por Said: bordado sin costuras internas, animación suave de Propuesta A en la web y formatos de sublimación 300 DPI con modo espejo.</p>
    </header>

    <!-- CLARIFICATION BOXES -->
    <div class="differences-grid">
      <div class="diff-box">
        <h4>🧵 Bordado vs. 🖨️ Estampado DTF</h4>
        <p><strong>Bordado:</strong> Usa hilos reales cosidos. Requiere vectores matemáticos limpios (.SVG/.PDF) o matrices de puntada (.DST/.PES). <em>NO admite PNGs 3D con sombras.</em><br>
        <strong>DTF:</strong> Imprime tinta con cama blanca sobre cualquier tela (incluyendo algodón negro). Se imprime al derecho.</p>
      </div>
      <div class="diff-box sublim">
        <h4>🔥 Sublimación Textil (Para Said)</h4>
        <p><strong>Sublimación:</strong> Proceso de gas térmico a 200°C que tiñe directamente las fibras de poliéster / dry-fit (tacto cero, 100% transpirable).<br>
        <strong>El secreto del Modo Espejo:</strong> Se imprime invertido horizontalmente para que al plancharse boca abajo quede al derecho. Ya incluimos ambos archivos listos.</p>
      </div>
    </div>

    <!-- 2 VISUAL PREVIEWS: BORDADO EN POLO Y SUBLIMACION EN DRY-FIT -->
    <div class="preview-grid">
      <div class="preview-card">
        <div class="preview-header">
          <div class="preview-title">Bordado Textil (Polo Negra)</div>
          <a href="descargas_cliente/sf_monograma_bordado_uniformes.svg" class="file-link" target="_blank">Ver Vector</a>
        </div>
        <div class="stage-img-wrap">
          <img src="{data_uri_polo}" alt="Muestra Bordado Polo Negra">
        </div>
        <div style="font-size: 12px; color: var(--text-muted); margin-top: 10px; text-align: center;">
          Hilo Oro + Hilo Platino sin costuras internas transparentes
        </div>
      </div>

      <div class="preview-card">
        <div class="preview-header">
          <div class="preview-title" style="color: var(--accent-purple);">Sublimación Textil (Dry-Fit Blanco)</div>
          <a href="descargas_cliente/sf_logotipo_sublimacion_vector_cmyk.pdf" class="file-link purple" target="_blank">Ver PDF CMYK</a>
        </div>
        <div class="stage-img-wrap" style="background: #EAECEF;">
          <img src="{data_uri_dryfit}" alt="Muestra Sublimacion Dry-Fit Blanco">
        </div>
        <div style="font-size: 12px; color: var(--text-muted); margin-top: 10px; text-align: center;">
          Tinta gaseosa fijada a 200°C, transpirable, ideal para uniformes deportivos y eventos
        </div>
      </div>
    </div>

    <!-- 4 DIRECTORY CARDS -->
    <div class="grid-4">

      <!-- CARD 1: BORDADO -->
      <div class="card" style="border-top: 3px solid var(--gold);">
        <div class="card-badge gold">00_bordado_uniformes</div>
        <h2>1. Bordado</h2>
        <p class="desc">Para camisas polo, chaquetas de staff y gorras. Vectores limpios y matrices directas para la máquina.</p>
        
        <ul class="file-list">
          <li class="file-item">
            <div>
              <div class="file-name">sf_monograma_bordado_uniformes.svg</div>
              <div style="font-size: 10.5px; color: var(--text-muted);">Vector puro para Wilcom / Tajima</div>
            </div>
            <a href="descargas_cliente/sf_monograma_bordado_uniformes.svg" class="file-link" target="_blank">Abrir</a>
          </li>
          <li class="file-item">
            <div>
              <div class="file-name">sf_logotipo_completo_bordado.svg</div>
              <div style="font-size: 10.5px; color: var(--text-muted);">Monograma + Entretenimiento centrado</div>
            </div>
            <a href="descargas_cliente/sf_logotipo_completo_bordado.svg" class="file-link" target="_blank">Abrir</a>
          </li>
          <li class="file-item">
            <div>
              <div class="file-name">sf_monograma_pecho_7cm.dst</div>
              <div style="font-size: 10.5px; color: var(--text-muted);">Matriz Tajima (7 cm pecho)</div>
            </div>
            <a href="descargas_cliente/sf_monograma_pecho_7cm.dst" class="file-link" download>Descargar</a>
          </li>
          <li class="file-item">
            <div>
              <div class="file-name">sf_monograma_pecho_7cm.pes</div>
              <div style="font-size: 10.5px; color: var(--text-muted);">Matriz Brother (7 cm pecho)</div>
            </div>
            <a href="descargas_cliente/sf_monograma_pecho_7cm.pes" class="file-link" download>Descargar</a>
          </li>
          <li class="file-item">
            <div>
              <div class="file-name">ficha_tecnica_bordado_sf.png</div>
              <div style="font-size: 10.5px; color: var(--text-muted);">Códigos de hilo Madeira y medidas</div>
            </div>
            <a href="descargas_cliente/ficha_tecnica_bordado_sf.png" class="file-link" target="_blank">Ver Ficha</a>
          </li>
        </ul>
      </div>

      <!-- CARD 2: ESTAMPADO DTF -->
      <div class="card" style="border-top: 3px solid #38BDF8;">
        <div class="card-badge blue">02_estampado_dtf_png</div>
        <h2>2. Estampado DTF</h2>
        <p class="desc">Para franelas de algodón o poliéster estampadas por calor con volúmenes 3D y reflejos dorados.</p>
        
        <ul class="file-list">
          <li class="file-item">
            <div>
              <div class="file-name">sf_logotipo_completo_3d_estampado_dtf_4k.png</div>
              <div style="font-size: 10.5px; color: var(--text-muted);">Logotipo completo 3D 4K (300 DPI)</div>
            </div>
            <a href="descargas_cliente/sf_logotipo_completo_3d_estampado_dtf_4k.png" class="file-link" target="_blank">Abrir</a>
          </li>
          <li class="file-item">
            <div>
              <div class="file-name">sf_monograma_3d_estampado_dtf_4k.png</div>
              <div style="font-size: 10.5px; color: var(--text-muted);">Monograma SF 3D 4K (300 DPI)</div>
            </div>
            <a href="descargas_cliente/sf_monograma_3d_estampado_dtf_4k.png" class="file-link" target="_blank">Abrir</a>
          </li>
        </ul>
      </div>

      <!-- CARD 3: SUBLIMACION (NUEVO) -->
      <div class="card" style="border-top: 3px solid var(--accent-purple);">
        <div class="card-badge purple">04_sublimacion_textil</div>
        <h2>3. Sublimación Textil</h2>
        <p class="desc">Solicitado por Said: para franelas Dry-Fit, lanyards VIP y tazas. Incluye versión directo y modo espejo.</p>
        
        <ul class="file-list">
          <li class="file-item">
            <div>
              <div class="file-name">sf_logotipo_sublimacion_modo_espejo_4k_300dpi.png</div>
              <div style="font-size: 10.5px; color: var(--accent-purple);">Listo para imprimir y planchar a 200°C</div>
            </div>
            <a href="descargas_cliente/sf_logotipo_completo_sublimacion_modo_espejo_4k_300dpi.png" class="file-link purple" target="_blank">Abrir</a>
          </li>
          <li class="file-item">
            <div>
              <div class="file-name">sf_logotipo_sublimacion_directo_4k_300dpi.png</div>
              <div style="font-size: 10.5px; color: var(--text-muted);">Vista al derecho 4K a 300 DPI</div>
            </div>
            <a href="descargas_cliente/sf_logotipo_completo_sublimacion_directo_4k_300dpi.png" class="file-link purple" target="_blank">Abrir</a>
          </li>
          <li class="file-item">
            <div>
              <div class="file-name">sf_monograma_sublimacion_modo_espejo_4k_300dpi.png</div>
              <div style="font-size: 10.5px; color: var(--text-muted);">Monograma en espejo para gorras/lanyards</div>
            </div>
            <a href="descargas_cliente/sf_monograma_sublimacion_modo_espejo_4k_300dpi.png" class="file-link purple" target="_blank">Abrir</a>
          </li>
          <li class="file-item">
            <div>
              <div class="file-name">sf_logotipo_sublimacion_vector_cmyk.pdf</div>
              <div style="font-size: 10.5px; color: var(--text-muted);">Vector CMYK para plotters Epson / Roland</div>
            </div>
            <a href="descargas_cliente/sf_logotipo_sublimacion_vector_cmyk.pdf" class="file-link purple" target="_blank">Abrir</a>
          </li>
          <li class="file-item">
            <div>
              <div class="file-name">ficha_tecnica_sublimacion_sf.png</div>
              <div style="font-size: 10.5px; color: var(--text-muted);">Ficha con tiempos, presión y telas</div>
            </div>
            <a href="descargas_cliente/ficha_tecnica_sublimacion_sf.png" class="file-link purple" target="_blank">Ver Ficha</a>
          </li>
        </ul>
      </div>

      <!-- CARD 4: PAGINA WEB -->
      <div class="card" style="border-top: 3px solid #4ADE80;">
        <div class="card-badge green">web</div>
        <h2>4. Página Web Actualizada</h2>
        <p class="desc">Actualizada con la animación suave de Propuesta A (descenso escultórico, rebote elástico y sin temblor brusco).</p>
        
        <ul class="file-list">
          <li class="file-item">
            <div>
              <div class="file-name">index.html</div>
              <div style="font-size: 10.5px; color: #4ADE80;">Sitio oficial con la caída suave ganadora</div>
            </div>
            <a href="index.html" class="file-link" target="_blank">Abrir Web</a>
          </li>
          <li class="file-item">
            <div>
              <div class="file-name">animaciones_logo.html</div>
              <div style="font-size: 10.5px; color: var(--text-muted);">Laboratorio interactivo de propuestas</div>
            </div>
            <a href="animaciones_logo.html" class="file-link" target="_blank">Abrir</a>
          </li>
        </ul>
      </div>

    </div>

    <footer>
      SF ENTRETENIMIENTO, C.A. — Paquete Oficial de Confección Textil, Sublimación y Web. Todos los archivos en minúsculas.
    </footer>
  </div>

</body>
</html>
'''

# Write to both web_lista_para_subir and archivos_finales_cliente
target_web = os.path.join(web_root, 'guia_de_archivos_y_bordado.html')
target_client = os.path.join(client_root, 'guia_de_archivos_y_bordado.html')

with open(target_web, 'w', encoding='utf-8') as f:
    f.write(html_content)
print('Wrote:', target_web)

with open(target_client, 'w', encoding='utf-8') as f:
    f.write(html_content)
print('Wrote:', target_client)

# Screenshot test
chrome_path = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
test_screenshot = r'C:\Users\danie\.gemini\antigravity\brain\c68dc380-8aa2-4180-a684-fbf64042ffc2\test_guia_sublimacion_screenshot.png'
cmd = [
    chrome_path,
    '--headless',
    '--disable-gpu',
    f'--screenshot={test_screenshot}',
    '--window-size=1280,1800',
    target_web
]
subprocess.run(cmd, check=True)
print('Screenshot generated successfully:', test_screenshot)
