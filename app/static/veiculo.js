console.log('veiculo.js: arquivo carregado');

document.addEventListener('DOMContentLoaded', () => {
  console.log('veiculo.js: DOM carregado');

  const form = document.getElementById('veiculoForm');
  const btnSalvar = document.getElementById('btnSalvar');
  const btnLimpar = document.getElementById('btnLimpar');
  const mensagem = document.getElementById('mensagem');

  console.log('Elementos encontrados:', {
    form: !!form,
    btnSalvar: !!btnSalvar,
    btnLimpar: !!btnLimpar,
    mensagem: !!mensagem
  });

  // Função para limpar o formulário
  function limparFormulario() {
    console.log('Limpando formulário');
    if (form) {
      form.reset();
      if (mensagem) {
        mensagem.textContent = '';
        mensagem.className = 'muted';
      }
    }
  }

  // Função para salvar o veículo
  async function salvarVeiculo(e) {
    console.log('salvarVeiculo: função chamada');
    e.preventDefault();
    
    if (!mensagem) {
      console.error('Elemento mensagem não encontrado');
      return;
    }

    mensagem.textContent = '';
    mensagem.className = 'muted';

    // Coleta os dados do formulário
    const placaEl = document.getElementById('placa');
    const anoEl = document.getElementById('ano');
    const marcaEl = document.getElementById('marca');
    const modeloEl = document.getElementById('modelo');
    const kmEl = document.getElementById('km_atual');

    console.log('Elementos do form:', {
      placa: !!placaEl,
      ano: !!anoEl,
      marca: !!marcaEl,
      modelo: !!modeloEl,
      km: !!kmEl
    });

    if (!placaEl || !anoEl || !marcaEl || !modeloEl || !kmEl) {
      mensagem.textContent = 'Erro: Campos do formulário não encontrados.';
      mensagem.className = 'muted error';
      console.error('Um ou mais campos não foram encontrados');
      return;
    }

    const placa = placaEl.value?.trim();
    const ano = anoEl.value;
    const marca = marcaEl.value?.trim();
    const modelo = modeloEl.value?.trim();
    const km_atual = kmEl.value;

    console.log('Valores coletados:', { placa, ano, marca, modelo, km_atual });

    // Validação básica
    if (!placa || !ano || !marca || !modelo || !km_atual) {
      mensagem.textContent = 'Por favor, preencha todos os campos.';
      mensagem.className = 'muted error';
      console.warn('Validação falhou: campos vazios');
      return;
    }

    // Prepara o payload
    const payload = {
      placa: placa,
      ano: parseInt(ano),
      marca: marca,
      modelo: modelo,
      km_atual: parseInt(km_atual)
    };

    console.log('Enviando payload:', payload);
    mensagem.textContent = 'Salvando...';

    try {
      const response = await fetch('/veiculos/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        credentials: 'same-origin',
        body: JSON.stringify(payload)
      });

      console.log('Status da resposta:', response.status);

      if (response.ok) {
        const data = await response.json();
        console.log('Veículo cadastrado com sucesso:', data);
        mensagem.textContent = 'Veículo cadastrado com sucesso!';
        mensagem.className = 'muted success';
        limparFormulario();
      } else {
        const error = await response.json().catch(() => ({ detail: 'Erro desconhecido' }));
        console.error('Erro ao cadastrar:', error);
        mensagem.textContent = `Erro: ${error.detail || response.statusText}`;
        mensagem.className = 'muted error';
      }
    } catch (error) {
      console.error('Erro de rede:', error);
      mensagem.textContent = 'Erro de conexão com o servidor.';
      mensagem.className = 'muted error';
    }
  }

  // Adiciona eventos aos botões
  if (btnSalvar) {
    console.log('Adicionando listener ao btnSalvar');
    btnSalvar.addEventListener('click', salvarVeiculo);
  } else {
    console.error('btnSalvar não encontrado no DOM');
  }

  if (btnLimpar) {
    console.log('Adicionando listener ao btnLimpar');
    btnLimpar.addEventListener('click', limparFormulario);
  } else {
    console.error('btnLimpar não encontrado no DOM');
  }
});