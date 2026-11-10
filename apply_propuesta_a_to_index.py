# -*- coding: utf-8 -*-
import os, re, shutil, subprocess

base_dir = r'C:\Users\danie\Downloads\SF'
web_pub = os.path.join(base_dir, 'web_lista_para_subir')
web_src = os.path.join(base_dir, 'web')
client_web = os.path.join(base_dir, 'archivos_finales_cliente', '03_paquete_web')

# Source of Propuesta A
prop_a_file = os.path.join(web_pub, 'index_propuesta_a.html')
with open(prop_a_file, 'r', encoding='utf-8', errors='ignore') as f:
    raw_prop_a = f.read()

# Normalize excessive blank lines if present
lines = [l.rstrip() for l in raw_prop_a.splitlines()]
clean_lines = []
last_empty = False
for l in lines:
    if not l:
        if not last_empty:
            clean_lines.append('')
            last_empty = True
    else:
        clean_lines.append(l)
        last_empty = False
clean_prop_a = '\n'.join(clean_lines)

# Backup current index.html in web_lista_para_subir
idx_pub = os.path.join(web_pub, 'index.html')
shutil.copy2(idx_pub, os.path.join(web_pub, 'index_caida_fuerte_backup.html'))

# Update index.html across all target locations
targets = [
    os.path.join(web_pub, 'index.html'),
    os.path.join(web_src, 'index.html'),
    os.path.join(client_web, 'index.html')
]

for t in targets:
    with open(t, 'w', encoding='utf-8') as f:
        f.write(clean_prop_a)
    print('Updated with Propuesta A soft drop:', t)

# Verify with Chrome headless screenshot
chrome_path = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
screenshot_path = r'C:\Users\danie\.gemini\antigravity\brain\c68dc380-8aa2-4180-a684-fbf64042ffc2\test_index_updated_preview.png'

cmd = [
    chrome_path,
    '--headless',
    '--disable-gpu',
    f'--screenshot={screenshot_path}',
    '--window-size=1280,800',
    targets[0]
]
subprocess.run(cmd, check=True)
print('Screenshot generated successfully:', screenshot_path)
