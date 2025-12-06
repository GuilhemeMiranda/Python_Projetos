console.log('plano_list.js: arquivo carregado');

document.addEventListener('DOMContentLoaded', () => {
  console.log('plano_list.js: DOM carregado');

  const tbody = document.querySelector('#planosTable tbody');
  const refreshBtn = document.getElementById('refreshReport');
  const filterInput = document.getElementById('filterNome');
  const applyFilterBtn = document.getElementById('applyFilter');
  const clearFilterBtn = document.getElementById('clearFilter');
  const reportMsg = document.getElementById('reportMsg');

  console.log('Elementos encontrados:', {
    tbody: !!tbody,
    refreshBtn: !!refreshBtn,
    filterInput: !!filterInput,
    applyFilterBtn: !!applyFilterBtn,
    clearFilterBtn: !!clearFilterBtn,
    reportMsg: !!reportMsg
  });

  // Elementos do modal de edição
  const editModal = document.getElementById('editModal');
  const closeModalBtn = document.getElementById('closeModal');
  const cancelEditBtn = document.getElementById('cancelEdit');
  const saveEditBtn = document.getElementById('saveEdit');
  const editMsg = document.getElementById('editMsg');

  console.log('Elementos modal edição:', {
    editModal: !!editModal,
    closeModalBtn: !!closeModalBtn,
    cancelEditBtn: !!cancelEditBtn,
    saveEditBtn: !!saveEditBtn,
    editMsg: !!editMsg
  });

  // Elementos do modal de exclusão
  const deleteModal = document.getElementById('deleteModal');
  const closeDeleteModalBtn = document.getElementById('closeDeleteModal');
  const btnCancelarDelete = document.getElementById('btnCancelarDelete');
  const btnConfirmarDelete = document.getElementById('btnConfirmarDelete');
  const deleteMsg = document.getElementById('deleteMsg');

  console.log('Elementos modal exclusão:', {
    deleteModal: !!deleteModal,
    closeDeleteModalBtn: !!closeDeleteModalBtn,
    btnCancelarDelete: !!btnCancelarDelete,
    btnConfirmarDelete: !!btnConfirmarDelete,
    deleteMsg: !!deleteMsg
  });

  let planoIdParaExcluir = null;

  // Funções auxiliares para token
  function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) {
      let cookie = parts.pop().split(';').shift();
      cookie = cookie.replace(/^"(.*)"$/, '$1');
      return cookie;
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
      const payload = JSON.parse(payloadJson);
      return payload;
    } catch (error) {
      console.error('Erro ao decodificar token:', error);
      return null;
    }
  }

  async function carregarPlanos(filtroNome = '') {
    console.log('carregarPlanos chamado, filtro:', filtroNome);

    if (!tbody) {
      console.error('❌ tbody não encontrado!');
      return;
    }

    if (!reportMsg) {
      console.error('❌ reportMsg não encontrado!');
      return;
    }

    reportMsg.textContent = 'Carregando...';
    reportMsg.className = 'muted';
    tbody.innerHTML = '<tr><td colspan="6" class="text-center">Carregando...</td></tr>';

    try {
      const token = getCookie('access_token');
      
      if (!token) {
        reportMsg.textContent = '❌ Você não está autenticado. Faça login novamente.';
        reportMsg.className = 'muted error';
        setTimeout(() => {
          window.location.href = '/ui/login';
        }, 2000);
        return;
      }

      const userData = parseCustomToken(token);
      
      if (!userData || !userData.sub) {
        reportMsg.textContent = '❌ Token inválido. Faça login novamente.';
        reportMsg.className = 'muted error';
        setTimeout(() => {
          window.location.href = '/ui/login';
        }, 2000);
        return;
      }

      const usuarioId = userData.sub;
      const url = `/planos/?usuario_id=${usuarioId}`;
      console.log('Buscando:', url);
      
      const res = await fetch(url, {
        method: 'GET',
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });

      if (!res.ok) {
        throw new Error(`Erro ${res.status}: ${res.statusText}`);
      }

      let data = await res.json();
      console.log('Dados recebidos:', data);
      
      // Aplica filtro por nome
      if (filtroNome) {
        data = data.filter(p => 
          p.nome.toLowerCase().includes(filtroNome.toLowerCase())
        );
      }

      tbody.innerHTML = '';

      if (data.length === 0) {
        reportMsg.textContent = filtroNome ? 
          'Nenhum plano encontrado com esse nome.' : 
          'Nenhum plano cadastrado.';
        reportMsg.className = 'muted';
        tbody.innerHTML = '<tr><td colspan="6" class="text-center">Nenhum plano encontrado</td></tr>';
        return;
      }

      reportMsg.textContent = `${data.length} plano(s) encontrado(s)`;
      reportMsg.className = 'muted success';
      
      data.forEach(plano => {
        const tr = document.createElement('tr');
        
        const kmFormatado = plano.km_intervalo ? 
          `${plano.km_intervalo.toLocaleString('pt-BR')} km` : 
          '-';
        
        const diasFormatado = plano.dias_intervalo ? 
          `${plano.dias_intervalo} dias` : 
          '-';

        tr.innerHTML = `
          <td>${plano.id}</td>
          <td>${plano.nome}</td>
          <td>${plano.descricao || '-'}</td>
          <td>${kmFormatado}</td>
          <td>${diasFormatado}</td>
          <td class="actions-cell">
            <button class="btn btn-sm btn-primary" data-id="${plano.id}" data-action="edit">✏️ Editar</button>
            <button class="btn btn-sm btn-danger" data-id="${plano.id}" data-action="delete">🗑️ Excluir</button>
          </td>
        `;
        tbody.appendChild(tr);
      });

      // Adiciona eventos aos botões de ação
      document.querySelectorAll('[data-action="edit"]').forEach(btn => {
        btn.addEventListener('click', () => abrirModalEdicao(btn.dataset.id));
      });

      document.querySelectorAll('[data-action="delete"]').forEach(btn => {
        btn.addEventListener('click', () => abrirModalExclusao(btn.dataset.id));
      });

    } catch (e) {
      tbody.innerHTML = '<tr><td colspan="6" class="text-center error">Erro ao carregar</td></tr>';
      reportMsg.textContent = `Erro ao carregar planos: ${e.message}`;
      reportMsg.className = 'muted error';
      console.error('Erro:', e);
    }
  }

  async function abrirModalEdicao(id) {
    console.log('Abrindo modal para edição, ID:', id);
    
    if (!editModal) {
      console.error('❌ editModal não encontrado!');
      return;
    }

    try {
      const token = getCookie('access_token');
      
      if (!token) {
        alert('Sessão expirada. Faça login novamente.');
        window.location.href = '/ui/login';
        return;
      }

      const res = await fetch(`/planos/${id}`, {
        method: 'GET',
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      
      if (!res.ok) {
        throw new Error('Erro ao buscar plano');
      }

      const plano = await res.json();
      console.log('Plano carregado:', plano);

      // Preenche o formulário
      document.getElementById('edit_id').value = plano.id;
      document.getElementById('edit_nome').value = plano.nome;
      document.getElementById('edit_descricao').value = plano.descricao || '';
      document.getElementById('edit_km_intervalo').value = plano.km_intervalo || '';
      document.getElementById('edit_dias_intervalo').value = plano.dias_intervalo || '';

      // Mostra o modal
      editModal.style.display = 'block';
      if (editMsg) {
        editMsg.textContent = '';
        editMsg.className = 'muted';
      }

    } catch (e) {
      console.error('Erro ao carregar plano:', e);
      alert('Erro ao carregar dados do plano');
    }
  }

  function fecharModalEdicao() {
    if (editModal) {
      editModal.style.display = 'none';
    }
    if (editMsg) {
      editMsg.textContent = '';
      editMsg.className = 'muted';
    }
  }

  async function salvarEdicao() {
    const id = document.getElementById('edit_id').value;
    const nome = document.getElementById('edit_nome').value.trim();
    const descricao = document.getElementById('edit_descricao').value.trim();
    const km_intervalo = document.getElementById('edit_km_intervalo').value;
    const dias_intervalo = document.getElementById('edit_dias_intervalo').value;

    if (!editMsg) return;

    // Validações
    if (!nome || nome.length < 3) {
      editMsg.textContent = '⚠️ O nome deve ter pelo menos 3 caracteres';
      editMsg.className = 'muted error';
      return;
    }

    if (!km_intervalo && !dias_intervalo) {
      editMsg.textContent = '⚠️ Informe pelo menos um intervalo (KM ou Dias)';
      editMsg.className = 'muted error';
      return;
    }

    const payload = {
      nome: nome,
      descricao: descricao || null,
      km_intervalo: km_intervalo ? parseInt(km_intervalo) : null,
      dias_intervalo: dias_intervalo ? parseInt(dias_intervalo) : null
    };

    console.log('Salvando alterações:', payload);
    editMsg.textContent = 'Salvando...';
    editMsg.className = 'muted';

    try {
      const token = getCookie('access_token');
      
      if (!token) {
        alert('Sessão expirada. Faça login novamente.');
        window.location.href = '/ui/login';
        return;
      }

      const res = await fetch(`/planos/${id}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify(payload)
      });

      if (res.ok) {
        editMsg.textContent = '✅ Plano atualizado com sucesso!';
        editMsg.className = 'muted success';
        
        setTimeout(() => {
          fecharModalEdicao();
          carregarPlanos();
        }, 1500);
      } else {
        const err = await res.json();
        editMsg.textContent = `❌ Erro: ${err.detail}`;
        editMsg.className = 'muted error';
      }

    } catch (e) {
      console.error('Erro ao salvar:', e);
      editMsg.textContent = '❌ Erro ao salvar alterações';
      editMsg.className = 'muted error';
    }
  }

  function abrirModalExclusao(id) {
    if (!deleteModal) {
      console.error('❌ deleteModal não encontrado!');
      return;
    }

    planoIdParaExcluir = id;
    deleteModal.style.display = 'block';
    if (deleteMsg) {
      deleteMsg.textContent = '';
      deleteMsg.className = 'muted';
    }
  }

  function fecharModalExclusao() {
    if (deleteModal) {
      deleteModal.style.display = 'none';
    }
    if (deleteMsg) {
      deleteMsg.textContent = '';
      deleteMsg.className = 'muted';
    }
    planoIdParaExcluir = null;
  }

  async function confirmarExclusao() {
    if (!planoIdParaExcluir) return;
    if (!deleteMsg) return;

    console.log('Deletando plano ID:', planoIdParaExcluir);
    deleteMsg.textContent = 'Excluindo...';
    deleteMsg.className = 'muted';

    try {
      const token = getCookie('access_token');
      
      if (!token) {
        alert('Sessão expirada. Faça login novamente.');
        window.location.href = '/ui/login';
        return;
      }

      const res = await fetch(`/planos/${planoIdParaExcluir}`, {
        method: 'DELETE',
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });

      if (res.status === 204 || res.ok) {
        deleteMsg.textContent = '✅ Plano excluído com sucesso!';
        deleteMsg.className = 'muted success';
        
        setTimeout(() => {
          fecharModalExclusao();
          carregarPlanos();
        }, 1500);
      } else {
        const err = await res.json().catch(() => ({ detail: 'Erro desconhecido' }));
        deleteMsg.textContent = `❌ Erro ao excluir: ${err.detail}`;
        deleteMsg.className = 'muted error';
      }

    } catch (e) {
      console.error('Erro ao deletar:', e);
      deleteMsg.textContent = '❌ Erro ao excluir plano';
      deleteMsg.className = 'muted error';
    }
  }

  // Event Listeners (com verificação de null)
  if (refreshBtn) {
    refreshBtn.addEventListener('click', () => {
      console.log('Atualizando lista...');
      carregarPlanos();
    });
  }

  if (applyFilterBtn) {
    applyFilterBtn.addEventListener('click', () => {
      const nome = filterInput?.value?.trim() || '';
      console.log('Filtrando por nome:', nome);
      carregarPlanos(nome);
    });
  }

  if (clearFilterBtn) {
    clearFilterBtn.addEventListener('click', () => {
      if (filterInput) {
        filterInput.value = '';
      }
      console.log('Limpando filtro...');
      carregarPlanos();
    });
  }

  if (filterInput) {
    filterInput.addEventListener('keypress', (e) => {
      if (e.key === 'Enter') {
        const nome = filterInput.value.trim();
        console.log('Enter pressionado, filtrando:', nome);
        carregarPlanos(nome);
      }
    });
  }

  // Modal de edição
  if (closeModalBtn) {
    closeModalBtn.addEventListener('click', fecharModalEdicao);
  }

  if (cancelEditBtn) {
    cancelEditBtn.addEventListener('click', fecharModalEdicao);
  }

  if (saveEditBtn) {
    saveEditBtn.addEventListener('click', salvarEdicao);
  }

  // Modal de exclusão
  if (closeDeleteModalBtn) {
    closeDeleteModalBtn.addEventListener('click', fecharModalExclusao);
  }

  if (btnCancelarDelete) {
    btnCancelarDelete.addEventListener('click', fecharModalExclusao);
  }

  if (btnConfirmarDelete) {
    btnConfirmarDelete.addEventListener('click', confirmarExclusao);
  }

  // Fecha modal ao clicar fora
  window.addEventListener('click', (e) => {
    if (editModal && e.target === editModal) {
      fecharModalEdicao();
    }
    if (deleteModal && e.target === deleteModal) {
      fecharModalExclusao();
    }
  });

  // Fecha modal com ESC
  window.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
      if (editModal && editModal.style.display === 'block') {
        fecharModalEdicao();
      }
      if (deleteModal && deleteModal.style.display === 'block') {
        fecharModalExclusao();
      }
    }
  });

  // Carrega a lista ao abrir a página
  console.log('Carregando lista inicial...');
  carregarPlanos();
});