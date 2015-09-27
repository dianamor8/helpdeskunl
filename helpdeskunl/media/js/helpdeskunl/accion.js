$(document).on('ready', my_ready);
	document.write('<script src="/media/js/configure_tables.js" type="text/javascript"></script>');
	document.write('<script src="/media/js/bootstrap.file-input.js" type="text/javascript"></script>');

function my_ready () {
	configuracion_tabla($('#tbl-acciones'));	
	configuracion_tabla($('#tbl-recursos'));	
	validar_radio();	
}



function validarForm () {
	$('#tbl-bienes tr .recibido').each(function() {
		if ($(this).data('recibido')=="no") {
			$(this).remove();
		};		
	});
	return true;
}

// function handleClick(cb) {	
// 	// var idcheck = cb.id;
// 	// var check = document.getElementById(idcheck);
// 	// console.log(check);
// 	// var idput = check.data('input');
// 	// var	input = document.getElementById(idput);		

// 	if (cb.checked) {
// 		input.data('recibido', 'si');
// 	}else{		
// 		input.data('recibido', 'no');
// 	};  
// }

function validar_radio () {
	$(".radio").change(function(event) {	
		var idput = $(this).data('input');
		var	input = document.getElementById(idput);		
		if ($(this).is(':checked')) {
			$("#"+idput).data('recibido','si');			
		}else{		
			$("#"+idput).data('recibido','no');			
		};		
	});
}


