document.addEventListener('DOMContentLoaded', () => {
  const sidebar = document.getElementById('sidebar');
  const btn = document.getElementById('btnToggle');
  const links = document.querySelectorAll('.nav-item');

  // Toggle mobile
  if (btn && sidebar) {
    btn.addEventListener('click', () => sidebar.classList.toggle('open'));
  }

  // Marca link ativo conforme URL
  function setActive() {
    const path = location.pathname;
    links.forEach(a => {
      if (a.getAttribute('href') === path) a.classList.add('active');
      else a.classList.remove('active');
    });
  }
  setActive();

  // Fecha menu mobile ao clicar em link
  links.forEach(a => a.addEventListener('click', () => {
    if (window.innerWidth <= 880 && sidebar.classList.contains('open')) sidebar.classList.remove('open');
  }));

  // Logout
  const logoutBtn = document.getElementById('logoutBtn');
  if (logoutBtn) {
    logoutBtn.addEventListener('click', () => {
      // usa GET para acionar logout no servidor e redirecionar
      window.location.href = '/auth/logout';
    });
  }
});