document.addEventListener('DOMContentLoaded', () => {
  console.log('manutencao.js carregado');

  // Elementos do formulário
  const salvarBtn = document.getElementById('salvarManut');
  const limparBtn = document.getElementById('limparManut');
  const msg = document.getElementById('manutMsg');

  // Relatório
  const tbody = document.querySelector('#manutTable tbody');
  const refreshBtn = document.getElementById('refreshReport');
  const filterInput = document.getElementById('filterVeiculo');
  const applyFilterBtn = document.getElementById('applyFilter');
  const reportMsg = document.getElementById('reportMsg');

  async function postarManutencao() {
    msg.textContent = '';
    const veiculo_id = parseInt(document.getElementById('m_veiculo_id')?.value) || null;
    const data = document.getElementById('m_data')?.value || null;
    const km = parseInt(document.getElementById('m_km')?.value) || null;
    const tipo_manutencao = document.getElementById('m_tipo')?.value || '';
    const custo = parseFloat(document.getElementById('m_custo')?.value) || 0;
    const prestador_servico = document.getElementById('m_prestador')?.value || '';
    const descricao = document.getElementById('m_descricao')?.value || '';

    const payload = { veiculo_id, data, km, tipo_manutencao, descricao, custo, prestador_servico };
    try {
      const res = await fetch('/manutencoes/', {
        method: 'POST',
        headers: {'Content-Type':'application/json'},
        body: JSON.stringify(payload)
      });
      if (res.ok) {
        msg.textContent = 'Manutenção registrada com sucesso';
        limparFormulario();
      } else {
        const err = await res.json().catch(()=>({detail:res.statusText}));
        msg.textContent = `Erro: ${err.detail || res.statusText}`;
      }
    } catch (e) {
      msg.textContent = 'Erro de rede ao salvar';
      console.error(e);
    }
  }

  function limparFormulario() {
    ['m_veiculo_id','m_data','m_km','m_tipo','m_custo','m_prestador','m_descricao'].forEach(id => {
      const el = document.getElementById(id);
      if (el) el.value = '';
    });
    msg.textContent = '';
  }

  async function carregarRelatorio(placa = '') {
    reportMsg.textContent = 'Carregando...';
    tbody.innerHTML = '';

    try {
      const url = placa ? `/manutencoes/?placa=${encodeURIComponent(placa)}` : '/manutencoes/';
      const res = await fetch(url, {
        credentials: 'same-origin'
      });

      if (!res.ok) {
        throw new Error(res.statusText);
      }

      const data = await res.json();
      
      if (data.length === 0) {
        reportMsg.textContent = 'Nenhuma manutenção encontrada.';
        return;
      }

      reportMsg.textContent = '';
      data.forEach(m => {
        const tr = document.createElement('tr');
        tr.innerHTML = `
          <td>${m.id}</td>
          <td>${m.placa}</td>
          <td>${m.data}</td>
          <td>${m.km}</td>
          <td>${m.tipo}</td>
          <td>${m.prestador || '-'}</td>
          <td>R$ ${m.custo ? m.custo.toFixed(2) : '0.00'}</td>
        `;
        tbody.appendChild(tr);
      });

    } catch (e) {
      tbody.innerHTML = '';
      reportMsg.textContent = 'Erro ao carregar manutenções.';
      console.error(e);
    }
  }

  if (salvarBtn) salvarBtn.addEventListener('click', postarManutencao);
  if (limparBtn) limparBtn.addEventListener('click', limparFormulario);
  if (refreshBtn) {
    refreshBtn.addEventListener('click', () => carregarRelatorio());
  }

  if (applyFilterBtn) {
    applyFilterBtn.addEventListener('click', () => {
      const placa = filterInput.value.trim();
      carregarRelatorio(placa);
    });
  }

  // Carrega ao abrir a página
  carregarRelatorio();
});