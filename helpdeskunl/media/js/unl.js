jQuery(document).ready(function($) {
	activarCarousel();
});

function activarCarousel () {
	$(".carousel").carousel({
		interval : 3000
	});	
}