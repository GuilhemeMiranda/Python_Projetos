document.addEventListener('DOMContentLoaded', () => {
  // Usuários
  const listaUsuarios = document.getElementById('listaUsuarios');
  const btnCarregarUsuarios = document.getElementById('carregarUsuarios');
  const btnCriarUsuario = document.getElementById('criarUsuario');
  const criarMsg = document.getElementById('criarMsg');

  // Veículos
  const listaVeiculos = document.getElementById('listaVeiculos');
  const btnCarregarVeiculos = document.getElementById('carregarVeiculos');
  const btnCriarVeiculo = document.getElementById('criarVeiculo');
  const criarVeiculoMsg = document.getElementById('criarVeiculoMsg');

  // Manutenções
  const listaManutencoes = document.getElementById('listaManutencoes');
  const btnCarregarManutencoes = document.getElementById('carregarManutencoes');
  const btnCriarManutencao = document.getElementById('criarManutencao');
  const criarManutencaoMsg = document.getElementById('criarManutencaoMsg');

  // ---------- Usuários ----------
  async function carregarUsuarios() {
    listaUsuarios.innerHTML = 'Carregando...';
    try {
      const res = await fetch('/usuarios/');
      const data = await res.json();
      listaUsuarios.innerHTML = '';
      if (!Array.isArray(data) || data.length === 0) {
        listaUsuarios.innerHTML = '<li>(nenhum usuário)</li>';
        return;
      }
      data.forEach(u => {
        const li = document.createElement('li');
        li.textContent = `${u.id} — ${u.nome} <${u.email}>`;
        listaUsuarios.appendChild(li);
      });
    } catch (e) {
      listaUsuarios.innerHTML = '<li>Erro ao carregar usuários</li>';
      console.error(e);
    }
  }

  btnCarregarUsuarios.addEventListener('click', carregarUsuarios);

  btnCriarUsuario.addEventListener('click', async () => {
    criarMsg.textContent = '';
    const nome = document.getElementById('nome').value;
    const email = document.getElementById('email').value;
    const senha = document.getElementById('senha').value;
    try {
      const res = await fetch('/usuarios/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ nome, email, senha })
      });
      if (res.ok) {
        criarMsg.textContent = 'Usuário criado';
        document.getElementById('nome').value = '';
        document.getElementById('email').value = '';
        document.getElementById('senha').value = '';
        carregarUsuarios();
      } else {
        const err = await res.json().catch(()=>({detail:res.statusText}));
        criarMsg.textContent = `Erro: ${err.detail || res.statusText}`;
      }
    } catch (e) {
      criarMsg.textContent = 'Erro de rede';
      console.error(e);
    }
  });

  // ---------- Veículos ----------
  async function carregarVeiculos() {
    listaVeiculos.innerHTML = 'Carregando...';
    try {
      const res = await fetch('/veiculos/');
      const data = await res.json();
      listaVeiculos.innerHTML = '';
      if (!Array.isArray(data) || data.length === 0) {
        listaVeiculos.innerHTML = '<li>(nenhum veículo)</li>';
        return;
      }
      data.forEach(v => {
        const li = document.createElement('li');
        li.textContent = `${v.id} — ${v.placa || '-'} | ${v.marca || '-'} ${v.modelo || '-'} | km:${v.km_atual || '-'} | usuario:${v.usuario_id || '-'}`;
        listaVeiculos.appendChild(li);
      });
    } catch (e) {
      listaVeiculos.innerHTML = '<li>Erro ao carregar veículos</li>';
      console.error(e);
    }
  }

  btnCarregarVeiculos.addEventListener('click', carregarVeiculos);

  btnCriarVeiculo.addEventListener('click', async () => {
    criarVeiculoMsg.textContent = '';
    const placa = document.getElementById('v_placa').value;
    const modelo = document.getElementById('v_modelo').value;
    const marca = document.getElementById('v_marca').value;
    const ano = parseInt(document.getElementById('v_ano').value) || null;
    const km_atual = parseInt(document.getElementById('v_km').value) || 0;
    const usuario_id = parseInt(document.getElementById('v_usuario_id').value) || null;

    try {
      const payload = { placa, modelo, marca, ano, km_atual, usuario_id };
      const res = await fetch('/veiculos/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });
      if (res.ok) {
        criarVeiculoMsg.textContent = 'Veículo criado';
        document.getElementById('v_placa').value = '';
        document.getElementById('v_modelo').value = '';
        document.getElementById('v_marca').value = '';
        document.getElementById('v_ano').value = '';
        document.getElementById('v_km').value = '';
        document.getElementById('v_usuario_id').value = '';
        carregarVeiculos();
      } else {
        const err = await res.json().catch(()=>({detail:res.statusText}));
        criarVeiculoMsg.textContent = `Erro: ${err.detail || res.statusText}`;
      }
    } catch (e) {
      criarVeiculoMsg.textContent = 'Erro de rede';
      console.error(e);
    }
  });

  // ---------- Manutenções ----------
  async function carregarManutencoes() {
    listaManutencoes.innerHTML = 'Carregando...';
    try {
      const res = await fetch('/manutencoes/');
      const data = await res.json();
      listaManutencoes.innerHTML = '';
      if (!Array.isArray(data) || data.length === 0) {
        listaManutencoes.innerHTML = '<li>(nenhuma manutenção)</li>';
        return;
      }
      data.forEach(m => {
        const li = document.createElement('li');
        li.textContent = `${m.id} | veic:${m.veiculo_id} | ${m.data || '-'} | km:${m.km || '-'} | ${m.tipo_manutencao || '-'} | ${m.custo || '-'}`;
        listaManutencoes.appendChild(li);
      });
    } catch (e) {
      listaManutencoes.innerHTML = '<li>Erro ao carregar manutenções</li>';
      console.error(e);
    }
  }

  btnCarregarManutencoes.addEventListener('click', carregarManutencoes);

  btnCriarManutencao.addEventListener('click', async () => {
    criarManutencaoMsg.textContent = '';
    const veiculo_id = parseInt(document.getElementById('m_veiculo_id').value) || null;
    const data = document.getElementById('m_data').value || null;
    const km = parseInt(document.getElementById('m_km').value) || null;
    const tipo_manutencao = document.getElementById('m_tipo').value || '';
    const custo = parseFloat(document.getElementById('m_custo').value) || 0;
    const prestador_servico = document.getElementById('m_prestador').value || '';
    const descricao = document.getElementById('m_descricao').value || '';

    try {
      const payload = { veiculo_id, data, km, tipo_manutencao, descricao, custo, prestador_servico };
      const res = await fetch('/manutencoes/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });
      if (res.ok) {
        criarManutencaoMsg.textContent = 'Manutenção criada';
        document.getElementById('m_veiculo_id').value = '';
        document.getElementById('m_data').value = '';
        document.getElementById('m_km').value = '';
        document.getElementById('m_tipo').value = '';
        document.getElementById('m_custo').value = '';
        document.getElementById('m_prestador').value = '';
        document.getElementById('m_descricao').value = '';
        carregarManutencoes();
      } else {
        const err = await res.json().catch(()=>({detail:res.statusText}));
        criarManutencaoMsg.textContent = `Erro: ${err.detail || res.statusText}`;
      }
    } catch (e) {
      criarManutencaoMsg.textContent = 'Erro de rede';
      console.error(e);
    }
  });

  // carregar listas iniciais
  carregarUsuarios();
  carregarVeiculos();
  carregarManutencoes();
});