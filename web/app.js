/**
 * SF Entretenimiento - The Events Lounge Edition
 * Client-Side Controller: Gallery Filtering, Concierge Quote Generator, Video Controls.
 */

document.addEventListener('DOMContentLoaded', () => {
  initGalleryFilter();
  initConciergeCalculator();
  initVideoPlayer();
});

// --- 1. PORTFOLIO GALLERY FILTER ---
function initGalleryFilter() {
  const filterBtns = document.querySelectorAll('.gallery-filter-btn');
  const galleryItems = document.querySelectorAll('.gallery-item');

  if (!filterBtns.length || !galleryItems.length) return;

  filterBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      // Toggle active style
      filterBtns.forEach(b => {
        b.classList.remove('bg-purple-600', 'text-white', 'shadow-lg');
        b.classList.add('bg-purple-950/40', 'text-purple-300');
      });
      btn.classList.add('bg-purple-600', 'text-white', 'shadow-lg');
      btn.classList.remove('bg-purple-950/40', 'text-purple-300');

      const filter = btn.dataset.filter;

      galleryItems.forEach(item => {
        if (filter === 'all' || item.dataset.category === filter) {
          item.style.display = 'block';
          item.style.opacity = '0';
          setTimeout(() => { item.style.opacity = '1'; }, 50);
        } else {
          item.style.display = 'none';
        }
      });
    });
  });
}

// --- 2. CONCIERGE EVENT QUOTE ESTIMATOR ---
function initConciergeCalculator() {
  const eventType = document.getElementById('concierge-type');
  const guests = document.getElementById('concierge-guests');
  const city = document.getElementById('concierge-city');
  const addons = document.querySelectorAll('.concierge-addon');
  const summaryBox = document.getElementById('concierge-summary');
  const btnSaid = document.getElementById('concierge-btn-said');
  const btnFernando = document.getElementById('concierge-btn-fernando');

  if (!eventType || !guests || !summaryBox) return;

  function recalculate() {
    const selectedType = eventType.value;
    const selectedGuests = guests.value;
    const selectedCity = city ? city.value : 'Valencia';

    const selectedAddons = [];
    addons.forEach(chk => {
      if (chk.checked) selectedAddons.push(chk.dataset.label || chk.value);
    });

    let message = `Estimados Said y Fernando,\n\n`;
    message += `Deseo consultar presupuesto y disponibilidad para un evento:\n\n`;
    message += `• Celebración: ${selectedType}\n`;
    message += `• Invitados: ${selectedGuests}\n`;
    message += `• Ciudad: ${selectedCity}\n`;

    if (selectedAddons.length > 0) {
      message += `• Servicios solicitados:\n  - ` + selectedAddons.join('\n  - ') + `\n`;
    }

    message += `\n¿Podrían indicarme opciones de fecha y propuesta técnica? ¡Muchas gracias!`;

    summaryBox.textContent = message;

    const encoded = encodeURIComponent(message);
    if (btnSaid) {
      btnSaid.href = `https://wa.me/584144246260?text=${encoded}`;
    }
    if (btnFernando) {
      btnFernando.href = `https://wa.me/584144270723?text=${encoded}`;
    }
  }

  eventType.addEventListener('change', recalculate);
  guests.addEventListener('change', recalculate);
  if (city) city.addEventListener('change', recalculate);
  addons.forEach(chk => chk.addEventListener('change', recalculate));

  recalculate();
}

// --- 3. VIDEO REEL CONTROLLER ---
function initVideoPlayer() {
  const video = document.getElementById('lounge-reel-video');
  const playOverlay = document.getElementById('reel-play-btn');

  if (!video || !playOverlay) return;

  playOverlay.addEventListener('click', () => {
    if (video.paused) {
      video.play();
      playOverlay.classList.add('opacity-0', 'pointer-events-none');
    } else {
      video.pause();
      playOverlay.classList.remove('opacity-0', 'pointer-events-none');
    }
  });

  video.addEventListener('click', () => {
    if (video.paused) {
      video.play();
      playOverlay.classList.add('opacity-0', 'pointer-events-none');
    } else {
      video.pause();
      playOverlay.classList.remove('opacity-0', 'pointer-events-none');
    }
  });

  video.addEventListener('ended', () => {
    playOverlay.classList.remove('opacity-0', 'pointer-events-none');
  });
}
