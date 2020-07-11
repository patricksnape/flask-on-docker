(function($) {

	'use strict';
	
	// MAIN SLIDER-FLEXSLIDER
	//==================================================================================
	$(window).load(function() {
		var main_slider = $('#main-slider');
		var ul_slides = $('#main-slider').find('ul.slides');
		var slide_effect, speed, show_control_nav, show_direction_nav, pause_on_hover;		
		
		// Slide Effect Option
		if (main_slider.hasClass("slider-fade")){
			slide_effect = "fade";
		}
		else if (main_slider.hasClass("slider-slide")){
			slide_effect = "slide";
		}
		
		if (main_slider.data("speed")) {
 		 	speed = $('#main-slider').data("speed");
		}
		
		// Show Control Nav Option
		if (main_slider.hasClass("show-control-nav")) {
 		 	show_control_nav = true;
		}
		else{
			show_control_nav = false;
		}
		
		// Show Direction Nav Option
		if (main_slider.hasClass("show-direction-nav")) {
 		 	show_direction_nav = true;
		}
		else{
			show_direction_nav = false;
		}
		
		// Pause on Hover Option
		if (main_slider.hasClass("pause-on-hover")) {
 		 	pause_on_hover = true;
		}
		else{
			pause_on_hover = false;
		}
		
		// Start Flexslider
		$('#main-slider.flexslider').flexslider(
		{
			animation : slide_effect,
			controlNav: show_control_nav,
			directionNav: show_direction_nav,
			slideshowSpeed: speed,  
			animationSpeed:1500,
			pauseOnAction: false,
			animationLoop: true, 
			pauseOnHover: pause_on_hover,
			start:function(slider){
				if( !device.tablet() && !device.mobile() || isIE11desktop() ) {
					//Loop Animation 
					if (main_slider.hasClass("slider-fade") && main_slider.hasClass("animate-image")){
						ul_slides.find(".flex-active-slide > .loop-animation").addClass("animate");
					}
					
					//Caption Use Animation 
					if (main_slider.hasClass("animate-title")){
						ul_slides.find(".flex-active-slide .use-animation").css({ visibility: 'visible' }).addClass("animated");
					}
				}
				else
				{
					//Caption Use Animation
					if (main_slider.hasClass("animate-title")){
						$(".use-animation").css({ visibility: 'visible' });
					}
				}
			},
			before:function(){
				if( !device.tablet() && !device.mobile() || isIE11desktop() ) {
					//Caption Use Animation
					if (main_slider.hasClass("animate-title")){
					
						ul_slides.find("li .use-animation").css({ visibility: 'hidden' }).removeClass("animated");
					}
				}
			},
			after:function(){
				if( !device.tablet() && !device.mobile() || isIE11desktop() ) {
					//Loop Animation
					if (main_slider.hasClass("slider-fade") && main_slider.hasClass("animate-image")){
						ul_slides.find("li > .loop-animation").removeClass("animate");
						ul_slides.find(".flex-active-slide > .loop-animation").addClass("animate");
					}
					
					//Caption Use Animation
					if (main_slider.hasClass("animate-title")){
						ul_slides.find(".flex-active-slide .use-animation").css({ visibility: 'visible' }).addClass("animated");
					}
				}			
			}		
			
		});
	});
	
	// Check FIREFOX 
	//----------------------------------------------------------------------------------
	var is_firefox = function is_firefox() {
		if (navigator.userAgent.toLowerCase().indexOf('firefox') > -1){
			return 1;
		}
	}
	
	// Check IE11 (Not Windows Phone)
	///----------------------------------------------------------------------------------
	var isIE11desktop = function isIE11desktop() {	
 		if (!!navigator.userAgent.match(/Trident\/7\./) && window.navigator.userAgent.indexOf("Windows Phone") < 0) {
   		 	return 1;
		}
	}
	
	if (is_firefox() || isIE11desktop()){
		$('.flexslider .slides').addClass("css-fade");
	}
	
})(jQuery);