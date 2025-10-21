// Elements
const openBtn = document.getElementById('openConfig');
const closeBtn = document.getElementById('closeConfig');
const panel = document.getElementById('configPanel');
const overlay = document.getElementById('overlay');
const toast = document.getElementById('toast');

// toggles
const toggleDark = document.getElementById('toggleDark');
const toggleContrast = document.getElementById('toggleContrast');
const toggleNotifications = document.getElementById('toggleNotifications');
const toggleReduceMotion = document.getElementById('toggleReduceMotion');

// feedback
const fbName = document.getElementById('fbName');
const fbEmail = document.getElementById('fbEmail');
const fbMessage = document.getElementById('fbMessage');
const charCount = document.getElementById('charCount');
const sendFeedback = document.getElementById('sendFeedback');
const fbStatus = document.getElementById('fbStatus');

// open / close panel
openBtn?.addEventListener('click', openPanel);
closeBtn?.addEventListener('click', closePanel);
overlay?.addEventListener('click', closePanel);
document.addEventListener('keydown', (e) => { if (e.key === 'Escape') closePanel(); });

function openPanel() {
  panel.classList.add('active');
  overlay.classList.add('active');
  panel.setAttribute('aria-hidden', 'false');
}

function closePanel() {
  panel.classList.remove('active');
  overlay.classList.remove('active');
  panel.setAttribute('aria-hidden', 'true');
}

// toast helper
function showToast(msg, time = 2500) {
  if (!toast) return;
  toast.textContent = msg;
  toast.classList.add('show');
  setTimeout(() => toast.classList.remove('show'), time);
}

// persist settings in localStorage
const SETTINGS_KEY = 'rf_settings_v1';
function saveSettings(obj) {
  localStorage.setItem(SETTINGS_KEY, JSON.stringify(obj));
}
function loadSettings() {
  try {
    const s = JSON.parse(localStorage.getItem(SETTINGS_KEY));
    return s || {};
  } catch (e) { return {}; }
}

// apply saved settings on load
const saved = loadSettings();
if (saved.dark) { document.body.classList.add('dark-mode'); toggleDark.checked = true; }
if (saved.contrast) { document.body.classList.add('high-contrast'); toggleContrast.checked = true; }
if (saved.notifications === false) toggleNotifications.checked = false;
if (saved.reduceMotion) toggleReduceMotion.checked = true;

// toggle handlers
toggleDark?.addEventListener('change', (e) => {
  document.body.classList.toggle('dark-mode', e.target.checked);
  saved.dark = e.target.checked; saveSettings(saved);
  showToast(e.target.checked ? 'Modo noturno ativado' : 'Modo noturno desativado');
});

toggleContrast?.addEventListener('change', (e) => {
  document.body.classList.toggle('high-contrast', e.target.checked);
  saved.contrast = e.target.checked; saveSettings(saved);
  showToast(e.target.checked ? 'Alto contraste ativado' : 'Alto contraste desativado');
});

toggleNotifications?.addEventListener('change', (e) => {
  saved.notifications = e.target.checked; saveSettings(saved);
  showToast(e.target.checked ? 'Notificações ativadas' : 'Notificações desativadas');
});

toggleReduceMotion?.addEventListener('change', (e) => {
  saved.reduceMotion = e.target.checked; saveSettings(saved);
  if (e.target.checked) document.documentElement.style.setProperty('scroll-behavior', 'auto');
  else document.documentElement.style.setProperty('scroll-behavior', 'smooth');
  showToast(e.target.checked ? 'Animações reduzidas' : 'Animações ativadas');
});

// feedback char count
fbMessage?.addEventListener('input', (e) => {
  const len = e.target.value.length;
  charCount.textContent = `${len} / 300`;
});

// send feedback: simple validation + store to localStorage
sendFeedback?.addEventListener('click', () => {
  const message = fbMessage.value.trim();
  if (!message) {
    fbStatus.textContent = 'Escreva uma mensagem antes de enviar.';
    fbStatus.style.color = '#c23';
    return;
  }

  const entry = {
    name: fbName.value.trim() || null,
    email: fbEmail.value.trim() || null,
    message,
    createdAt: new Date().toISOString()
  };

  // store
  const key = 'rf_feedbacks';
  const arr = JSON.parse(localStorage.getItem(key) || '[]');
  arr.unshift(entry);
  localStorage.setItem(key, JSON.stringify(arr));

  // feedback UI
  fbStatus.style.color = 'green';
  fbStatus.textContent = 'Obrigado! Feedback enviado.';
  fbMessage.value = '';
  charCount.textContent = '0 / 300';
  fbName.value = '';
  fbEmail.value = '';

  showToast('Feedback enviado — obrigado!');

  // hide message after a bit
  setTimeout(() => fbStatus.textContent = '', 4200);
});

// progressive reveal for step-cards
function revealOnScroll() {
  document.querySelectorAll('.step-card').forEach(card => {
    const rect = card.getBoundingClientRect();
    if (rect.top < window.innerHeight - 80) card.classList.add('step-visible');
  });
}
window.addEventListener('scroll', revealOnScroll);
window.addEventListener('load', revealOnScroll);
