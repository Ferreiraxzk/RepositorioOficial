// Efeito de aparição suave ao rolar
window.addEventListener("scroll", () => {
  document.querySelectorAll(".step-card").forEach((card) => {
    const rect = card.getBoundingClientRect();
    if (rect.top < window.innerHeight - 80) {
      card.classList.add("step-visible");
    }
  });
});


