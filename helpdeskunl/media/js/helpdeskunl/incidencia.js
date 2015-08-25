$(document).on('ready', my_ready);
	document.write('<script src="/media/js/configure_tables.js" type="text/javascript"></script>');
	document.write('<script src="/media/js/bootstrap.file-input.js" type="text/javascript"></script>');

function my_ready () {
	configuracion_tabla($('#tbl-incidencias'));	
	hacer_visible();
	cambiar_opcion();	
	multiselect_bienes();
	$('input[type=file]').bootstrapFileInput();
	$('.file-inputs').bootstrapFileInput();
	// configuracion_tabla($('#example'));
	// $('#tbl-incidencias').dataTable();
	// $('#tbl-incidencias').removeClass( 'display' ).a$('#id').show();ddClass('table table-striped table-bordered');
}

function hacer_visible () {
	var form_padre = ($('#Input_urgencia').parent('div')).parent('div');
	var input_urgencia = $('#Input_urgencia');
	var opcion_seleccionada = $('#id_prioridad_solicitada').val();
	form_padre.attr('id', 'div-hidden');		
	if (opcion_seleccionada=='0' || opcion_seleccionada=='1') {		
		$('#div-hidden').hide();
	}else{
		$('#div-hidden').show();
		$('#Input_urgencia').show();
		$('#Input_urgencia').attr('type', 'text');
		opcion_justificacion = $('#Input_urgencia').val();
	};
}

var opcion_justificacion = ''

function cambiar_opcion () {
	$('#id_prioridad_solicitada').change(function(event) {
		$('#id_prioridad_solicitada option:selected').each(function() {
			if ($( this ).text()=='Bajo' || $( this ).text()=='Normal') {
				$('#Input_urgencia').val('');
				$('#div-hidden').hide();
			};			
			if ($( this ).text()=='Alto') {
				$('#div-hidden').show();
				$('#Input_urgencia').show();
				$('#Input_urgencia').attr('type', 'text');
				$('#Input_urgencia').val(opcion_justificacion);
			};
		});
	});	
}

function multiselect_bienes () {
	$('#id_bienes').multiSelect();
	$('#my-select').multiSelect();
	
	
	
	
}

// function agregar_incidencia () {
// 	$('#incidencia_create_form').submit(function(event) {
// 		var opcion = $('#id_prioridad_solicitada').val();
// 		if (opcion == '2') {

// 		};
// 	});
// }
// jQuery(document).ready(function($) {
// 	$('#tbl-incidencias').dataTable();
// 0979827152

// });