	//Mascara de CPF
	$(document).ready(function(){
		$("#id_cpf").mask("999.999.999-99");
	});

	//Mascara de CEP
	$(document).ready(function(){
	$("#id_cep").mask("99.999-999");
    });

    //Executa a requisição quando o campo username perder o foco
    $('#id_cpf').blur(function(){
        var cpf = $('#id_cpf').val().replace(/[^0-9]/g, '').toString();
        var cpfValido = true
        if (cpf != "")
            cpfValido = validaCpf(cpf);
        if (cpfValido) {
            $("#btnSalvar").attr("disabled", false);
        }
        else {
            alert('CPF invalido!')
            $("#btnSalvar").attr("disabled", true);
        }
    });

function validaCpf(strCPF) {
    var Soma;
    var Resto;
    Soma = 0;
  if (strCPF == "00000000000") return false;


  for (i=1; i<=9; i++) Soma = Soma + parseInt(strCPF.substring(i-1, i)) * (11 - i);
  Resto = (Soma * 10) % 11;

    if ((Resto == 10) || (Resto == 11))  Resto = 0;
    if (Resto != parseInt(strCPF.substring(9, 10)) ) return false;

  Soma = 0;
    for (i = 1; i <= 10; i++) Soma = Soma + parseInt(strCPF.substring(i-1, i)) * (12 - i);
    Resto = (Soma * 10) % 11;

    if ((Resto == 10) || (Resto == 11))  Resto = 0;
    if (Resto != parseInt(strCPF.substring(10, 11) ) ) return false;
    return true;
}

$('#id_cep').blur(function(){
   var cep = $('#id_cep').val()
   pesquisacep(cep)
});

function limpa_formulário_cep() {
    //Limpa valores do formulário de cep.
    document.getElementById('id_rua').value=("");
    document.getElementById('id_bairro').value=("");
    document.getElementById('id_cidade').value=("");
    document.getElementById('id_estado').value=("");
}

function meu_callback(conteudo) {
    if (!("erro" in conteudo)) {
        //Atualiza os campos com os valores.
        document.getElementById('id_rua').value=(conteudo.logradouro);
        document.getElementById('id_bairro').value=(conteudo.bairro);
        document.getElementById('id_cidade').value=(conteudo.localidade);
        document.getElementById('id_estado').value=(conteudo.uf);
    }
    else {
        //CEP não Encontrado.
        limpa_formulário_cep();
        alert("CEP não encontrado.");
        }
    }

function pesquisacep(valor) {

    //Nova variável "cep" somente com dígitos.
    var cep = valor.replace(/\D/g, '');

    //Verifica se campo cep possui valor informado.
    if (cep != "") {

        //Expressão regular para validar o CEP.
        var validacep = /^[0-9]{8}$/;

        //Valida o formato do CEP.
        if(validacep.test(cep)) {

            //Preenche os campos com "..." enquanto consulta webservice.
            document.getElementById('id_rua').value="...";
            document.getElementById('id_bairro').value="...";
            document.getElementById('id_cidade').value="...";
            document.getElementById('id_estado').value="...";

            //Cria um elemento javascript.
            var script = document.createElement('script');

            //Sincroniza com o callback.
            script.src = 'https://viacep.com.br/ws/'+ cep + '/json/?callback=meu_callback';

            //Insere script no documento e carrega o conteúdo.
            document.body.appendChild(script);

        }
        else {
            //cep é inválido.
            limpa_formulário_cep();
            alert("Formato de CEP inválido.");
        }
    }
    else {
        //cep sem valor, limpa formulário.
        limpa_formulário_cep();
    }
}
