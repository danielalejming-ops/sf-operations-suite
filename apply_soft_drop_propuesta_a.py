import re

path = r'c:\Users\danie\Downloads\SF\web\index_propuesta_a.html'
path_prod = r'c:\Users\danie\Downloads\SF\web_lista_para_subir\index_propuesta_a.html'

with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Update CSS: replace heavy drops and tremor with gentle sculptural physics
old_drop_css = '''    .hero-fullbleed-stage.primed .layer-s,
    .hero-fullbleed-stage.primed .layer-f,
    .hero-fullbleed-stage.primed .layer-ent,
    .hero-fullbleed-stage.primed .layer-phones {
      opacity: 0;
      transform: translateY(-108%);
    }

    .hero-fullbleed-stage.primed .layer-s-refl,
    .hero-fullbleed-stage.primed .layer-f-refl {
      opacity: 0;
      transform: translateY(108%);
    }

    @keyframes dropFromTopToCenter {
      0% {
        opacity: 1;
        transform: translateY(-108%);
        filter: brightness(1.55) drop-shadow(0 -18px 16px rgba(212, 175, 55, 0.4));
      }
      78% {
        opacity: 1;
        transform: translateY(0%);
        filter: brightness(1.45) drop-shadow(0 0 28px rgba(255, 228, 135, 0.9));
      }
      88% {
        transform: translateY(-2.5%);
      }
      100% {
        opacity: 1;
        transform: translateY(0%);
        filter: brightness(1.08) drop-shadow(0 12px 24px rgba(0, 0, 0, 0.85));
      }
    }

    @keyframes riseFromBottomToCenter {
      0% {
        opacity: 0;
        transform: translateY(108%);
      }
      30% {
        opacity: 0.8;
      }
      78% {
        opacity: 1;
        transform: translateY(0%);
      }
      88% {
        transform: translateY(2.5%);
      }
      100% {
        opacity: 1;
        transform: translateY(0%);
      }
    }

    @keyframes stageTremor {
      0%, 100% { transform: translate(0, 0); }
      20% { transform: translate(-7px, 8px); }
      40% { transform: translate(7px, -6px); }
      60% { transform: translate(-4px, 4px); }
      80% { transform: translate(2px, -2px); }
    }

    .hero-fullbleed-stage.dropping .layer-s {
      animation: dropFromTopToCenter 0.60s cubic-bezier(0.45, 0.05, 0.85, 0.25) 0.08s forwards;
    }
    .hero-fullbleed-stage.dropping .layer-s-refl {
      animation: riseFromBottomToCenter 0.60s cubic-bezier(0.45, 0.05, 0.85, 0.25) 0.08s forwards;
    }
    .hero-fullbleed-stage.dropping .layer-f {
      animation: dropFromTopToCenter 0.60s cubic-bezier(0.45, 0.05, 0.85, 0.25) 0.68s forwards;
    }
    .hero-fullbleed-stage.dropping .layer-f-refl {
      animation: riseFromBottomToCenter 0.60s cubic-bezier(0.45, 0.05, 0.85, 0.25) 0.68s forwards;
    }
    .hero-fullbleed-stage.dropping .layer-ent {
      animation: dropFromTopToCenter 0.58s cubic-bezier(0.45, 0.05, 0.85, 0.25) 1.28s forwards;
    }
    .hero-fullbleed-stage.dropping .layer-phones {
      animation: dropFromTopToCenter 0.52s cubic-bezier(0.45, 0.05, 0.85, 0.25) 1.65s forwards;
    }'''

new_drop_css = '''    /* FÍSICA ESCULTÓRICA SUAVE Y ELEGANTE (PROPUESTA A) - CAÍDA CORTA Y FLUIDA */
    .hero-fullbleed-stage.primed .layer-s,
    .hero-fullbleed-stage.primed .layer-f {
      opacity: 0;
      transform: translateY(-130px);
    }
    .hero-fullbleed-stage.primed .layer-s-refl,
    .hero-fullbleed-stage.primed .layer-f-refl {
      opacity: 0;
      transform: translateY(130px);
    }
    .hero-fullbleed-stage.primed .layer-ent,
    .hero-fullbleed-stage.primed .layer-phones {
      opacity: 0;
      transform: translateY(16px);
    }

    @keyframes dropSculpturalSoft {
      0% {
        opacity: 0;
        transform: translateY(-130px);
        filter: brightness(1.2);
      }
      35% {
        opacity: 1;
      }
      80% {
        transform: translateY(0%);
        filter: brightness(1.15) drop-shadow(0 0 16px rgba(229, 193, 88, 0.4));
      }
      90% {
        transform: translateY(-3.5px); /* Micro rebote sutil y elástico */
      }
      100% {
        opacity: 1;
        transform: translateY(0%);
        filter: brightness(1.0) drop-shadow(0 10px 22px rgba(0, 0, 0, 0.85));
      }
    }

    @keyframes riseSculpturalSoft {
      0% {
        opacity: 0;
        transform: translateY(130px);
      }
      35% {
        opacity: 0.85;
      }
      80% {
        transform: translateY(0%);
      }
      90% {
        transform: translateY(3.5px); /* Reflejo rebota simétricamente */
      }
      100% {
        opacity: 1;
        transform: translateY(0%);
      }
    }

    @keyframes fadeEntSoft {
      0% {
        opacity: 0;
        transform: translateY(16px);
      }
      100% {
        opacity: 1;
        transform: translateY(0%);
      }
    }

    /* Coreografía suave sin temblor brusco de pantalla */
    .hero-fullbleed-stage.dropping .layer-s {
      animation: dropSculpturalSoft 0.75s cubic-bezier(0.175, 0.885, 0.32, 1.25) 0.05s forwards;
    }
    .hero-fullbleed-stage.dropping .layer-s-refl {
      animation: riseSculpturalSoft 0.75s cubic-bezier(0.175, 0.885, 0.32, 1.25) 0.05s forwards;
    }
    .hero-fullbleed-stage.dropping .layer-f {
      animation: dropSculpturalSoft 0.75s cubic-bezier(0.175, 0.885, 0.32, 1.25) 0.38s forwards;
    }
    .hero-fullbleed-stage.dropping .layer-f-refl {
      animation: riseSculpturalSoft 0.75s cubic-bezier(0.175, 0.885, 0.32, 1.25) 0.38s forwards;
    }
    .hero-fullbleed-stage.dropping .layer-ent {
      animation: fadeEntSoft 0.65s ease-out 0.78s forwards;
    }
    .hero-fullbleed-stage.dropping .layer-phones {
      animation: fadeEntSoft 0.60s ease-out 1.05s forwards;
    }'''

# Normalize and replace
text_norm = text.replace('\r\n', '\n')
old_norm = old_drop_css.replace('\r\n', '\n')
new_norm = new_drop_css.replace('\r\n', '\n')

assert old_norm in text_norm, 'old_drop_css not found'
text_norm = text_norm.replace(old_norm, new_norm)

# 2. In triggerTopDrop(), remove the stageTremor shake loops
old_shake_code = '''      [560, 1160, 1760].forEach(ms => {
        dropTimers.push(setTimeout(() => {
          stage.classList.remove('shake-impact');
          void stage.offsetWidth;
          stage.classList.add('shake-impact');
        }, ms));
      });'''

new_shake_code = '''      // En Propuesta A NO hay temblor brusco de pantalla: la caída es suave, fluida y escultórica'''

old_shake_norm = old_shake_code.replace('\r\n', '\n')
new_shake_norm = new_shake_code.replace('\r\n', '\n')

if old_shake_norm in text_norm:
    text_norm = text_norm.replace(old_shake_norm, new_shake_norm)

# Restore CRLF
final_text = text_norm.replace('\n', '\r\n')

with open(path, 'w', encoding='utf-8') as f:
    f.write(final_text)

with open(path_prod, 'w', encoding='utf-8') as f:
    f.write(final_text)

print('Updated index_propuesta_a.html with the gentle, smooth Propuesta A sculptural drop!')
