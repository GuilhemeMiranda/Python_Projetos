console.log('veiculo_list.js: arquivo carregado');

document.addEventListener('DOMContentLoaded', () => {
  console.log('veiculo_list.js: DOM carregado');

  const tbody = document.querySelector('#veiculoTable tbody');
  const listMsg = document.getElementById('listMsg');
  const filterInput = document.getElementById('filterPlaca');
  const refreshBtn = document.getElementById('refreshList');
  const applyFilterBtn = document.getElementById('applyFilter');
  const clearFilterBtn = document.getElementById('clearFilter');

  // Modal de edição
  const editModal = document.getElementById('editModal');
  const closeEditModal = document.getElementById('closeEditModal');
  const btnCancelarEdit = document.getElementById('btnCancelarEdit');
  const btnSalvarEdit = document.getElementById('btnSalvarEdit');
  const editMsg = document.getElementById('editMsg');

  // Modal de exclusão
  const deleteModal = document.getElementById('deleteModal');
  const closeDeleteModal = document.getElementById('closeDeleteModal');
  const btnCancelarDelete = document.getElementById('btnCancelarDelete');
  const btnConfirmarDelete = document.getElementById('btnConfirmarDelete');
  const deleteMsg = document.getElementById('deleteMsg');

  console.log('Modais encontrados:', {
    editModal: !!editModal,
    deleteModal: !!deleteModal
  });

  // Garante que os modais começam escondidos
  if (editModal) {
    editModal.style.display = 'none';
    console.log('Modal de edição inicializado como oculto');
  }
  if (deleteModal) {
    deleteModal.style.display = 'none';
    console.log('Modal de exclusão inicializado como oculto');
  }

  let currentDeleteId = null;
  let currentEditData = null;

  // Carregar veículos
  async function carregarVeiculos(placa = '') {
    console.log('carregarVeiculos chamada, placa:', placa);
    
    if (!tbody || !listMsg) {
      console.error('Elementos não encontrados');
      return;
    }

    listMsg.textContent = 'Carregando...';
    tbody.innerHTML = '';

    try {
      const url = placa ? `/veiculos/?placa=${encodeURIComponent(placa)}` : '/veiculos/';
      console.log('Fazendo fetch:', url);
      
      const res = await fetch(url, { credentials: 'same-origin' });

      if (!res.ok) {
        throw new Error(res.statusText);
      }

      const data = await res.json();
      console.log('Veículos recebidos:', data.length);
      
      if (data.length === 0) {
        listMsg.textContent = 'Nenhum veículo encontrado.';
        return;
      }

      listMsg.textContent = `${data.length} veículo(s) encontrado(s)`;
      
      data.forEach((v, index) => {
        console.log(`Criando linha ${index + 1} para veículo ID:`, v.id);
        const tr = document.createElement('tr');
        tr.innerHTML = `
          <td>${v.id}</td>
          <td>${v.placa}</td>
          <td>${v.marca}</td>
          <td>${v.modelo}</td>
          <td>${v.ano}</td>
          <td>${v.km_atual ? v.km_atual.toLocaleString('pt-BR') : '-'}</td>
          <td class="actions-cell">
            <button class="btn btn-small btn-light btn-edit" data-id="${v.id}" type="button">Editar</button>
            <button class="btn btn-small btn-danger btn-delete" data-id="${v.id}" data-placa="${v.placa}" type="button">Excluir</button>
          </td>
        `;
        tbody.appendChild(tr);
      });

      console.log('Linhas criadas, adicionando event listeners...');
      // Adiciona event listeners aos botões
      attachButtonListeners();
      console.log('Event listeners adicionados');

    } catch (e) {
      listMsg.textContent = 'Erro ao carregar veículos.';
      console.error('Erro em carregarVeiculos:', e);
    }
  }

  // Adiciona event listeners aos botões de ação
  function attachButtonListeners() {
    console.log('attachButtonListeners chamada');
    
    // Botões de editar
    const editButtons = document.querySelectorAll('.btn-edit');
    console.log('Botões de editar encontrados:', editButtons.length);
    
    editButtons.forEach((btn, index) => {
      console.log(`Adicionando listener ao botão editar ${index + 1}`);
      btn.addEventListener('click', function(e) {
        console.log('Click no botão editar, event:', e);
        e.preventDefault();
        e.stopPropagation();
        const id = this.getAttribute('data-id');
        console.log('Chamando editarVeiculo com ID:', id);
        editarVeiculo(id);
      });
    });

    // Botões de deletar
    const deleteButtons = document.querySelectorAll('.btn-delete');
    console.log('Botões de deletar encontrados:', deleteButtons.length);
    
    deleteButtons.forEach((btn, index) => {
      console.log(`Adicionando listener ao botão deletar ${index + 1}`);
      btn.addEventListener('click', function(e) {
        console.log('Click no botão deletar, event:', e);
        e.preventDefault();
        e.stopPropagation();
        const id = this.getAttribute('data-id');
        const placa = this.getAttribute('data-placa');
        console.log('Chamando confirmarDelete com ID:', id, 'Placa:', placa);
        confirmarDelete(id, placa);
      });
    });
  }

  // Editar veículo
  async function editarVeiculo(id) {
    console.log('editarVeiculo chamada, ID:', id);
    
    if (!editModal || !editMsg) {
      console.error('Modal de edição não encontrado');
      return;
    }

    editMsg.textContent = 'Carregando dados...';
    editMsg.className = 'muted';

    try {
      const res = await fetch(`/veiculos/${id}`, { credentials: 'same-origin' });
      
      if (!res.ok) {
        throw new Error('Veículo não encontrado');
      }

      const veiculo = await res.json();
      console.log('Dados do veículo carregados:', veiculo);
      currentEditData = veiculo;

      // Preenche o formulário
      document.getElementById('edit_id').value = veiculo.id;
      document.getElementById('edit_placa').value = veiculo.placa;
      document.getElementById('edit_marca').value = veiculo.marca;
      document.getElementById('edit_modelo').value = veiculo.modelo;
      document.getElementById('edit_ano').value = veiculo.ano;
      document.getElementById('edit_km_atual').value = veiculo.km_atual;

      editMsg.textContent = '';
      console.log('Abrindo modal de edição');
      editModal.style.display = 'flex';

    } catch (e) {
      console.error('Erro em editarVeiculo:', e);
      alert('Erro ao carregar dados do veículo.');
    }
  }

  // Salvar edição
  async function salvarEdicao() {
    console.log('salvarEdicao chamada');
    
    if (!editMsg) return;

    editMsg.textContent = '';
    editMsg.className = 'muted';

    const id = document.getElementById('edit_id').value;
    const marca = document.getElementById('edit_marca').value.trim();
    const modelo = document.getElementById('edit_modelo').value.trim();
    const ano = document.getElementById('edit_ano').value;
    const km_atual = document.getElementById('edit_km_atual').value;

    if (!marca || !modelo || !ano || !km_atual) {
      editMsg.textContent = 'Todos os campos são obrigatórios.';
      editMsg.className = 'muted error';
      return;
    }

    const payload = {
      marca,
      modelo,
      ano: parseInt(ano),
      km_atual: parseInt(km_atual)
    };

    console.log('Salvando edição, payload:', payload);
    editMsg.textContent = 'Salvando...';

    try {
      const res = await fetch(`/veiculos/${id}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        credentials: 'same-origin',
        body: JSON.stringify(payload)
      });

      if (res.ok) {
        console.log('Edição salva com sucesso');
        editMsg.textContent = 'Veículo atualizado com sucesso!';
        editMsg.className = 'muted success';
        
        setTimeout(() => {
          fecharModalEdit();
          carregarVeiculos();
        }, 1500);
      } else {
        const error = await res.json().catch(() => ({ detail: 'Erro desconhecido' }));
        console.error('Erro ao salvar:', error);
        editMsg.textContent = `Erro: ${error.detail}`;
        editMsg.className = 'muted error';
      }
    } catch (e) {
      console.error('Erro em salvarEdicao:', e);
      editMsg.textContent = 'Erro de conexão.';
      editMsg.className = 'muted error';
    }
  }

  // Confirmar exclusão
  function confirmarDelete(id, placa) {
    console.log('confirmarDelete chamada, ID:', id, 'Placa:', placa);
    
    if (!deleteModal || !deleteMsg) {
      console.error('Modal de exclusão não encontrado');
      return;
    }

    currentDeleteId = id;
    const deletePlacaEl = document.getElementById('deletePlaca');
    if (deletePlacaEl) {
      deletePlacaEl.textContent = placa;
    }
    deleteMsg.textContent = '';
    deleteMsg.className = 'muted';
    
    console.log('Abrindo modal de exclusão');
    deleteModal.style.display = 'flex';
  }

  // Excluir veículo
  async function excluirVeiculo() {
    console.log('excluirVeiculo chamada, ID:', currentDeleteId);
    
    if (!currentDeleteId || !deleteMsg) return;

    deleteMsg.textContent = 'Excluindo...';
    deleteMsg.className = 'muted';

    try {
      const res = await fetch(`/veiculos/${currentDeleteId}`, {
        method: 'DELETE',
        credentials: 'same-origin'
      });

      if (res.ok || res.status === 204) {
        console.log('Veículo excluído com sucesso');
        deleteMsg.textContent = 'Veículo excluído com sucesso!';
        deleteMsg.className = 'muted success';
        
        setTimeout(() => {
          fecharModalDelete();
          currentDeleteId = null;
          carregarVeiculos();
        }, 1500);
      } else {
        const error = await res.json().catch(() => ({ detail: 'Erro desconhecido' }));
        console.error('Erro ao excluir:', error);
        deleteMsg.textContent = `Erro: ${error.detail}`;
        deleteMsg.className = 'muted error';
      }
    } catch (e) {
      console.error('Erro em excluirVeiculo:', e);
      deleteMsg.textContent = 'Erro de conexão.';
      deleteMsg.className = 'muted error';
    }
  }

  // Fechar modais
  function fecharModalEdit() {
    console.log('Fechando modal de edição');
    if (editModal) {
      editModal.style.display = 'none';
    }
    if (editMsg) {
      editMsg.textContent = '';
      editMsg.className = 'muted';
    }
  }

  function fecharModalDelete() {
    console.log('Fechando modal de exclusão');
    if (deleteModal) {
      deleteModal.style.display = 'none';
    }
    if (deleteMsg) {
      deleteMsg.textContent = '';
      deleteMsg.className = 'muted';
    }
  }

  // Event Listeners
  console.log('Configurando event listeners principais...');

  if (refreshBtn) {
    refreshBtn.addEventListener('click', (e) => {
      e.preventDefault();
      console.log('Botão refresh clicado');
      carregarVeiculos();
    });
  }

  if (applyFilterBtn) {
    applyFilterBtn.addEventListener('click', (e) => {
      e.preventDefault();
      const placa = filterInput.value.trim();
      console.log('Aplicando filtro, placa:', placa);
      carregarVeiculos(placa);
    });
  }

  if (clearFilterBtn) {
    clearFilterBtn.addEventListener('click', (e) => {
      e.preventDefault();
      console.log('Limpando filtro');
      filterInput.value = '';
      carregarVeiculos();
    });
  }

  if (filterInput) {
    filterInput.addEventListener('keypress', (e) => {
      if (e.key === 'Enter') {
        e.preventDefault();
        const placa = filterInput.value.trim();
        console.log('Enter pressionado no filtro, placa:', placa);
        carregarVeiculos(placa);
      }
    });
  }

  // Modal de edição - fechar
  if (closeEditModal) {
    closeEditModal.addEventListener('click', (e) => {
      e.preventDefault();
      console.log('Botão X do modal de edição clicado');
      fecharModalEdit();
    });
  }

  if (btnCancelarEdit) {
    btnCancelarEdit.addEventListener('click', (e) => {
      e.preventDefault();
      console.log('Botão cancelar edição clicado');
      fecharModalEdit();
    });
  }

  if (btnSalvarEdit) {
    btnSalvarEdit.addEventListener('click', (e) => {
      e.preventDefault();
      console.log('Botão salvar edição clicado');
      salvarEdicao();
    });
  }

  // Modal de exclusão - fechar
  if (closeDeleteModal) {
    closeDeleteModal.addEventListener('click', (e) => {
      e.preventDefault();
      console.log('Botão X do modal de exclusão clicado');
      fecharModalDelete();
    });
  }

  if (btnCancelarDelete) {
    btnCancelarDelete.addEventListener('click', (e) => {
      e.preventDefault();
      console.log('Botão cancelar exclusão clicado');
      fecharModalDelete();
    });
  }

  if (btnConfirmarDelete) {
    btnConfirmarDelete.addEventListener('click', (e) => {
      e.preventDefault();
      console.log('Botão confirmar exclusão clicado');
      excluirVeiculo();
    });
  }

  // Fechar modal ao clicar fora
  window.addEventListener('click', (e) => {
    if (e.target === editModal) {
      console.log('Click fora do modal de edição');
      fecharModalEdit();
    }
    if (e.target === deleteModal) {
      console.log('Click fora do modal de exclusão');
      fecharModalDelete();
    }
  });

  // Fechar modais com ESC
  window.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
      if (editModal && editModal.style.display === 'flex') {
        console.log('ESC pressionado, fechando modal de edição');
        fecharModalEdit();
      }
      if (deleteModal && deleteModal.style.display === 'flex') {
        console.log('ESC pressionado, fechando modal de exclusão');
        fecharModalDelete();
      }
    }
  });

  // Carrega ao abrir a página
  console.log('Iniciando carregamento inicial da lista...');
  carregarVeiculos();
});