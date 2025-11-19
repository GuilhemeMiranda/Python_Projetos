console.log('manutencao_report.js: arquivo carregado');

document.addEventListener('DOMContentLoaded', () => {
  console.log('manutencao_report.js carregado');

  const tbody = document.querySelector('#manutTable tbody');
  const refreshBtn = document.getElementById('refreshReport');
  const filterInput = document.getElementById('filterVeiculo');
  const applyFilterBtn = document.getElementById('applyFilter');
  const reportMsg = document.getElementById('reportMsg');

  // Elementos do modal
  const modal = document.getElementById('editModal');
  const closeModalBtn = document.getElementById('closeModal');
  const cancelEditBtn = document.getElementById('cancelEdit');
  const saveEditBtn = document.getElementById('saveEdit');
  const editMsg = document.getElementById('editMsg');

  async function carregarRelatorio(placa = '') {
    if (!tbody || !reportMsg) {
      console.error('Elementos de relatório não encontrados');
      return;
    }

    reportMsg.textContent = 'Carregando...';
    tbody.innerHTML = '';

    try {
      const url = placa ? `/manutencoes/?placa=${encodeURIComponent(placa)}` : '/manutencoes/';
      console.log('Buscando:', url);
      
      const res = await fetch(url, { credentials: 'same-origin' });

      if (!res.ok) {
        throw new Error(`Erro ${res.status}: ${res.statusText}`);
      }

      const data = await res.json();
      console.log('Dados recebidos:', data);
      
      if (data.length === 0) {
        reportMsg.textContent = 'Nenhuma manutenção encontrada.';
        return;
      }

      reportMsg.textContent = `${data.length} manutenção(ões) encontrada(s)`;
      
      data.forEach(m => {
        const tr = document.createElement('tr');
        
        const dataFormatada = m.data ? 
          new Date(m.data + 'T00:00:00').toLocaleDateString('pt-BR') : 
          '-';
        
        const custoFormatado = m.custo ? 
          new Intl.NumberFormat('pt-BR', { style: 'currency', currency: 'BRL' }).format(m.custo) : 
          'R$ 0,00';

        tr.innerHTML = `
          <td>${m.id}</td>
          <td>${m.placa}</td>
          <td>${dataFormatada}</td>
          <td>${m.km ? m.km.toLocaleString('pt-BR') : '-'}</td>
          <td>${m.tipo_manutencao || '-'}</td>
          <td>${m.prestador || '-'}</td>
          <td>${custoFormatado}</td>
          <td class="actions-cell">
            <button class="btn btn-sm btn-primary" data-id="${m.id}" data-action="edit">Editar</button>
            <button class="btn btn-sm btn-danger" data-id="${m.id}" data-action="delete">Excluir</button>
          </td>
        `;
        tbody.appendChild(tr);
      });

      // Adiciona eventos aos botões de ação
      document.querySelectorAll('[data-action="edit"]').forEach(btn => {
        btn.addEventListener('click', () => abrirModalEdicao(btn.dataset.id));
      });

      document.querySelectorAll('[data-action="delete"]').forEach(btn => {
        btn.addEventListener('click', () => deletarManutencao(btn.dataset.id));
      });

    } catch (e) {
      tbody.innerHTML = '';
      reportMsg.textContent = `Erro ao carregar manutenções: ${e.message}`;
      console.error('Erro:', e);
    }
  }

  async function abrirModalEdicao(id) {
    console.log('Abrindo modal para edição, ID:', id);
    
    try {
      const res = await fetch(`/manutencoes/${id}`, { credentials: 'same-origin' });
      
      if (!res.ok) {
        throw new Error('Erro ao buscar manutenção');
      }

      const manutencao = await res.json();
      console.log('Manutenção carregada:', manutencao);

      // Preenche o formulário
      document.getElementById('edit_id').value = manutencao.id;
      document.getElementById('edit_placa').value = manutencao.placa;
      document.getElementById('edit_data').value = manutencao.data;
      document.getElementById('edit_km').value = manutencao.km;
      document.getElementById('edit_tipo').value = manutencao.tipo_manutencao;
      document.getElementById('edit_prestador').value = manutencao.prestador;
      document.getElementById('edit_custo').value = manutencao.custo;
      document.getElementById('edit_observacoes').value = manutencao.observacoes || '';

      // Mostra o modal
      modal.style.display = 'block';
      editMsg.textContent = '';
      editMsg.className = 'muted';

    } catch (e) {
      console.error('Erro ao carregar manutenção:', e);
      alert('Erro ao carregar dados da manutenção');
    }
  }

  function fecharModal() {
    modal.style.display = 'none';
    editMsg.textContent = '';
    editMsg.className = 'muted';
  }

  async function salvarEdicao() {
    const id = document.getElementById('edit_id').value;
    const placa = document.getElementById('edit_placa').value.trim();
    const data = document.getElementById('edit_data').value;
    const km = parseInt(document.getElementById('edit_km').value);
    const tipo_manutencao = document.getElementById('edit_tipo').value.trim();
    const prestador = document.getElementById('edit_prestador').value.trim();
    const custo = parseFloat(document.getElementById('edit_custo').value);
    const observacoes = document.getElementById('edit_observacoes').value.trim();

    if (!placa || !data || !km || !tipo_manutencao || !prestador || !custo) {
      editMsg.textContent = 'Preencha todos os campos obrigatórios';
      editMsg.className = 'muted error';
      return;
    }

    if (km <= 0) {
      editMsg.textContent = 'A quilometragem deve ser maior que zero';
      editMsg.className = 'muted error';
      return;
    }

    if (custo <= 0) {
      editMsg.textContent = 'O custo deve ser maior que zero';
      editMsg.className = 'muted error';
      return;
    }

    const payload = {
      placa,
      data,
      km,
      tipo_manutencao,
      prestador,
      custo,
      observacoes: observacoes || null
    };

    console.log('Salvando alterações:', payload);
    editMsg.textContent = 'Salvando...';
    editMsg.className = 'muted';

    try {
      const res = await fetch(`/manutencoes/${id}`, {
        method: 'PUT',
        credentials: 'same-origin',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });

      if (res.ok) {
        editMsg.textContent = 'Manutenção atualizada com sucesso!';
        editMsg.className = 'muted success';
        
        setTimeout(() => {
          fecharModal();
          carregarRelatorio();
        }, 1500);
      } else {
        const err = await res.json();
        editMsg.textContent = `Erro: ${err.detail}`;
        editMsg.className = 'muted error';
      }

    } catch (e) {
      console.error('Erro ao salvar:', e);
      editMsg.textContent = 'Erro ao salvar alterações';
      editMsg.className = 'muted error';
    }
  }

  async function deletarManutencao(id) {
    if (!confirm('Tem certeza que deseja excluir esta manutenção?')) {
      return;
    }

    console.log('Deletando manutenção ID:', id);

    try {
      const res = await fetch(`/manutencoes/${id}`, {
        method: 'DELETE',
        credentials: 'same-origin'
      });

      if (res.status === 204 || res.ok) {
        reportMsg.textContent = 'Manutenção excluída com sucesso!';
        reportMsg.className = 'muted success';
        
        setTimeout(() => {
          reportMsg.textContent = '';
          reportMsg.className = 'muted';
          carregarRelatorio();
        }, 2000);
      } else {
        const err = await res.json().catch(() => ({ detail: 'Erro desconhecido' }));
        reportMsg.textContent = `Erro ao excluir: ${err.detail}`;
        reportMsg.className = 'muted error';
      }

    } catch (e) {
      console.error('Erro ao deletar:', e);
      reportMsg.textContent = 'Erro ao excluir manutenção';
      reportMsg.className = 'muted error';
    }
  }

  // Event Listeners
  if (refreshBtn) {
    refreshBtn.addEventListener('click', () => {
      console.log('Atualizando relatório...');
      carregarRelatorio();
    });
  }

  if (applyFilterBtn) {
    applyFilterBtn.addEventListener('click', () => {
      const placa = filterInput?.value?.trim() || '';
      console.log('Filtrando por placa:', placa);
      carregarRelatorio(placa);
    });
  }

  if (filterInput) {
    filterInput.addEventListener('keypress', (e) => {
      if (e.key === 'Enter') {
        const placa = filterInput.value.trim();
        console.log('Enter pressionado, filtrando:', placa);
        carregarRelatorio(placa);
      }
    });
  }

  if (closeModalBtn) {
    closeModalBtn.addEventListener('click', fecharModal);
  }

  if (cancelEditBtn) {
    cancelEditBtn.addEventListener('click', fecharModal);
  }

  if (saveEditBtn) {
    saveEditBtn.addEventListener('click', salvarEdicao);
  }

  // Fecha modal ao clicar fora
  window.addEventListener('click', (e) => {
    if (e.target === modal) {
      fecharModal();
    }
  });

  // Fecha modal com ESC
  window.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && modal.style.display === 'block') {
      fecharModal();
    }
  });

  // Carrega o relatório ao abrir a página
  console.log('Carregando relatório inicial...');
  carregarRelatorio();
});