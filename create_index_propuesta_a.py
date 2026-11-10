import re, os, shutil

src = r"c:\Users\danie\Downloads\SF\web\index.html"
dst = r"c:\Users\danie\Downloads\SF\web\index_propuesta_a.html"
dst_prod = r"c:\Users\danie\Downloads\SF\web_lista_para_subir\index_propuesta_a.html"

with open(src, "r", encoding="utf-8") as f:
    text = f.read()

# 1. Update title tag
text = text.replace(
    "<title>SF Entretenimiento • Valencia, Maracay, Pto. Cabello • Eventos VIP, Pantallas LED, Tarimas y Sonido</title>",
    "<title>SF Entretenimiento • [PROPUESTA A: Caída Escultórica 3D] • Web Principal</title>"
)

# 2. Add shockwave element and styling to the hero stage
shockwave_css = """
    /* Propuesta A Shockwave Ripple */
    .prop-a-shockwave {
      position: absolute;
      top: 55%;
      left: 58%;
      transform: translate(-50%, -50%) scale(0);
      width: 480px;
      height: 140px;
      border: 2px solid rgba(229, 193, 88, 0.85);
      border-radius: 50%;
      pointer-events: none;
      opacity: 0;
      z-index: 25;
      box-shadow: 0 0 30px rgba(229, 193, 88, 0.5), inset 0 0 20px rgba(229, 193, 88, 0.3);
    }
    .prop-a-shockwave.rippling {
      animation: rippleShockwave 0.75s cubic-bezier(0.2, 0.8, 0.2, 1) forwards;
    }
    @keyframes rippleShockwave {
      0% { transform: translate(-50%, -50%) scale(0.2); opacity: 0.9; }
      100% { transform: translate(-50%, -50%) scale(1.75); opacity: 0; }
    }
"""

text = text.replace("</style>", shockwave_css + "\n  </style>")

# 3. Add shockwave inside heroParallaxInner
old_inner = '''      <div id="heroParallaxInner" class="hero-focal-canvas">
        <img src="img/logo_layers/hero_plate_vip_stage.jpg" alt="SF Placa 3D Escenario VIP" class="drop-layer z-10" />'''

new_inner = '''      <div id="heroParallaxInner" class="hero-focal-canvas">
        <img src="img/logo_layers/hero_plate_vip_stage.jpg" alt="SF Placa 3D Escenario VIP" class="drop-layer z-10" />
        <div id="heroShockwave" class="prop-a-shockwave"></div>'''

text = text.replace(old_inner, new_inner)

# 4. Add floating badge at top of page indicating this is Propuesta A
badge_html = '''  <!-- Floating Mode Banner for Propuesta A -->
  <div class="fixed top-2 left-1/2 -translate-x-1/2 z-50 bg-black/80 backdrop-blur-md border border-amber-400/50 rounded-full px-5 py-2 shadow-2xl flex items-center gap-3">
    <span class="w-2.5 h-2.5 rounded-full bg-emerald-400 animate-pulse"></span>
    <span class="text-xs font-semibold tracking-wider text-amber-200 uppercase">Vista de Prueba: Propuesta A (Caída Escultórica 3D)</span>
    <a href="index.html" class="text-xs text-white/70 hover:text-white underline ml-2">Volver a Web Estándar</a>
  </div>
'''

text = text.replace('<header class="fixed top-0 left-0 right-0 z-40', badge_html + '\n  <header class="fixed top-0 left-0 right-0 z-40')

# 5. In triggerTopDrop, trigger the shockwave at t=700ms
old_trigger = '''      [560, 1160, 1760].forEach(ms => {
        dropTimers.push(setTimeout(() => {
          stage.classList.remove('shake-impact');
          void stage.offsetWidth;
          stage.classList.add('shake-impact');
        }, ms));
      });'''

new_trigger = '''      [560, 1160, 1760].forEach(ms => {
        dropTimers.push(setTimeout(() => {
          stage.classList.remove('shake-impact');
          void stage.offsetWidth;
          stage.classList.add('shake-impact');
        }, ms));
      });

      // Propuesta A Shockwave trigger
      const sw = document.getElementById('heroShockwave');
      if (sw) {
        sw.classList.remove('rippling');
        dropTimers.push(setTimeout(() => {
          void sw.offsetWidth;
          sw.classList.add('rippling');
        }, 700));
      }'''

text = text.replace(old_trigger, new_trigger)

with open(dst, "w", encoding="utf-8") as f:
    f.write(text)

with open(dst_prod, "w", encoding="utf-8") as f:
    f.write(text)

print("Created index_propuesta_a.html in web/ and web_lista_para_subir/ successfully!")
