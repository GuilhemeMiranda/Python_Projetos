console.log('app.js: arquivo carregado');

document.addEventListener('DOMContentLoaded', () => {
  console.log('app.js: DOM carregado');

  const btnToggle = document.getElementById('btnToggle');
  const sidebar = document.getElementById('sidebar');
  const logoutBtn = document.getElementById('logoutBtn');

  // Toggle do menu lateral
  if (btnToggle && sidebar) {
    console.log('app.js: btnToggle e sidebar encontrados');
    btnToggle.addEventListener('click', () => {
      console.log('app.js: toggle sidebar');
      sidebar.classList.toggle('open');
    });
  } else {
    console.log('app.js: btnToggle ou sidebar não encontrados');
  }

  // Botão de logout
  if (logoutBtn) {
    console.log('app.js: logoutBtn encontrado');
    logoutBtn.addEventListener('click', () => {
      console.log('app.js: logout clicado');
      window.location.href = '/auth/logout';
    });
  } else {
    console.log('app.js: logoutBtn não encontrado');
  }

  // Marca links ativos no menu
  const navLinks = document.querySelectorAll('.nav-item');
  const currentPath = window.location.pathname;
  
  navLinks.forEach(link => {
    if (link.getAttribute('href') === currentPath) {
      link.classList.add('active');
    }
  });
});