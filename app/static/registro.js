console.log('registro.js: arquivo carregado');

document.addEventListener('DOMContentLoaded', () => {
  console.log('registro.js: DOM carregado');

  const form = document.getElementById('registroForm');
  const btnRegistrar = document.getElementById('btnRegistrar');
  const btnVoltar = document.getElementById('btnVoltar');
  const msg = document.getElementById('registroMsg');

  // Função para validar email
  function validarEmail(email) {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(email);
  }

  // Função para registrar usuário
  async function registrarUsuario() {
    console.log('Iniciando registro de usuário');
    msg.textContent = '';
    msg.className = 'muted';

    const nome = document.getElementById('nome').value.trim();
    const email = document.getElementById('email').value.trim();
    const senha = document.getElementById('senha').value;
    const confirmarSenha = document.getElementById('confirmarSenha').value;

    // Validações
    if (!nome || !email || !senha || !confirmarSenha) {
      msg.textContent = 'Todos os campos são obrigatórios';
      msg.className = 'muted error';
      return;
    }

    if (!validarEmail(email)) {
      msg.textContent = 'E-mail inválido';
      msg.className = 'muted error';
      return;
    }

    if (senha.length < 6) {
      msg.textContent = 'A senha deve ter no mínimo 6 caracteres';
      msg.className = 'muted error';
      return;
    }

    if (senha !== confirmarSenha) {
      msg.textContent = 'As senhas não coincidem';
      msg.className = 'muted error';
      return;
    }

    const payload = { nome, email, senha };
    console.log('Enviando registro:', { nome, email });

    msg.textContent = 'Cadastrando...';
    msg.className = 'muted';

    try {
      const res = await fetch('/auth/registro', {
        method: 'POST',
        credentials: 'same-origin',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });

      console.log('Status da resposta:', res.status);

      if (res.ok) {
        const data = await res.json();
        console.log('Usuário registrado:', data);
        msg.textContent = 'Cadastro realizado com sucesso! Redirecionando...';
        msg.className = 'muted success';
        
        // Redireciona para login após 2 segundos
        setTimeout(() => {
          window.location.href = '/ui/login';
        }, 2000);
        return;
      }

      const err = await res.json().catch(() => ({ detail: res.statusText }));
      console.error('Erro ao registrar:', err);
      msg.textContent = `Erro: ${err.detail || res.statusText}`;
      msg.className = 'muted error';
    } catch (e) {
      console.error('Erro de rede:', e);
      msg.textContent = 'Erro de conexão com o servidor';
      msg.className = 'muted error';
    }
  }

  // Botão Registrar
  if (btnRegistrar) {
    btnRegistrar.addEventListener('click', registrarUsuario);
  }

  // Botão Voltar
  if (btnVoltar) {
    btnVoltar.addEventListener('click', () => {
      window.location.href = '/ui/login';
    });
  }

  // Enter no formulário
  if (form) {
    form.addEventListener('keypress', (e) => {
      if (e.key === 'Enter') {
        e.preventDefault();
        registrarUsuario();
      }
    });
  }
});