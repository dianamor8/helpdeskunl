function configuracion_tabla(id_tabla){
	$(id_tabla).dataTable({
		dom: '<"small" <"row" <"col-sm-6 text-left" l> <"col-sm-6 text-right" f>>>t<"small text-center pager"p>',		
		lengthMenu: [ [10, 15, 20, -1], [10, 15,20 ,"Todos"]],
		DisplayLength: 10,
		order: [1,'desc'],
		language: {
			"lengthMenu": "Mostrar _MENU_ resultados por página.",
			"zeroRecords": "La búsqueda realizada no generó registros.",
			"info": "Mostrando _PAGE_ de _PAGES_",
			"infoEmpty": "No hay registros disponibles",
			"infoFiltered": "Filtrado de _MAX_ resultados",
			"paginate": {"first": "Primero","last":"Último","next": "Siguiente","previous":"Anterior"},
			"search":"Buscar:       ",
			"loadingRecords": "Cargando...",
			"processing":"Procesando...",
        }	
	});
}