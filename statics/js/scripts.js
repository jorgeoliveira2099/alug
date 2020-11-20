
$(document).ready(function(){
    $("#id_cpf").mask("999.999.999-99");
});

$('#id_preco').keyup(function(){
    v = $("#id_preco").val()
	v = v.replace(/\D/g,"");  //permite digitar apenas numeros
	v = v.replace(/[0-9]{12}/,"inválido");   //limita pra maximo 999.999.999,99
	v = v.replace(/(\d{1})(\d{8})$/,"$1.$2");  //coloca ponto antes dos ultimos 8 digitos
	v = v.replace(/(\d{1})(\d{5})$/,"$1.$2");  //coloca ponto antes dos ultimos 5 digitos
	v = v.replace(/(\d{1})(\d{1,2})$/,"$1,$2");        //coloca virgula antes dos ultimos 2 digitos

	$("#id_preco").val(v)
});

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

$('#id_fim').blur(function(){
    var dataInicial = $('#id_inicio').val();
    var dataFinal = $('#id_fim').val();
    console.log(dataInicial)
    console.log(dataFinal)

    if (dataInicial != '' && dataFinal != '') {
        let date1 = new Date(dataInicial);
        let date2 = new Date(dataFinal);
        if (date1 <= date2) {
            $("#btnSalvar").attr("disabled", false);
        }
        else {
            alert('A data de inicio do aluguel deve ser menor ou igual a data final!')
            $("#btnSalvar").attr("disabled", true);
        }
    }
});

$('#id_inicio').blur(function(){
    var dataInicial = $('#id_inicio').val();
    var dataFinal = $('#id_fim').val();
    console.log(dataInicial)
    console.log(dataFinal)

    if (dataInicial != '' && dataFinal != '') {
        let date1 = new Date(dataInicial);
        let date2 = new Date(dataFinal);
        if (date1 <= date2) {
            $("#btnSalvar").attr("disabled", false);
        }
        else {
            alert('A data de inicio do aluguel deve ser menor ou igual a data final!')
            $("#btnSalvar").attr("disabled", true);
        }
    }
});



function prenecherExclusao(idProduto){
    var a = $('#modal-exlusao').find('a')
    var link = a.attr('href')
    link = link.slice(0, -1)
    link = link.slice(0, -1)
    link = link + idProduto + '/'
    console.log(link)
    a.attr('href', link)
}

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


