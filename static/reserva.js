
// Função para normalizar strings (remover espaços extras e converter para maiúsculas)
function normalizeString(str) {
    return str ? str.trim().toUpperCase() : "";
}

// Função para consultar CEP na API ViaCEP
async function consultarCEP(cep) {
    try {
        const response = await fetch(`https://viacep.com.br/ws/${cep}/json/`);
        const data = await response.json();

        if (data.erro) {
            console.log("CEP não encontrado");
            return null;
        }

        const endereco = {
            cep: normalizeString(data.cep),
            estado: normalizeString(data.uf),
            cidade: normalizeString(data.localidade),
            bairro: normalizeString(data.bairro),
            rua: normalizeString(data.logradouro),
            complemento: normalizeString(data.complemento) || null,
        };

        return endereco;
    } catch (error) {
        console.log(error.message);
        return null;
    }
}

// Função para preencher os campos do formulário com base no CEP
function preencherCampos(form, dados) {
    if (dados) {
        form.querySelector('input[name="adult_estado"]').value = dados.estado;
        form.querySelector('input[name="adult_cidade"]').value = dados.cidade;
        form.querySelector('input[name="adult_bairro"]').value = dados.bairro;
        form.querySelector('input[name="adult_rua"]').value = dados.rua;
    }
}

// Adiciona o event listener para os campos de CEP
document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('input[name^="adult_cep"]').forEach((cepField) => {
        cepField.addEventListener('change', async (event) => {
            const form = event.target.closest('form');
            const cep = event.target.value.replace(/\D/g, ''); // Remove caracteres não numéricos
            if (cep.length === 8) {
                const dados = await consultarCEP(cep);
                preencherCampos(form, dados);
            } else {
                console.log("CEP inválido");
            }
        });
    });
});
