$(document).ready(function() {
	
	//BUSCADOR DE USUARIOS.
	buscar_usuarios();	
	cambiar_criterio_busqueda();
	eliminar_usuario();
	
	// eventos_key();
	cargar_variable();

	// LIMPIAR EL MODAL DE BUSCAR USUARIOS
	// limpiar_modal('#buscar_usuarios');
	limpiar_modal_buscar_usuarios_onshow();

	// AGREGA CLASES SEGUN LA FILA SELECCIONADA
	fila_seleccionada('#tbl-usuarios');
	importar_usuario();

	// FIJA LOS BOOTBOX EN IDIOMA ESPAÑOL
	bootbox.setDefaults({locale: "es",});	

	// CARGA LOS PARAMETROS DEL POST PARA LLAMAR A VENTANA BUSCAR USUARIOS
	llamada_btn_usuario();

});

function limpiar_modal (modal_name) {
	$(modal_name).on('hide.bs.modal',function () {		
		$(modal_name).data('bs.modal', null);
		console.log('SUPUESTAMENTE LIMPIA');
	});	
}

function cambiar_criterio_busqueda () {
	// Cada que entra a la búsqueda desactiva el input
	// document.getElementById("buscar_usuario").disabled = true;

	$(".dropdown-menu").on('click', 'li a', function(){		
		$("#button:first-child").text($(this).text());
		$("#button:first-child").val($(this).text());
		var opcion = $('#button:first-child').text();		
		var input = document.getElementById("buscar_usuario");
		var input_attr = $('#buscar_usuario');
		input.disabled = false;		
		if (opcion == 'Cédula') {			
			input_attr.attr('placeholder','Ingrese un número de cédula.');			
		};
		if (opcion == 'Nombres') {			
			input_attr.attr('placeholder','Ingrese los nombres del usuario.');
		};
		if (opcion == 'Apellidos') {			
			input_attr.attr('placeholder','Ingrese los apellidos del usuario.');			
		};
		if (opcion == 'Opciones.') {
			input.disabled = true;
			input_attr.attr('placeholder','Seleccione un criterio de búsqueda.');			
		};
		document.getElementById('buscar_usuario').value = '';		
	});
}

function asignar_evento(evento){
	var opcion = $('#button:first-child').text();
	var input_attr = $('#buscar_usuario');
	if (opcion != 'Cédula') {
		return evento_letras(evento);
	}else{
		return evento_numeros(evento);
	};
}
    

function consumir_eventos (e) {		
	// Allow: backspace, delete, tab, escape, enter and .	
	if ($.inArray(e.keyCode, [46, 9, 27, 32, 13,110, 16, 190]) !== -1 ||
             // Allow: Ctrl+A
            (e.keyCode == 65 && e.ctrlKey === true) ||
             // Allow: Ctrl+C
            (e.keyCode == 67 && e.ctrlKey === true) ||
             // Allow: Ctrl+X
            (e.keyCode == 88 && e.ctrlKey === true) ||
             // Allow: home, end, left, right
            (e.keyCode >= 35 && e.keyCode <= 39)) {
                 // let it happen, don't do anything
                 console.log('CONSUMIR EVENTOS .. NO LO DEJA PASAR RETURN');
                 return false;
    } 
    return true;
}


function evento_letras(e){ 	
	if ((e.which>=65 && e.which<=90)||(e.which>=97 && e.which<=122) || e.which == 241 || e.which == 209 || e.which == 8 || e.which == 13) {
		// console.log('EVENTO LETRAS .. SI ES LETRA TRUE'+ e.which);
		return true;
	}else{		
		// console.log('EVENTO LETRAS .. SI ES OTRA COSA NO LO DEJA PASAR RETURN');
		return false;
	};	
}

function evento_numeros(e){		
	if (e.which>=48 && e.which<=57 || e.which == 8 || e.which == 13) {
		// console.log('EVENTO NUMEROS .. SI ES NUMERO TRUE'+ e.which);
		return true;
	}else{
		// console.log('EVENTO NUMEROS .. SI ES OTRA COSA NO LO DEJA PASAR RETURN');
		return false;
	};	
}

function validar_criterio(){
	var opcion = $('#button:first-child').text();
	if (opcion == 'Cédula' || opcion == 'Nombres' || opcion == 'Apellidos' ) {		
		return true;
	}else{		
		return false;
	};	
}

function campo_elegido () {
	var opcion = $('#button:first-child').text();	
	if (opcion == 'Cédula') {
		return 'dni'
	};
	if (opcion == 'Nombres') {
		return 'nombres'
	};
	if (opcion == 'Apellidos') {
		return 'apellidos'
	};
	return opcion;	
}


function buscar_usuarios() {	
	$('#buscar_usuario').keyup(function(e){		
		if (validar_criterio()) {			
			if (consumir_eventos(e)) {				
				if(asignar_evento(e)){
					consulta = $("#buscar_usuario").val();
					var columnas = [{ data: 'dni', sortable: true},
									{ data: 'nombres',sortable: true},
									{ data: 'apellidos',sortable: true},
									{ data: 'departamento',sortable: true}];					
					$.ajax({
						data: {'valor': consulta, 'campo': campo_elegido()},
						url: '/usuario/busqueda/',
						type: 'get',
						success : function(data) {				
							configuracion_tabla('#tbl-usuarios', data.usuarios, columnas);
							// $('#tbody-usuarios tr').remove();
							// $.each(data.tabla, function(index, val) {					
							// 	$('#tbody-usuarios').append(val.tabla);
							// });
							inicializar_tabla('#tbl-usuarios');
						},
						error : function(message) {
							console.log(message);
						}						
					});
				}else{
					console.log('Se consume el evento');
					e.stopPropagation();
					e.preventDefault();					
					document.getElementById('buscar_usuario').value = campo;
					return;
				};			
			}else{
				// 
				console.log("Se ejecuta pero no se consume");
				return;
			};
						
		} else{
			console.log('No ha seleccionado un criterio válido');
		};
	});
}

// GUARDA LA VARIABLE DEL INPUT ANTES DE EJECUTAR PARA PODER CONSUMIRLA
var campo = '';
function cargar_variable () {
	$('#buscar_usuario').keydown(function(event) {
		campo = $(this).val();
	});
}

// CONFIGURACIÓN PARA TABLAS DINÁMICAS
function configuracion_tabla (id_tabla, datos, columnas) {
	$(id_tabla).DataTable({
		data: datos,		
		destroy: true,
		columns: columnas,		
		pageLength: 5,
		dom: '<"text-right small"i>t<"small text-center pager"p>',		
		language: {
			"lengthMenu": "Mostrar _MENU_ resultados por página.",
			"zeroRecords": "La búsqueda realizada no generó registros.",
			"info": "Mostrando _PAGE_ de _PAGES_",
			"infoEmpty": "No hay registros disponibles",
			"infoFiltered": "Filtrado de _MAX_ resultados",
			"paginate": {"first": "Primero","last":"Último","next": "Siguiente","previous":"Anterior"},
			"search":"Filtrar:",
			"loadingRecords": "Cargando...",
			"processing":"Procesando...",
        }
    });
}

// variable que muestra la opcion seleccionada
var usuario= null;
function fila_seleccionada (table_name) {	
    $(table_name).on('click', 'tr', function () {
    	if ($(this).hasClass('selected')) {
    		$(this).removeClass('selected');
    		$(this).removeClass('success');
    		$('#btn_importar_usuario').prop('disabled',true);
    		usuario = null;
    	}else{
    		var dni = $('td', this).eq(0).text();
    		usuario = new Object();    		
    		usuario.dni = dni;
    		usuario.nombres = $('td', this).eq(1).text();
    		usuario.apellidos = $('td', this).eq(2).text();
    		$(table_name+' tr').removeClass('success');
    		$(table_name+' tr').removeClass('selected');
    		$(this).toggleClass('success');
    		$(this).toggleClass('selected');
    		$('#btn_importar_usuario').prop('disabled',false);
    	};
    } );
}

// AL CARGAR LOS DATOS DE LA CONSULTA CON KEYUP SE LIMPIA EL OBJETO SELECCIONADO
function inicializar_tabla (table_name) {
	$(table_name+ ' tr').removeClass('selected');
	$(table_name+ ' tr').removeClass('success');
	$('#btn_importar_usuario').prop('disabled',true);
	usuario = null;
}

// IMPORTA EL USUARIO A LA VENTANA QUE LO LLAMÓ
function importar_usuario () {
	$('#btn_importar_usuario').on('click', function(event) {
		var grupo='';		
		if (usuario != null) {
			if (app=='centro_asistencia') {	
				if (tipo_usuario == 'JEFE DEPARTAMENTO') {
					grupo = 'Usuario Administrador.';
				};	
				if (tipo_usuario == 'ASESOR TECNICO') {
					grupo = 'Asesor Técnico.';
				};
				bootbox.confirm({				
					message: "Al usuario <strong>" +usuario.nombres + ' ' +usuario.apellidos+ "</strong> se le asignarán permisos de "+grupo, 
					title: '<h3>¿Realmente desea agregar?</h3>',				
					callback: function(result) {				
						if (result) {
							$.ajax({
								url: '/centro_asistencia/add_usuario',
								type: 'POST',							
								data: {'app': app, 'tipo_usuario': tipo_usuario, 
								'usuario': usuario.dni, 
								'centro_asistencia': centro_asistencia,
								'csrfmiddlewaretoken':csrftoken},							
								dataType: "json",
							})
							.always(function(data) {
								bootbox.alert('<strong>'+data.respuesta+ '</strong>'+data.mensaje, function(){
									location.reload();
								});
							});												
						};
					}
				});
			};
		}else{
			console.log('no se puede importar'+usuario);
		};
	});	
}

// LA AP QUE LLAMA LA VENTANA DE USUARIO
var app = '';
// EL TIPO DE USUARIO PARA AGREGAR EN CENTRO DE ASISTENCIA
var tipo_usuario = '';
var centro_asistencia = '';
var csrftoken = $.cookie('csrftoken');
function llamada_btn_usuario () {
	$('#btn_buscar_usuario_admin').on('click', function(event) {
		tipo_usuario = 'JEFE DEPARTAMENTO';
		app = 'centro_asistencia';
		centro_asistencia = $('#centro_asistencia_pk').val();		
	});

	$('#btn_buscar_usuario_asesor').on('click', function(event) {
		tipo_usuario = 'ASESOR TECNICO';
		app = 'centro_asistencia';
		centro_asistencia = $('#centro_asistencia_pk').val();		
	});
}

function limpiar_modal_buscar_usuarios_onshow () {
	$('#buscar_usuarios').on('shown.bs.modal', function () {		
		var input = document.getElementById("buscar_usuario");
		input.value = '';
		input.disabled = true;
		var input_attr = $('#buscar_usuario');
		input_attr.attr('placeholder','Seleccione un criterio de búsqueda.');		
	});	
}
