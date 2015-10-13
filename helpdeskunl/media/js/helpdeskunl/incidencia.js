$(document).on('ready', my_ready);
	document.write('<script src="/media/js/configure_tables.js" type="text/javascript"></script>');
	document.write('<script src="/media/js/bootstrap.file-input.js" type="text/javascript"></script>');

function my_ready () {
	$('[data-toggle="popover"]').popover();
	configuracion_tabla($('#tbl-incidencias'));	
	configuracion_tabla($('#tbl-incidenciasat'));	
	configuracion_tabla($('#tbl-incidenciasjd'));	
	configuracion_tabla($('#tbl-solicitudes-extension'));	
	configuracion_tabla($('#tbl-solicitudes-reapertura'));	
	
	hacer_visible();
	cambiar_opcion();	
	multiselect_bienes();	
	$('input[type=file]').bootstrapFileInput();
	$('.file-inputs').bootstrapFileInput();

	temporizador();
	// configuracion_tabla($('#example'));
	// $('#tbl-incidencias').dataTable();
	// $('#tbl-incidencias').removeClass( 'display' ).a$('#id').show();ddClass('table table-striped table-bordered');

	// NOTIFICACIONES
	// cargar_notificaciones();
	
	//PARA CALCULAR VIA AJAX EL TIEMPO RESTANTE Y CADUCIDAD DE LA INCIDENCIA
	servicio_onchange();
	prioridad_onchange();
	// PARA BUSCAR BIENES
	buscar_bien();
	eliminar_bien();

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
		// var stack_bottomright = {"dir1":"bottom", "dir2":"right", "push":"top"};
		// new PNotify({
		// 	title: data.tipo,
		// 	text: data.msg,
		// 	addclass: 'stack-bottomright',
		// 	icon: 'glyphicon glyphicon-wrench',
		// 	type: 'info',
		// 	stack: stack_bottomright
		// });
	});
	ishout.init();
}

function temporizador () {	
	// var caduca = new Date($(".caduca").val());	
	// $('.defaultCountdown').countdown({until: caduca, compact: true});	
	$('#tbl-incidenciasat tr .caduca').each(function(){		
		input = $(this);
		id_reloj = input.attr("data-id");
		// console.log("----"+input.val()+"----");
		if (input.val()!="") {
			var caduca = new Date(input.val());
		}else{
			var caduca = new Date();
		};		
		$('#defaultCountdown'+id_reloj).countdown({until: caduca, onExpiry: mensaje, compact: true});	
		// liftOff(id_reloj)
	});
}

function mensaje () {	
	console.log("entrando");
	$.ajax({
		url: '/cerrar_incidencia/',
		type: 'GET',	
		success : function(data) {
			console.log('pasando aqui');
			if (data.realizado) {
				location.reload();				
			};
		},
	});		
}

function liftOff (id_incidencia) {
	console.log("entra aqui");
	$.ajax({
		url: '/cerrar_incidencia/',
		type: 'GET',			
		data: {incidencia: id_incidencia},
		success : function(data) {
			if (data.realizado) {
				// Location.reload();
			};
		},
	});		
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
				// document.getElementById('caduca').value = data.caduca;
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
				// document.getElementById('caduca').value = data.caduca;
				document.getElementById('duracion').value = data.duracion;			
			});
			
		});
	});		
}


///////////////////
// BUSCAR BIENES //
///////////////////

function cambiar_criterio_busqueda () {
	$(".dropdown-menu").on('click', 'li a', function(){		
		$("#button_opciones:first-child").text($(this).text());
		$("#button_opciones:first-child").val($(this).text());
		var opcion = $('#button_opciones:first-child').text();		
		var input = document.getElementById("buscar_bien");
		var input_attr = $('#buscar_bien');
		input.disabled = false;		
		if (opcion == 'Código U.N.L.') {			
			input_attr.attr('placeholder','Ingrese el código institucional.');			
		};
		if (opcion == 'Código S.F.N.') {			
			input_attr.attr('placeholder','Código del Sistema Financiero Nacional.');
		};
		if (opcion == 'Serie') {			
			input_attr.attr('placeholder','Ingrese la serie del bien.');			
		};
		if (opcion == 'Opciones.') {
			input.disabled = true;
			input_attr.attr('placeholder','Seleccione un criterio de búsqueda.');			
		};
		document.getElementById('btn_buscar_bienes').value = '';		
	});
}

function campo_elegido () {
	var opcion = $('#button_opciones:first-child').text();	
	if (opcion == 'Código U.N.L.') {
		return 'codigo'
	};
	if (opcion == 'Código S.F.N.') {
		return 'codigo_cfn'
	};
	if (opcion == 'Serie') {
		return 'serie'
	};
	return opcion;	
}

function validar_criterio(){
	var opcion = $('#button_opciones:first-child').text();
	if (opcion == 'Código U.N.L.' || opcion == 'Código S.F.N.' || opcion == 'Serie' ) {		
		return true;
	}else{		
		return false;
	};	
}

function campo_elegido () {
	var opcion = $('#button_opciones:first-child').text();	
	if (opcion == 'Código U.N.L.') {
		return 'codigo'
	};
	if (opcion == 'Código S.F.N.') {
		return 'codigo_cfn'
	};
	if (opcion == 'Serie') {
		return 'serie'
	};
	return opcion;	
}

function buscar_bien () {	
	$('#btn_buscar_bienes').click(function(event) {		
		if (validar_criterio()) {
			consulta = $("#buscar_bien").val();
			if (consulta != "") {
				$.ajax({
					url: '/bien/busqueda/',
					type: 'GET',					
					data: {'valor': consulta, 'campo': campo_elegido()},
					success : function(data) {
						if (data.bien == "notfound") {
							var permiso = $("#permiso").val();
							if (permiso=="True") {
								bootbox.confirm({			
									message : '¿Desea agregar un nuevo bien?',
									title: '<h3>Recursos no encotrados.</h3>',
									buttons: {
										confirm: {label: 'Nuevo Bien', className: 'btn-primary pull-right'}
									},
									callback: function(result) {
										if (result) {
											// LANZAR EL MODAL PARA CREAR BIEN
										};
									}
								});
							}else{
								bootbox.alert("Recursos no encontrados", function() {});								
							};

							
						}else{
							if(document.getElementById("trbien_"+data.id)==null){
								$('#tbl-bienes tr:last').after(data.fila);
							}else{
								bootbox.alert("Este bien ya está agregado", function() {});
							};							
						};
						
					},
					error : function(message) {
						console.log(message);
					}	 
				});
			}else{
				bootbox.alert("Ingrese algún valor", function() {});
			};
		}else{
			bootbox.alert("No ha seleccionado un criterio válido", function() {
			});
		};
	});
}

function eliminar_bien () {
	// PORQUE CUANDO SE AGREGAN DINAMICAMENTE LOS COMPONENTES NO SE AGREGAN LOS EVENTOS
	$('body').on('click', '.remover', function(e) {
    	var id = $(this).attr("data-id");
		$('#trbien_'+id).remove();
	}); 	
}

