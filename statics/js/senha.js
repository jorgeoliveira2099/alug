$('#id_password1').keyup(function(){
	var senha = $('#id_password1').val();
	console.log(senha)
	var forca = 0;

	if((senha.length >= 4) && (senha.length <= 7)){
		forca += 10;
	}else if(senha.length > 7){
		forca += 25;
	}

	if((senha.length >= 5) && (senha.match(/[a-z]+/))){
		forca += 10;
	}

	if((senha.length >= 6) && (senha.match(/[A-Z]+/))){
		forca += 20;
	}

	if((senha.length >= 7) && (senha.match(/[@#$%&;*]/))){
		forca += 25;
	}

	if(senha.match(/([1-9]+)\1{1,}/)){
		forca += -25;
	}

	mostrarForca(forca);
});

function mostrarForca(forca){

	if(forca < 30 ){
	    $( "#id_password1" ).focus();
	    $('#div-senha-fraca').removeAttr('hidden');
	    $('#div-senha-media').attr("hidden",true);
	    $('#div-senha-forte').attr("hidden",true);
	    $('#div-senha-excelente').attr("hidden",true);
	    $("#btnCadastro").attr("disabled", true);
	}else if((forca >= 30) && (forca < 50)){
	    $('#div-senha-media').removeAttr('hidden');
        $('#div-senha-fraca').attr("hidden",true);
        $('#div-senha-forte').attr("hidden",true);
	    $('#div-senha-excelente').attr("hidden",true);
	    $("#btnCadastro").attr("disabled", false);
	}else if((forca >= 50) && (forca < 70)){
	    $('#div-senha-forte').removeAttr('hidden');
        $('#div-senha-fraca').attr("hidden",true);
        $('#div-senha-media').attr("hidden",true);
	    $('#div-senha-excelente').attr("hidden",true);
	    $("#btnCadastro").attr("disabled", false);
	}else if((forca >= 70) && (forca < 100)){
	    $('#div-senha-excelente').removeAttr('hidden');
        $('#div-senha-fraca').attr("hidden",true);
        $('#div-senha-forte').attr("hidden",true);
	    $('#div-senha-media').attr("hidden",true);
	    $("#btnCadastro").attr("disabled", false);
	}
}