(function($) {

'use strict';

	$(document).ready(function() {

	var fullscreen = function(){
		var fheight = $(window).height();
		var fullscreen_el = $('.fullscreen');

		if (device.mobile() && device.landscape() && $(window).width() <= 768){
			fullscreen_el.css("height","425px");
		}
		else
		{
			fullscreen_el.css("height",fheight);
		}
	}

	//Execute on load
	fullscreen();

	//Execute on window resize
	$(window).resize(function() {
		fullscreen();
	});


	// Waypoint will animate it later (03.2 Waypoint Animate CSS)
	if( !device.tablet() && !device.mobile() ) {
		$('.animation').css({
			visibility: 'hidden'
		});
	}


	Pace.on('done', function () {
		$('#preloader').fadeOut(1000);
	});

	Pace.on('hide', function () {

	 	if( !device.tablet() && !device.mobile() ) {
			$(".image-divider").css("background-attachment","fixed");
		 	$(window).stellar({
			 	horizontalScrolling: false,
				responsive: true,
		 	});
	 	}

		if( !device.tablet() && !device.mobile() ) {
			$('.animation').each(function(){
        		var _this = this;
        		var animation_waypoint = new Waypoint({
            		element: _this,
            		handler: function (direction) {
						$(this.element).css({ visibility: 'visible' }).addClass('animated');
            		},
            		offset: '95%'
        		});
        	});

		}

	});

	if( device.tablet() || device.mobile() ) {
		$(".de-icon, .de-icon i").css("transition","none");
	 }

	});
})(jQuery);
