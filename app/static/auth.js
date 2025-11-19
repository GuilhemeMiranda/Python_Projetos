console.log('auth.js: arquivo carregado');

document.addEventListener('DOMContentLoaded', () => {
  console.log('auth.js: DOM carregado');

  const btn = document.getElementById('btnLogin');
  const btnRegistrar = document.getElementById('btnRegistrar');
  const msg = document.getElementById('loginMsg');

  async function login() {
    msg.textContent = '';
    msg.className = 'muted';

    const email = document.getElementById('email').value || '';
    const senha = document.getElementById('senha').value || '';

    if (!email || !senha) {
      msg.textContent = 'E-mail e senha são obrigatórios';
      msg.className = 'muted error';
      return;
    }

    msg.textContent = 'Autenticando...';

    try {
      const res = await fetch('/auth/login', {
        method: 'POST',
        credentials: 'same-origin',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, senha })
      });

      if (res.ok) {
        const data = await res.json();
        window.location.href = data.redirect || '/ui/dashboard';
        return;
      }

      const err = await res.json().catch(() => ({ detail: res.statusText }));
      msg.textContent = `Erro: ${err.detail || res.statusText}`;
      msg.className = 'muted error';
    } catch (e) {
      msg.textContent = 'Erro de conexão';
      msg.className = 'muted error';
      console.error(e);
    }
  }

  if (btn) {
    btn.addEventListener('click', login);
  }

  // Botão para ir para tela de registro
  if (btnRegistrar) {
    btnRegistrar.addEventListener('click', () => {
      window.location.href = '/ui/registro';
    });
  }

  // Enter no formulário
  const form = document.getElementById('loginForm');
  if (form) {
    form.addEventListener('keypress', (e) => {
      if (e.key === 'Enter') {
        e.preventDefault();
        login();
      }
    });
  }
});