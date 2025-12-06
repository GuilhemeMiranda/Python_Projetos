console.log('veiculo_plano.js: arquivo carregado');

document.addEventListener('DOMContentLoaded', () => {
  console.log('✅ veiculo_plano.js: DOM carregado');

  const veiculoSelect = document.getElementById('veiculo_id');
  const planoSelect = document.getElementById('plano_id');
  const proximaDataInput = document.getElementById('proxima_data');
  const proximoKmInput = document.getElementById('proximo_km');
  const btnAssociar = document.getElementById('btnAssociar');
  const formMsg = document.getElementById('formMsg');
  const tbody = document.querySelector('#associacoesTable tbody');
  const listMsg = document.getElementById('listMsg');

  const deleteModal = document.getElementById('deleteModal');
  const closeDeleteModalBtn = document.getElementById('closeDeleteModal');
  const btnCancelarDelete = document.getElementById('btnCancelarDelete');
  const btnConfirmarDelete = document.getElementById('btnConfirmarDelete');
  const deleteMsg = document.getElementById('deleteMsg');

  let associacaoIdParaExcluir = null;

  // Funções auxiliares
  function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) {
      let cookie = parts.pop().split(';').shift();
      return cookie.replace(/^"(.*)"$/, '$1');
    }
    return null;
  }

  function parseCustomToken(token) {
    try {
      if (!token) return null;
      token = token.replace(/^"(.*)"$/, '$1');
      const parts = token.split('.');
      if (parts.length !== 2) return null;
      const payloadBase64 = parts[0];
      const payloadJson = atob(payloadBase64);
      return JSON.parse(payloadJson);
    } catch (error) {
      console.error('Erro ao decodificar token:', error);
      return null;
    }
  }

  async function carregarVeiculos() {
    console.log('📥 Carregando veículos...');
    
    try {
      const token = getCookie('access_token');
      if (!token) {
        veiculoSelect.innerHTML = '<option value="">Faça login novamente</option>';
        return;
      }

      const res = await fetch('/veiculos/', {
        method: 'GET',
        headers: { 'Authorization': `Bearer ${token}` }
      });

      if (!res.ok) throw new Error('Erro ao carregar veículos');

      const veiculos = await res.json();
      console.log('📦 Veículos carregados:', veiculos.length);
      
      veiculoSelect.innerHTML = '<option value="">Selecione um veículo</option>';
      
      if (veiculos.length === 0) {
        veiculoSelect.innerHTML += '<option value="" disabled>Nenhum veículo cadastrado</option>';
        return;
      }

      veiculos.forEach(v => {
        const option = document.createElement('option');
        option.value = v.id;
        option.textContent = `${v.placa} - ${v.marca} ${v.modelo}`;
        veiculoSelect.appendChild(option);
      });

    } catch (e) {
      console.error('❌ Erro ao carregar veículos:', e);
      veiculoSelect.innerHTML = '<option value="">Erro ao carregar veículos</option>';
    }
  }

  async function carregarPlanos() {
    console.log('📥 Carregando planos...');
    
    try {
      const token = getCookie('access_token');
      if (!token) {
        planoSelect.innerHTML = '<option value="">Faça login novamente</option>';
        return;
      }

      const userData = parseCustomToken(token);
      if (!userData || !userData.sub) {
        planoSelect.innerHTML = '<option value="">Token inválido</option>';
        return;
      }

      const res = await fetch(`/planos/?usuario_id=${userData.sub}`, {
        method: 'GET',
        headers: { 'Authorization': `Bearer ${token}` }
      });

      if (!res.ok) throw new Error('Erro ao carregar planos');

      const planos = await res.json();
      console.log('📦 Planos carregados:', planos.length);
      
      planoSelect.innerHTML = '<option value="">Selecione um plano</option>';
      
      if (planos.length === 0) {
        planoSelect.innerHTML += '<option value="" disabled>Nenhum plano cadastrado</option>';
        return;
      }

      planos.forEach(p => {
        const option = document.createElement('option');
        option.value = p.id;
        option.textContent = p.nome;
        planoSelect.appendChild(option);
      });

    } catch (e) {
      console.error('❌ Erro ao carregar planos:', e);
      planoSelect.innerHTML = '<option value="">Erro ao carregar planos</option>';
    }
  }

  async function carregarAssociacoes() {
    console.log('📥 Carregando associações...');
    
    tbody.innerHTML = '<tr><td colspan="5" class="text-center">Carregando...</td></tr>';
    listMsg.textContent = 'Carregando...';
    listMsg.className = 'muted';

    try {
      const token = getCookie('access_token');
      if (!token) {
        tbody.innerHTML = '<tr><td colspan="5" class="text-center error">Não autenticado</td></tr>';
        listMsg.textContent = 'Faça login novamente';
        listMsg.className = 'muted error';
        return;
      }

      const res = await fetch('/veiculos-planos/', {
        method: 'GET',
        headers: { 'Authorization': `Bearer ${token}` }
      });

      if (!res.ok) throw new Error('Erro ao carregar associações');

      const associacoes = await res.json();
      console.log('📦 Associações carregadas:', associacoes.length);
      
      tbody.innerHTML = '';

      if (associacoes.length === 0) {
        tbody.innerHTML = '<tr><td colspan="5" class="text-center">Nenhuma associação encontrada</td></tr>';
        listMsg.textContent = 'Nenhum plano associado aos veículos';
        listMsg.className = 'muted';
        return;
      }

      listMsg.textContent = `${associacoes.length} associação(ões) encontrada(s)`;
      listMsg.className = 'muted success';

      associacoes.forEach(a => {
        const tr = document.createElement('tr');
        
        const dataFormatada = a.proxima_data ? 
          new Date(a.proxima_data + 'T00:00:00').toLocaleDateString('pt-BR') : 
          '-';
        
        const kmFormatado = a.proximo_km ? 
          a.proximo_km.toLocaleString('pt-BR') + ' km' : 
          '-';

        tr.innerHTML = `
          <td>${a.veiculo_placa} (${a.veiculo_modelo})</td>
          <td>${a.plano_nome}</td>
          <td>${dataFormatada}</td>
          <td>${kmFormatado}</td>
          <td class="actions-cell">
            <button class="btn btn-sm btn-danger" data-id="${a.id}">🗑️ Remover</button>
          </td>
        `;
        tbody.appendChild(tr);
      });

      document.querySelectorAll('button[data-id]').forEach(btn => {
        btn.addEventListener('click', () => abrirModalExclusao(btn.dataset.id));
      });

    } catch (e) {
      console.error('❌ Erro ao carregar associações:', e);
      tbody.innerHTML = '<tr><td colspan="5" class="text-center error">Erro ao carregar</td></tr>';
      listMsg.textContent = `Erro: ${e.message}`;
      listMsg.className = 'muted error';
    }
  }

  async function associarPlano() {
    const veiculo_id = veiculoSelect.value;
    const plano_id = planoSelect.value;
    const proxima_data = proximaDataInput.value || null;
    const proximo_km = proximoKmInput.value ? parseInt(proximoKmInput.value) : null;

    if (!veiculo_id || !plano_id) {
      formMsg.textContent = '⚠️ Selecione um veículo e um plano';
      formMsg.className = 'muted error';
      return;
    }

    const payload = { 
      veiculo_id: parseInt(veiculo_id), 
      plano_id: parseInt(plano_id), 
      proxima_data, 
      proximo_km 
    };

    console.log('📤 Enviando associação:', payload);

    formMsg.textContent = 'Associando...';
    formMsg.className = 'muted';

    try {
      const token = getCookie('access_token');
      if (!token) {
        alert('Sessão expirada. Faça login novamente.');
        window.location.href = '/ui/login';
        return;
      }

      const res = await fetch('/veiculos-planos/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify(payload)
      });

      if (res.ok) {
        formMsg.textContent = '✅ Plano associado com sucesso!';
        formMsg.className = 'muted success';
        
        // Limpa o formulário
        veiculoSelect.value = '';
        planoSelect.value = '';
        proximaDataInput.value = '';
        proximoKmInput.value = '';
        
        setTimeout(() => {
          formMsg.textContent = '';
          carregarAssociacoes();
        }, 2000);
      } else {
        const err = await res.json();
        formMsg.textContent = `❌ ${err.detail}`;
        formMsg.className = 'muted error';
      }
    } catch (e) {
      console.error('❌ Erro ao associar:', e);
      formMsg.textContent = '❌ Erro ao associar plano';
      formMsg.className = 'muted error';
    }
  }

  function abrirModalExclusao(id) {
    console.log('🗑️ Abrindo modal exclusão, ID:', id);
    associacaoIdParaExcluir = id;
    deleteModal.style.display = 'block';
    deleteMsg.textContent = '';
    deleteMsg.className = 'muted';
  }

  function fecharModalExclusao() {
    console.log('❌ Fechando modal exclusão');
    deleteModal.style.display = 'none';
    deleteMsg.textContent = '';
    deleteMsg.className = 'muted';
    associacaoIdParaExcluir = null;
  }

  async function confirmarExclusao() {
    if (!associacaoIdParaExcluir) return;

    console.log('🗑️ Confirmando exclusão, ID:', associacaoIdParaExcluir);

    deleteMsg.textContent = 'Removendo...';
    deleteMsg.className = 'muted';

    try {
      const token = getCookie('access_token');
      if (!token) {
        alert('Sessão expirada. Faça login novamente.');
        window.location.href = '/ui/login';
        return;
      }

      const res = await fetch(`/veiculos-planos/${associacaoIdParaExcluir}`, {
        method: 'DELETE',
        headers: { 'Authorization': `Bearer ${token}` }
      });

      if (res.status === 204 || res.ok) {
        deleteMsg.textContent = '✅ Associação removida!';
        deleteMsg.className = 'muted success';
        
        setTimeout(() => {
          fecharModalExclusao();
          carregarAssociacoes();
        }, 1500);
      } else {
        const err = await res.json().catch(() => ({ detail: 'Erro desconhecido' }));
        deleteMsg.textContent = `❌ ${err.detail}`;
        deleteMsg.className = 'muted error';
      }
    } catch (e) {
      console.error('❌ Erro ao remover:', e);
      deleteMsg.textContent = '❌ Erro ao remover associação';
      deleteMsg.className = 'muted error';
    }
  }

  // Event Listeners
  btnAssociar?.addEventListener('click', associarPlano);
  closeDeleteModalBtn?.addEventListener('click', fecharModalExclusao);
  btnCancelarDelete?.addEventListener('click', fecharModalExclusao);
  btnConfirmarDelete?.addEventListener('click', confirmarExclusao);

  window.addEventListener('click', (e) => {
    if (e.target === deleteModal) fecharModalExclusao();
  });

  window.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && deleteModal?.style.display === 'block') {
      fecharModalExclusao();
    }
  });

  // Inicialização
  console.log('🚀 Iniciando carregamento...');
  carregarVeiculos();
  carregarPlanos();
  carregarAssociacoes();
});