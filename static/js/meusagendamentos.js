const panel = document.getElementById("configPanel");
const overlay = document.getElementById("overlay");
const openConfig = document.getElementById("openConfig");
const closeConfig = document.getElementById("closeConfig");
const lista = document.getElementById("listaAgendamentos");
const toast = document.getElementById("toast");

// === Abrir/Fechar painel ===
openConfig.addEventListener("click", () => {
  panel.classList.add("active");
  overlay.classList.add("active");
});
closeConfig.addEventListener("click", () => fecharPainel());
overlay.addEventListener("click", () => fecharPainel());

function fecharPainel() {
  panel.classList.remove("active");
  overlay.classList.remove("active");
}

// === Toast ===
function showToast(msg) {
  toast.textContent = msg;
  toast.classList.add("show");
  setTimeout(() => toast.classList.remove("show"), 2500);
}

// === Carregar agendamentos ===
function carregarAgendamentos() {
  const agendamentos = JSON.parse(localStorage.getItem("rf_agendamentos") || "[]");
  lista.innerHTML = "";

  if (agendamentos.length === 0) {
    lista.innerHTML = '<p class="vazio">Nenhum agendamento cadastrado.</p>';
    return;
  }

  agendamentos.forEach((a, i) => {
    const div = document.createElement("div");
    div.classList.add("agendamento-item");
    div.innerHTML = `
      <h3><i class="fa-solid fa-chalkboard-user"></i> ${a.professor}</h3>
      <p><strong>Turma:</strong> ${a.turma}</p>
      <p><strong>Data:</strong> ${a.data}</p>
      <p><strong>Horário:</strong> ${a.horario}</p>
      <p><strong>Quantidade:</strong> ${a.quantidade}</p>
      <button class="btn excluir" onclick="excluirAgendamento(${i})"><i class="fa-solid fa-trash"></i> Excluir</button>
    `;
    lista.appendChild(div);
  });
}

// === Funções dos botões ===
function novoAgendamento() {
  window.location.href = "/agendar";
}

function excluirAgendamento(i) {
  const agendamentos = JSON.parse(localStorage.getItem("rf_agendamentos") || "[]");
  agendamentos.splice(i, 1);
  localStorage.setItem("rf_agendamentos", JSON.stringify(agendamentos));
  carregarAgendamentos();
  showToast("Agendamento removido!");
}

function excluirTodos() {
  if (confirm("Tem certeza que deseja excluir todos os agendamentos?")) {
    localStorage.removeItem("rf_agendamentos");
    carregarAgendamentos();
    showToast("Todos os agendamentos foram excluídos.");
  }
}

// === Configurações ===
const toggleDark = document.getElementById("toggleDark");
const toggleContrast = document.getElementById("toggleContrast");
const toggleReduceMotion = document.getElementById("toggleReduceMotion");

toggleDark.addEventListener("change", () => {
  document.body.classList.toggle("dark-mode", toggleDark.checked);
  localStorage.setItem("rf_darkmode", toggleDark.checked);
});
toggleContrast.addEventListener("change", () => {
  document.body.classList.toggle("high-contrast", toggleContrast.checked);
  localStorage.setItem("rf_contrast", toggleContrast.checked);
});
toggleReduceMotion.addEventListener("change", () => {
  document.body.classList.toggle("reduce-motion", toggleReduceMotion.checked);
  localStorage.setItem("rf_reducemotion", toggleReduceMotion.checked);
});

// Aplicar preferências salvas
document.addEventListener("DOMContentLoaded", () => {
  toggleDark.checked = localStorage.getItem("rf_darkmode") === "true";
  toggleContrast.checked = localStorage.getItem("rf_contrast") === "true";
  toggleReduceMotion.checked = localStorage.getItem("rf_reducemotion") === "true";

  document.body.classList.toggle("dark-mode", toggleDark.checked);
  document.body.classList.toggle("high-contrast", toggleContrast.checked);
  document.body.classList.toggle("reduce-motion", toggleReduceMotion.checked);

  carregarAgendamentos();
});
