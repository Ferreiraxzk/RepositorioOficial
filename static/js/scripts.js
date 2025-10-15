// Scroll suave ao clicar na seta
document.querySelector('.scroll-down').addEventListener('click', () => {
  window.scrollTo({
    top: window.innerHeight,
    behavior: 'smooth'
  });
});

// Efeito de fade-in quando rolar até as seções
const sections = document.querySelectorAll('.como-funciona, .sobre');

const fadeInOnScroll = () => {
  sections.forEach(sec => {
    const rect = sec.getBoundingClientRect();
    if (rect.top < window.innerHeight - 100) {
      sec.style.opacity = '1';
      sec.style.transform = 'translateY(0)';
    }
  });
};

window.addEventListener('scroll', fadeInOnScroll);

// Configura animação inicial das seções
sections.forEach(sec => {
  sec.style.opacity = '0';
  sec.style.transform = 'translateY(60px)';
  sec.style.transition = 'all 1s ease';
});
