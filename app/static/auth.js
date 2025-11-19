document.addEventListener('DOMContentLoaded', () => {
  const btn = document.getElementById('btnLogin');
  const msg = document.getElementById('loginMsg');

  async function login() {
    msg.textContent = '';
    const email = document.getElementById('email').value || '';
    const senha = document.getElementById('senha').value || '';

    try {
      const res = await fetch('/auth/login', {
        method: 'POST',
        credentials: 'same-origin',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, senha })
      });

      if (res.ok) {
        const data = await res.json();
        // Redireciona para o dashboard
        window.location.href = data.redirect || '/ui/dashboard';
        return;
      }

      const err = await res.json().catch(()=>({detail: res.statusText}));
      msg.textContent = `Erro: ${err.detail || res.statusText}`;
    } catch (e) {
      msg.textContent = 'Erro de rede';
      console.error(e);
    }
  }

  if (btn) btn.addEventListener('click', login);
});