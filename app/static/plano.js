(function() {
  console.log("🚀 Script plano.js carregado!");
  
  const form = document.getElementById('planoForm');
  const btnSalvar = document.getElementById('btnSalvar');
  const btnLimpar = document.getElementById('btnLimpar');
  const mensagem = document.getElementById('mensagem');

  // Limpar formulário
  btnLimpar.addEventListener('click', () => {
    form.reset();
    mensagem.textContent = '';
    mensagem.className = 'muted';
  });

  // Salvar plano
  btnSalvar.addEventListener('click', async () => {
    const nome = document.getElementById('nome').value.trim();
    const descricao = document.getElementById('descricao').value.trim() || null;
    const km_intervalo = document.getElementById('km_intervalo').value;
    const dias_intervalo = document.getElementById('dias_intervalo').value;

    // Validações
    if (!km_intervalo && !dias_intervalo) {
      mensagem.textContent = '⚠️ Informe pelo menos um intervalo (KM ou Dias)';
      mensagem.className = 'muted error';
      return;
    }

    if (!nome || nome.length < 3) {
      mensagem.textContent = '⚠️ O nome deve ter pelo menos 3 caracteres';
      mensagem.className = 'muted error';
      return;
    }

    const planoData = {
      nome: nome,
      descricao: descricao,
      km_intervalo: km_intervalo ? parseInt(km_intervalo) : null,
      dias_intervalo: dias_intervalo ? parseInt(dias_intervalo) : null
    };

    try {
      const token = getCookie('access_token');
      
      if (!token) {
        mensagem.textContent = '❌ Você não está autenticado. Faça login novamente.';
        mensagem.className = 'muted error';
        setTimeout(() => {
          window.location.href = '/ui/login';
        }, 2000);
        return;
      }

      const userData = parseCustomToken(token);
      
      if (!userData || !userData.sub) {
        mensagem.textContent = '❌ Token inválido. Faça login novamente.';
        mensagem.className = 'muted error';
        setTimeout(() => {
          window.location.href = '/ui/login';
        }, 2000);
        return;
      }

      const usuarioId = userData.sub;
      const url = `/planos/?usuario_id=${usuarioId}`;

      const response = await fetch(url, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify(planoData)
      });

      if (response.ok) {
        mensagem.textContent = '✅ Plano cadastrado com sucesso!';
        mensagem.className = 'muted success';
        form.reset();
        
        setTimeout(() => {
          window.location.href = '/ui/planos';
        }, 1500);
      } else {
        const error = await response.json();
        mensagem.textContent = `❌ Erro: ${error.detail || 'Não foi possível cadastrar'}`;
        mensagem.className = 'muted error';
      }
    } catch (error) {
      console.error('Erro:', error);
      mensagem.textContent = `❌ Erro de conexão: ${error.message}`;
      mensagem.className = 'muted error';
    }
  });

  // Função para obter cookie
  function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) {
      let cookie = parts.pop().split(';').shift();
      // Remove aspas duplas se existirem
      cookie = cookie.replace(/^"(.*)"$/, '$1');
      return cookie;
    }
    return null;
  }

  // Função para decodificar token customizado (base64.signature)
  function parseCustomToken(token) {
    try {
      if (!token) return null;
      
      // Remove aspas duplas se existirem
      token = token.replace(/^"(.*)"$/, '$1');
      
      // Token customizado: payload_base64.signature
      const parts = token.split('.');
      if (parts.length !== 2) return null;
      
      // Decodifica payload (primeira parte)
      const payloadBase64 = parts[0];
      const payloadJson = atob(payloadBase64);
      const payload = JSON.parse(payloadJson);
      
      return payload;
    } catch (error) {
      console.error('Erro ao decodificar token:', error);
      return null;
    }
  }
})();