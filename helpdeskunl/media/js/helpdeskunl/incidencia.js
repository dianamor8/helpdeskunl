$(document).on('ready', my_ready);
	document.write('<script src="/media/js/configure_tables.js" type="text/javascript"></script>');
	document.write('<script src="/media/js/bootstrap.file-input.js" type="text/javascript"></script>');

function my_ready () {
	$('[data-toggle="popover"]').popover();
	configuracion_tabla($('#tbl-incidencias'));	
	configuracion_tabla($('#tbl-incidenciasat'));	
	configuracion_tabla($('#tbl-incidenciasjd'));	
	hacer_visible();
	cambiar_opcion();	
	multiselect_bienes();	
	// $('input[type=file]').bootstrapFileInput();
	// $('.file-inputs').bootstrapFileInput();

	temporizador();
	// configuracion_tabla($('#example'));
	// $('#tbl-incidencias').dataTable();
	// $('#tbl-incidencias').removeClass( 'display' ).a$('#id').show();ddClass('table table-striped table-bordered');

	// NOTIFICACIONES
	// cargar_notificaciones();
	
	//PARA CALCULAR VIA AJAX EL TIEMPO RESTANTE Y CADUCIDAD DE LA INCIDENCIA
	servicio_onchange();
	prioridad_onchange();

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
	$('#id_tecnicos').multiSelect();
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

function cargar_notificaciones () {
	ishout.on('notificaciones', function(data){
		console.log("NOTIFICA")
		var stack_bottomright = {"dir1":"bottom", "dir2":"right", "push":"top"};
		new PNotify({
			title: data.tipo,
			text: data.msg,
			addclass: 'stack-bottomright',
			icon: 'glyphicon glyphicon-wrench',
			type: 'info',
			stack: stack_bottomright
		});
	});
	ishout.init();
}

function temporizador () {	
	// var caduca = new Date($(".caduca").val());	
	// $('.defaultCountdown').countdown({until: caduca, compact: true});	
	$('#tbl-incidenciasat tr .caduca').each(function(){		
		input = $(this);
		id_reloj = input.attr("data-id");
		var caduca = new Date(input.val());
		$('#defaultCountdown'+id_reloj).countdown({until: caduca, compact: true});	
		// $(this).find('td .caduca').each(function(key,value){
		// 	console.log($(this));			
		// 	if (key == 1) {};
		// })
	})
}


function servicio_onchange () {
	$('#sla').change(function(event) {
		$('#sla option:selected').each(function() {			
			$.ajax({
				url: '/calcularincidencia/',
				type: 'GET',			
				data: {servicio: $(this).val(), p_asignada: $("#p_asignada").val(), incidencia: $("#incidencia_id").val()},
			})			
			.always(function(data) {				
				document.getElementById('caduca').value = data.caduca;
				document.getElementById('duracion').value = data.duracion;			
			});
			
		});
	});		
}

function prioridad_onchange () {
	$('#p_asignada').change(function(event) {
		$('#p_asignada option:selected').each(function() {			
			$.ajax({
				url: '/calcularincidencia/',
				type: 'GET',			
				data: {servicio: $("#sla").val(), p_asignada: $(this).val(), incidencia: $("#incidencia_id").val()},
			})			
			.always(function(data) {				
				document.getElementById('caduca').value = data.caduca;
				document.getElementById('duracion').value = data.duracion;			
			});
			
		});
	});		
}