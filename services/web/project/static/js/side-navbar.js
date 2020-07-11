(function($) {

	'use strict';

	$(document).ready(function() {
			
		// Slidebar				
		$.slidebars();
	
		// Nav Close Button
		$("#close-button").on( "click", function(e){
			e.preventDefault();
			$.slidebars.close();
		});
	
		// Side Nav Menu Click
		$('#side-nav-menu').on( "click", function(e){
			var target =  $(e.target);
						
			if ( target.is('a')) {					
				
				var href_value = target.attr("href");	
				
				// Prevent Default Link with #
				if (target.attr("href") == "#"){
					e.preventDefault();
				}
				
				// Plus and Minus For Parent Menu
				if ( target.next().is('ul')) {
					var this_ul = target.next();				
					this_ul.toggleClass("expand");
		
					if (target.hasClass("minus")){
						target.removeClass("minus");
					}
					else
					{
						target.addClass("minus");
					}
				}	
							
			}
			
		});
	
		// One Page Side Nav Menu
		$('#side-nav-menu.nav-smooth-scroll a').smoothScroll({
			speed: 1000,
			offset: 0,
			beforeScroll: function() {
				$.slidebars.close();
			},
		});	
	
			
	});
			
})(jQuery);	