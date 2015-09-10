$(document).ready(function() {
	// FORMULARIOS
	// -----centro_asistencia_add($('#add_centro_asistencia_form'),'#centro_asistencia_modal', '/centro_asistencia/add');
	// clear_data_modal('#centro_asistencia_modal');

	// CARGAR DATA-
	modalDatosEliminar('.delete');
});

// function clear_data_modal (idModal) {
// 	$(idModal).on('hide.bs.modal',function () {
// 		console.log('ENTRA EN HIDEN');
// 		// // console.log($(this).removeData('bs.modal'));
// 		$(idModal).data('bs.modal', null);
// 		//$(idModal).removeData();


// 	});	
// 	// $(idModal).on('hidden.bs.modal', function () {
// 	// 	$(idModal).data('bs.modal', null).find(".modal-content").empty();
// 	// 	console.log('entro aqui');
// 	// });
// // 	$(document).on("hidden.bs.modal", ".modal:not(.local-modal)", function (e) {
// // 		$(e.target).removeData("bs.modal").find(".modal-content").empty();
// // 	});
// 	// $(idModal).on('hidden', function() {
// 	// 	$(this).removeData('modal');
// 	// });
// }


function centro_asistencia_add (idForm, idModal, url_rest) {
	idForm.on('submit', function(e) {		
		e.preventDefault();
		var json = $(this).serialize();	
		$.post(url_rest, json, function(data) {	
			if (data.respuesta) {
				$(idModal).modal('hide');
				// $(idModal).modal('hide').data('bs.modal',null);
				location.reload();
			}else{
				var mensaje = '<small><div class="alert alert-danger mensaje">' +
				'<button type="button" class="close" data-dismiss="alert">&times;</button>'+
				'</div></small>';
				$('#id_mensaje_centro_asistencia').html(mensaje);				
				$.each(data.errores, function(index, element){					
					var mensajes_error = '<span>' + element+ '</span> <br>';										
					// index... da los atributos
					$(".mensaje").append(mensajes_error);					
				});
			};			
		});
		
	});	
}


function modalDatosEliminar (modalDelete) {
	$(document.body).on('click', modalDelete, function(){		
		var nombre = $(this).data('nombre');		
		$('#modal_nombre').text(nombre);
	});	 
}

// ELIMINA EL USUARIO MANY TO MANY DE CENTRO DE ASISTENCIA
function eliminar_usuario () {
	$('.eliminar-usuario').on('click', function(event) {
		var usuario = $(this).data('nombre');
		var dni = $(this).data('id');
		var tipo_usuario = $(this).data('tipousuario');
		var centro_asistencia = $('#centro_asistencia_pk').val();

		bootbox.confirm({			
			message : '¿Realmente desea eliminar al usuario <strong>' + usuario +'</strong>?',
			title: '<h3>Eliminar usuario</h3>',			
			buttons: {				
				confirm: 
					{label: 'Eliminar', className: 'btn-danger pull-right'}
			},
			callback: function(result) {
				if (result) {
					$.ajax({
						url: '/centro_asistencia/remove_usuario',
						type: 'POST',
						dataType: 'json',
						data: {
							'dni': dni,
							'tipo_usuario':tipo_usuario, 
							'centro_asistencia':centro_asistencia,
							'csrfmiddlewaretoken':csrftoken,
						},
					})					
					.fail(function(data) {
						bootbox.alert('<strong>'+'Lo sentimos, la acción no se pudo realizar.'+'</strong>', function(){
							location.reload();
						});
					})
					.always(function(data) {
						bootbox.alert('<strong>'+data.respuesta+ '</strong>'+data.mensaje, function(){
							console.log("supuestamente refresca la página");
							location.reload();
						});
					});	
				}
			}
		});
		// box.find(".btn-primary").removeClass("btn-primary").addClass("btn-danger");
	});
}
