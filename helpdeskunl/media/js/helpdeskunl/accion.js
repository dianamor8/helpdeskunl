$(document).on('ready', my_ready);
	document.write('<script src="/media/js/configure_tables.js" type="text/javascript"></script>');
	document.write('<script src="/media/js/bootstrap.file-input.js" type="text/javascript"></script>');

function my_ready () {
	configuracion_tabla($('#tbl-acciones'));	
	configuracion_tabla($('#tbl-recursos'));	
	validar_radio();	
	hacer_visible();
	cambiar_opcion();
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


function hacer_visible () {
	var form_padre_nro_doc = ($('#Input_nro_doc').parent('div')).parent('div');
	var form_padre_detalle = ($('#Input_detalle').parent('div')).parent('div');
	var form_padre_observacion = ($('#Input_observacion').parent('div')).parent('div');
	var Input_nro_doc = $('#Input_nro_doc');
	var Input_detalle = $('#Input_detalle');
	var Input_observacion = $('#Input_observacion');

	var opcion_seleccionada = $('#id_conforme_0').is(':checked');
	
	form_padre_nro_doc.attr('id', 'div-hiddenn');
	form_padre_detalle.attr('id', 'div-hiddend');
	form_padre_observacion.attr('id', 'div-hiddeno');

	if (opcion_seleccionada) {		
		$('#div-hiddeno').hide();
		$('#div-hiddenn').show();
		$('#div-hiddend').show();
		$('#Input_detalle').attr('type', 'text');
		$('#Input_nro_doc').attr('type', 'text');
		opcion_detalle = $('#Input_detalle').val();	
		opcion_nro_doc = $('#Input_nro_doc').val();	
	}else{
		$('#div-hiddeno').show();
		$('#div-hiddenn').hide();
		$('#div-hiddend').hide();
		$('#Input_observacion').attr('type', 'text');	
		opcion_observacion = $('#Input_observacion').val();	
	};
}

var opcion_observacion = ''
var opcion_detalle = ''
var opcion_nro_doc = ''


function cambiar_opcion () {
	$('input:radio').change(function(event) {		
		var opcion_seleccionada = $('#id_conforme_0').is(':checked');
		if (opcion_seleccionada) {
			$('#div-hiddeno').hide();
			$('#div-hiddenn').show();
			$('#div-hiddend').show();
			$('#Input_detalle').attr('type', 'text');
			$('#Input_nro_doc').attr('type', 'text');
			$('#Input_observacion').val('');
		}else{
			$('#div-hiddeno').show();
			$('#div-hiddenn').hide();
			$('#div-hiddend').hide();
			$('#Input_observacion').attr('type', 'text');			
			$('#Input_nro_doc').val('');
			$('#Input_detalle').val('');
		};		
	});
}