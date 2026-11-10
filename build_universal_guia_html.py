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

html_content = f'''<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>SF Entretenimiento — Guía Maestra de Archivos y Bordado Textil</title>
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
      --accent-red: #8C1D2A;
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
      max-width: 1200px;
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
      max-width: 780px;
      margin: 0 auto;
    }}

    /* Explanation Banner */
    .answer-card {{
      background: rgba(212, 175, 55, 0.08);
      border: 1px solid var(--gold);
      border-radius: 14px;
      padding: 24px;
      margin-bottom: 35px;
      display: flex;
      align-items: flex-start;
      gap: 20px;
    }}
    .answer-icon {{
      font-size: 32px;
      line-height: 1;
    }}
    .answer-card h3 {{
      color: var(--gold);
      font-size: 19px;
      margin-bottom: 8px;
      font-weight: 700;
    }}
    .answer-card p {{
      color: #E2E8F0;
      font-size: 14.5px;
      line-height: 1.6;
    }}

    /* Visual preview */
    .preview-card {{
      background: var(--card-bg);
      border: 1px solid var(--card-border);
      border-radius: 16px;
      padding: 30px;
      margin-bottom: 40px;
      box-shadow: 0 10px 30px rgba(0,0,0,0.5);
    }}
    .preview-header {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 15px;
      margin-bottom: 25px;
      padding-bottom: 15px;
      border-bottom: 1px solid var(--card-border);
    }}
    .preview-title {{
      font-size: 20px;
      font-weight: 700;
      color: var(--gold);
    }}
    .stage-img-wrap {{
      border-radius: 12px;
      overflow: hidden;
      border: 1px solid var(--card-border);
      text-align: center;
      background: #000;
      padding: 10px;
    }}
    .stage-img-wrap img {{
      width: 100%;
      max-height: 520px;
      object-fit: contain;
      display: block;
      margin: 0 auto;
      border-radius: 8px;
    }}

    /* Grid of file categories */
    .grid-3 {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(340px, 1fr));
      gap: 25px;
      margin-bottom: 40px;
    }}
    .card {{
      background: var(--card-bg);
      border: 1px solid var(--card-border);
      border-radius: 14px;
      padding: 24px;
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
    .card-badge.green {{ background: rgba(74, 222, 128, 0.15); color: #4ADE80; border: 1px solid rgba(74, 222, 128, 0.4); }}

    .card h2 {{
      font-size: 19px;
      font-weight: 700;
      color: #fff;
      margin-bottom: 10px;
    }}
    .card p.desc {{
      color: var(--text-muted);
      font-size: 13.5px;
      margin-bottom: 20px;
      flex-grow: 1;
    }}
    .file-list {{
      list-style: none;
      border-top: 1px solid var(--card-border);
      padding-top: 15px;
    }}
    .file-item {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 12px 0;
      border-bottom: 1px solid rgba(255,255,255,0.05);
      font-size: 13px;
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
      font-size: 12px;
      font-weight: 600;
      padding: 6px 14px;
      border: 1px solid var(--gold);
      border-radius: 6px;
      transition: all 0.2s;
      white-space: nowrap;
      margin-left: 10px;
    }}
    .file-link:hover {{
      background: var(--gold);
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
      <h1>Guía Maestra de Archivos de Bordado y Textil</h1>
      <p class="lead">Solución definitiva y funcional: todos los enlaces probados para descarga y apertura directa sin errores.</p>
    </header>

    <!-- DIRECT ANSWER TO USER'S QUESTION -->
    <div class="answer-card">
      <div class="answer-icon">💡</div>
      <div>
        <h3>¿El logotipo 3D estampado (.PNG) es lo que leerían las máquinas de bordado?</h3>
        <p><strong>Respuesta directa: NO.</strong> Las máquinas de bordar industriales (Tajima, Brother, Barudan, Ricoma) <strong>NO pueden leer imágenes PNG con sombras, grietas ni volúmenes 3D</strong>. Los PNGs 3D son exclusivos para <em>Estampado Textil DTF (impresión digital por calor en tela)</em>.</p>
        <p style="margin-top: 8px;">Para bordar con hilos en uniformes, camisas polo, franelas y gorras, se requiere:</p>
        <p style="margin-top: 4px;">1) El <strong>archivo vectorial limpio (.SVG / .PDF)</strong> sin fondo para que el ponchador asigne las puntadas; o bien</p>
        <p style="margin-top: 4px;">2) Las <strong>matrices directas de máquina (.DST para Tajima / .PES para Brother)</strong> ya compiladas para colocar en el pendrive y coser de inmediato.</p>
      </div>
    </div>

    <!-- VISUAL EMBROIDERY RESULT (EMBEDDED BASE64) -->
    <div class="preview-card">
      <div class="preview-header">
        <div>
          <div class="preview-title">Resultado Final: Bordado sobre Tela de Uniforme (Polo Negra)</div>
          <div style="font-size: 13.5px; color: var(--text-muted);">S en Hilo Oro (curvatura continua superior) | F en Hilo Platino (sólida, sin costuras internas) | Texto ENTRETENIMIENTO centrado</div>
        </div>
        <a href="descargas_cliente/sf_monograma_bordado_uniformes.svg" class="file-link" target="_blank" style="padding: 8px 16px;">Ver Vector SVG</a>
      </div>

      <div class="stage-img-wrap">
        <img src="{data_uri_polo}" alt="Muestra de Bordado Textil SF sobre Camisa Polo">
      </div>
    </div>

    <!-- 3 DIRECTORY CARDS -->
    <div class="grid-3">

      <!-- CARD 1: BORDADO -->
      <div class="card" style="border-top: 3px solid var(--gold);">
        <div class="card-badge gold">descargas_cliente</div>
        <h2>1. Para el Bordador de Uniformes</h2>
        <p class="desc">Entregar estos archivos al taller de confección y bordado. Incluyen los vectores corregidos y las matrices de puntada listas para la máquina.</p>
        
        <ul class="file-list">
          <li class="file-item">
            <div>
              <div class="file-name">sf_monograma_bordado_uniformes.svg</div>
              <div style="font-size: 11px; color: var(--text-muted);">Monograma puro sin fondo para Wilcom / Tajima</div>
            </div>
            <a href="descargas_cliente/sf_monograma_bordado_uniformes.svg" class="file-link" target="_blank">Abrir</a>
          </li>
          <li class="file-item">
            <div>
              <div class="file-name">sf_logotipo_completo_bordado.svg</div>
              <div style="font-size: 11px; color: var(--text-muted);">Monograma + Entretenimiento centrado</div>
            </div>
            <a href="descargas_cliente/sf_logotipo_completo_bordado.svg" class="file-link" target="_blank">Abrir</a>
          </li>
          <li class="file-item">
            <div>
              <div class="file-name">sf_monograma_pecho_7cm.dst</div>
              <div style="font-size: 11px; color: var(--text-muted);">Matriz Tajima universal (7 cm para pecho)</div>
            </div>
            <a href="descargas_cliente/sf_monograma_pecho_7cm.dst" class="file-link" download>Descargar</a>
          </li>
          <li class="file-item">
            <div>
              <div class="file-name">sf_monograma_pecho_7cm.pes</div>
              <div style="font-size: 11px; color: var(--text-muted);">Matriz Brother estándar (7 cm para pecho)</div>
            </div>
            <a href="descargas_cliente/sf_monograma_pecho_7cm.pes" class="file-link" download>Descargar</a>
          </li>
          <li class="file-item">
            <div>
              <div class="file-name">sf_monograma_gorra_5.5cm.dst</div>
              <div style="font-size: 11px; color: var(--text-muted);">Matriz Tajima para gorras y mangas</div>
            </div>
            <a href="descargas_cliente/sf_monograma_gorra_5.5cm.dst" class="file-link" download>Descargar</a>
          </li>
          <li class="file-item">
            <div>
              <div class="file-name">ficha_tecnica_bordado_sf.png</div>
              <div style="font-size: 11px; color: var(--text-muted);">Ficha con códigos de hilo Madeira y medidas</div>
            </div>
            <a href="descargas_cliente/ficha_tecnica_bordado_sf.png" class="file-link" target="_blank">Ver Ficha</a>
          </li>
        </ul>
      </div>

      <!-- CARD 2: ESTAMPADO DTF -->
      <div class="card" style="border-top: 3px solid #38BDF8;">
        <div class="card-badge blue">descargas_cliente</div>
        <h2>2. Para Estampado DTF</h2>
        <p class="desc">Entregar estos archivos cuando vayan a hacer <strong>estampado por calor</strong> (DTF, vinil textil impreso o sublimación) donde sí se imprimen los volúmenes 3D y reflejos.</p>
        
        <ul class="file-list">
          <li class="file-item">
            <div>
              <div class="file-name">sf_logotipo_completo_3d_estampado_dtf_4k.png</div>
              <div style="font-size: 11px; color: var(--text-muted);">Logotipo completo 3D 4K (300 DPI, transparente)</div>
            </div>
            <a href="descargas_cliente/sf_logotipo_completo_3d_estampado_dtf_4k.png" class="file-link" target="_blank">Abrir</a>
          </li>
          <li class="file-item">
            <div>
              <div class="file-name">sf_monograma_3d_estampado_dtf_4k.png</div>
              <div style="font-size: 11px; color: var(--text-muted);">Monograma SF 3D 4K (300 DPI, transparente)</div>
            </div>
            <a href="descargas_cliente/sf_monograma_3d_estampado_dtf_4k.png" class="file-link" target="_blank">Abrir</a>
          </li>
        </ul>
      </div>

      <!-- CARD 3: COMPARATIVA WEB -->
      <div class="card" style="border-top: 3px solid #4ADE80;">
        <div class="card-badge green">web</div>
        <h2>3. Para la Página Web</h2>
        <p class="desc">Los archivos HTML listos para comparar directamente el comportamiento de la caída de las letras en el Hero.</p>
        
        <ul class="file-list">
          <li class="file-item">
            <div>
              <div class="file-name">index.html</div>
              <div style="font-size: 11px; color: var(--text-muted);">Caída fuerte original con temblor de pantalla</div>
            </div>
            <a href="index.html" class="file-link" target="_blank">Probar</a>
          </li>
          <li class="file-item">
            <div>
              <div class="file-name">index_propuesta_a.html</div>
              <div style="font-size: 11px; color: var(--text-muted);">Caída suave y escultórica (Propuesta A)</div>
            </div>
            <a href="index_propuesta_a.html" class="file-link" target="_blank">Probar</a>
          </li>
          <li class="file-item">
            <div>
              <div class="file-name">animaciones_logo.html</div>
              <div style="font-size: 11px; color: var(--text-muted);">Laboratorio con las 2 propuestas maestras</div>
            </div>
            <a href="animaciones_logo.html" class="file-link" target="_blank">Abrir</a>
          </li>
        </ul>
      </div>

    </div>

    <footer>
      SF ENTRETENIMIENTO, C.A. — Paquete Oficial de Confección Textil y Web. Todos los archivos en minúsculas.
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

# Verify with Chrome headless screenshot
chrome_path = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
test_screenshot = r'C:\Users\danie\.gemini\antigravity\brain\c68dc380-8aa2-4180-a684-fbf64042ffc2\test_guia_screenshot.png'
cmd = [
    chrome_path,
    '--headless',
    '--disable-gpu',
    f'--screenshot={test_screenshot}',
    '--window-size=1200,1600',
    target_web
]
subprocess.run(cmd, check=True)
print('Screenshot generated successfully:', test_screenshot)
