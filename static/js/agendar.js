   // Importa o mesmo comportamento da página início
const openBtn = document.getElementById('openConfig');
const closeBtn = document.getElementById('closeConfig');
const panel = document.getElementById('configPanel');
const overlay = document.getElementById('overlay');
const toast = document.getElementById('toast');

const toggleDark = document.getElementById('toggleDark');
const toggleContrast = document.getElementById('toggleContrast');
const toggleNotifications = document.getElementById('toggleNotifications');
const toggleReduceMotion = document.getElementById('toggleReduceMotion');

// Abrir e fechar painel
openBtn?.addEventListener('click', openPanel);
closeBtn?.addEventListener('click', closePanel);
overlay?.addEventListener('click', closePanel);
document.addEventListener('keydown', (e) => { if (e.key === 'Escape') closePanel(); });

function openPanel() {
  panel.classList.add('active');
  overlay.classList.add('active');
}
function closePanel() {
  panel.classList.remove('active');
  overlay.classList.remove('active');
}

// Toast simples
function showToast(msg, time = 2500) {
  toast.textContent = msg;
  toast.classList.add('show');
  setTimeout(() => toast.classList.remove('show'), time);
}

// Armazenamento local
const SETTINGS_KEY = 'rf_settings_v1';
function saveSettings(o){ localStorage.setItem(SETTINGS_KEY, JSON.stringify(o)); }
function loadSettings(){ try{ return JSON.parse(localStorage.getItem(SETTINGS_KEY))||{} }catch{return{}}}

const saved = loadSettings();
if(saved.dark){document.body.classList.add('dark-mode');toggleDark.checked=true;}
if(saved.contrast){document.body.classList.add('high-contrast');toggleContrast.checked=true;}
if(saved.notifications===false)toggleNotifications.checked=false;
if(saved.reduceMotion)toggleReduceMotion.checked=true;

toggleDark?.addEventListener('change',e=>{
  document.body.classList.toggle('dark-mode',e.target.checked);
  saved.dark=e.target.checked; saveSettings(saved);
  showToast(e.target.checked?'Modo noturno ativado':'Modo noturno desativado');
});
toggleContrast?.addEventListener('change',e=>{
  document.body.classList.toggle('high-contrast',e.target.checked);
  saved.contrast=e.target.checked; saveSettings(saved);
  showToast(e.target.checked?'Alto contraste ativado':'Alto contraste desativado');
});
toggleNotifications?.addEventListener('change',e=>{
  saved.notifications=e.target.checked; saveSettings(saved);
  showToast(e.target.checked?'Notificações ativadas':'Notificações desativadas');
});
toggleReduceMotion?.addEventListener('change',e=>{
  saved.reduceMotion=e.target.checked; saveSettings(saved);
  document.documentElement.style.setProperty('scroll-behavior', e.target.checked?'auto':'smooth');
  showToast(e.target.checked?'Animações reduzidas':'Animações ativadas');
});

// Validação simples do formulário
document.querySelector('.agendar-form')?.addEventListener('submit', (e)=>{
  e.preventDefault();
  showToast('Agendamento confirmado com sucesso!');
  e.target.reset();
});