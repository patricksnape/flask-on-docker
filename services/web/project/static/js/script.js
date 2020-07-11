/*=============================================================
	- Template Name: STORY - Responsive HTML Wedding Template
	- Author: DoubleEight
	- Version: 1.0
	- Website: www.dethemes.com
=============================================================== */

/*----------------------
	Script Guide
------------------------
01. BROWSER AGENT FUNCTION
	01.1 Check CHROME (Mobile / Tablet)
	01.2 Check IOS
	01.3 Check FIREFOX
	01.4 Check IE (< IE10)
	01.5 Check IE11
	01.6 Check IE11 (Not Windows Phone)
	01.7 Check IE10
	01.8 Check IE9
	01.9 Check Safari/Chrome Mac

02. OTHER FUNCTION AND CLASS
	02.1 Fullscreen Class
	02.2 Hide All Animation Class
	02.3 Function For Resize Video

03. PRELOAD
	03.1 Navigation Menu
		03.1.1 Waypoint Sticky Navbar
		03.1.2 Waypoint OnePage Nav - Active Class
	03.2 Gallery - Masonry
	03.3 Stellar Parallax
	03.4 Waypoint Animate CSS
	03.5 Resize Background Video

04. MENU
	04.1 Menu Active Class (Multipage)
	04.2 Top Menu Smooth Scroll (Onepage)
	04.3 Mobile Menu
	04.4 Double Tap Drop Down Menu

05. SLIDE
	05.1 Slide Image (Background Position)
	05.2 Slide Video
		05.2.1 Hide Video Loader on Mobile
		05.2.2 Each Video
			05.2.2.1 Pause All Video on load on Mobile
			05.2.2.2 Resize Video
		05.2.3 Set Play or Pause Icon for Video on load
		05.2.4 Play Pause On Click
	05.3 HTML Audio
		05.3.1 Set Mute Icon for Mobile or Not Autoplay Audio
		05.3.2 On toggle mute button

06. ELEMENT
	06.1 Photo Item
	06.2 Countdown
	06.3 Gift Carousel
	06.4 Smooth Scroll Link
	06.5 Magnific Popup
		06.5.1 Magnific Zoom
		06.5.2 Magnific Zoom Gallery
		06.5.3 Magnific Ajax
	06.6 Icon
	06.7 SoundCloud Button
	06.8 Image Divider (Video)
		06.8.1 Each Divider Video
			06.8.1.1 Pause All Video on load on Mobile
			06.8.1.2 Resize Video
		06.8.2 Set Play or Pause Icon for Video on load
		06.8.3 Play Pause On Click

07. RSVP
	07.1 Custom Checkbox
	07.2 Custom Radio
*/

(function($) {

'use strict';

	$(document).ready(function() {

	// 01. BROWSER AGENT FUNCTION
	//=============================================================================================================================================
	//=============================================================================================================================================
	//=============================================================================================================================================

	// 01.1 Check Chrome (Mobile / Tablet)
	//================================================================================
	var isChromeMobile = function isChromeMobile() {
		if (device.tablet() || device.mobile()) {
			if (window.navigator.userAgent.indexOf("Chrome") > 0 || window.navigator.userAgent.indexOf("CriOS") > 0){
				return 1;
			}
		}
	}

	// 01.2 Check IOS
	//================================================================================
	var isIOS = function isIOS() {
		if (window.navigator.userAgent.indexOf("iPhone") > 0 || window.navigator.userAgent.indexOf("iPad") > 0 || window.navigator.userAgent.indexOf("iPod") > 0){
			return 1;
		}
	}

	// 01.3 Check FIREFOX
	//================================================================================
	var is_firefox = function is_firefox() {
		if (navigator.userAgent.toLowerCase().indexOf('firefox') > -1){
			return 1;
		}
	}

	// 01.4 Check IE (< IE10)
	//================================================================================
	var isIE = function isIE() {
 		if (window.navigator.userAgent.indexOf("MSIE ") > 0 || !!navigator.userAgent.match(/Trident\/7\./)) {
   		 	return 1;
		}
	}

	// 01.5 Check IE11
	//================================================================================
	var isIE11 = function isIE11() {
 		if (!!navigator.userAgent.match(/Trident\/7\./)) {
   		 	return 1;
		}
	}

	// 01.6 Check IE11 (Not Windows Phone)
	//================================================================================
	var isIE11desktop = function isIE11desktop() {
 		if (!!navigator.userAgent.match(/Trident\/7\./) && window.navigator.userAgent.indexOf("Windows Phone") < 0) {
   		 	return 1;
		}
	}

	// 01.7 Check IE10
	//================================================================================
	var isIE10 = function isIE10() {
 		if (window.navigator.userAgent.indexOf("MSIE 10.0") > 0) {
   		 	return 1;
		}
	}

	// 01.8 Check IE9
	//================================================================================
	var isIE9 = function isIE9() {
 		if (window.navigator.userAgent.indexOf("MSIE 9.0") > 0) {
   		 	return 1;
		}
	}

	// 01.9 Check Safari/Chrome Mac
	//================================================================================
	var isSafari = function isSafari() {
	 	if (navigator.userAgent.indexOf('Safari') != -1 && navigator.userAgent.indexOf('Mac') != -1) {
   		 	return 1;
		}
	}





	// 02. OTHER FUNCTION AND CLASS
	//=============================================================================================================================================
	//=============================================================================================================================================
	//=============================================================================================================================================

	// 02.1 Fullscreen Class
	//================================================================================
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


	// 02.2 Hide All Animation Class
	//================================================================================
	// Waypoint will animate it later (03.2 Waypoint Animate CSS)
	if( !device.tablet() && !device.mobile() && !isIE9() ) {
		$('.animation').css({
			visibility: 'hidden'
		});
	}


	// 02.3 Function For Resize Video
	//----------------------------------------------------------------------------------
	var video_resize = function(parent_wrapper){

		$(parent_wrapper).each(function(){

			var
          		// get native video size
            	videoHeight = $(this).find("video").height(),
            	videoWidth =  $(this).find("video").width(),

            	// get wrapper size
            	wrapperHeight = $(this).innerHeight(),
            	wrapperWidth = $(this).innerWidth(),

				divideWidth = wrapperWidth / videoWidth,
				divideHeight = wrapperHeight / videoHeight


       		if (divideWidth > divideHeight) {
            	$(this).find("video").css({
                	"width": wrapperWidth + 2,

                	// +2 pixels to prevent empty space after transformation
                	"height": "auto"
            	});
        	} else {
            	$(this).find("video").css({
                	"width": "auto",

               		// +2 pixels to prevent empty space after transformation
               		"height": wrapperHeight + 2
            	});

        	}

			$(this).find("video").css({
				"top": "50%",
            	"left": "50%",
				"-webkit-transform": "translate(-50%,-50%)",
           	 	"-ms-transform": "translate(-50%,-50%)",
            	"transform": "translate(-50%,-50%)"
			})

		});

	}




	// 03. PRELOAD
	//=============================================================================================================================================
	//=============================================================================================================================================
	//=============================================================================================================================================
	Pace.on('done', function () {
		$('#preloader').fadeOut(1000);
	});

	Pace.on('hide', function () {

		// 03.1 Navigation Menu
		//================================================================================

		// 03.1.1 Waypoint Sticky Navbar
		//------------------------------------------------------------------------------
		if ($("#nav-bar").hasClass("sticky-nav")){

			var navbar_el = $("#nav-bar");

			var nav_header_waypoint = $('#nav-header').waypoint(function(direction) {

				if (direction === 'down') {
					if( !device.tablet() && !device.mobile() ) {
						navbar_el.addClass("stick-it animated fadeInDownBig");
					}
					else
					{
						navbar_el.addClass("stick-it");
					}
				}
				else {
					navbar_el.removeClass("stick-it animated fadeInDownBig");
				}

			}, {
  				offset:'-100%'
			});

		}

		// 03.2 Gallery - Masonry
		//================================================================================
		if ($("#masonry-gallery").length){
			var $gallery = $('#masonry-gallery');

			if (device.tablet() || device.mobile()) {
				$gallery.masonry({
					columnWidth: ".grid-sizer",
					itemSelector: ".masonry-col",
					gutter: ".gutter-sizer",
					transitionDuration: 0,
				});
			}
			else
			{
				$gallery.masonry({
					columnWidth: ".grid-sizer",
					itemSelector: ".masonry-col",
					gutter: ".gutter-sizer",
					transitionDuration: "1s",
				});
			}
		}

		// 03.3 Stellar Parallax
		//================================================================================
	 	if( !device.tablet() && !device.mobile() && !isIE9() && !isIE10() && !isSafari() ) {
			$(".image-divider").css("background-attachment","fixed");
		 	$(window).stellar({
			 	horizontalScrolling: false,
				responsive: true,
		 	});
	 	}

		// 03.4 Waypoint Animate CSS
		//================================================================================
		if( !device.tablet() && !device.mobile() && !isIE9() ) {
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

		// 03.5 Resize Background Video
		//================================================================================
		//Execute on load (function can be found on point 02.3)
		video_resize("#main-slider .slide-image");
		video_resize(".image-divider");

		//Execute on window resize
		$(window).resize(function() {
			video_resize("#main-slider .slide-image");
			video_resize(".image-divider");
		});

	}); // END of Pace on Hide





	// 04. MENU
	//=============================================================================================================================================
	//=============================================================================================================================================
	//=============================================================================================================================================


	// 04.3 Mobile Menu
	//================================================================================
	$("#mobile-nav").on( "click", function(e){
		$("#top-nav-menu").toggleClass("open");
		return false;
	});

	// 04.4 Double Tap Drop Down Menu
	//================================================================================
	if ($(window).width() > 991){
		$( '#top-nav-menu' ).doubleTapToGo();
	}





	// 05. SLIDE
	//=============================================================================================================================================
	//=============================================================================================================================================
	//=============================================================================================================================================

	// 05.1 Slide Image (Background Position)
	//================================================================================
	var slide_image_position = function(){
		$('#main-slider .slide-image').each(function(){
			var mobile_image_position = $(this).data("mobile-image-position");
			var tablet_image_position = $(this).data("tablet-image-position");

			if ($(window).width() <= "480" && mobile_image_position != ""){
				$(this).css("background-position",mobile_image_position);
			}
			else if ($(window).width() <= "991" && tablet_image_position != ""){
				$(this).css("background-position",tablet_image_position);
			}
		});
	}

	//Execute on load
	slide_image_position();

	//Execute on window resize
	$(window).resize(function() {
		slide_image_position();
	});


	// 05.2 Slide Video
	//================================================================================
	var main_slider = $('#main-slider');

	// 05.2.1 Hide Video Loader on Mobile
	//----------------------------------------------------------------------------------
	if (device.tablet() || device.mobile() || isIE11()){
		$(".loader").hide();
	}

	// 05.2.2 Each Video
	//----------------------------------------------------------------------------------
	main_slider.find("video").each(function(){

		// 05.2.2.1 Pause All Video on load on Mobile
		//----------------------------------------------------------------------------------
		if (device.tablet() || device.mobile()){
			$(this).removeAttr( "autoplay" ).get(0).pause();
		}

		// 05.2.2.2 Resize Video
		//----------------------------------------------------------------------------------
		$(this).on('canplay', function(){
			video_resize("#main-slider .slide-image");
		});
	});

	// 05.2.3 Set Play or Pause Icon for Video on load
	//----------------------------------------------------------------------------------
	main_slider.find(".play-pause").each(function(){
		var js_control = $(this).parents(".js-control");
		var closest_video;

		//Get Video
		if (js_control.hasClass("multiple")){
			closest_video = js_control.siblings(".slide-image").children("video");
		}
		else{
			closest_video = js_control.siblings(".slides").find("video");
		}

		var play_attr = closest_video.attr('autoplay');

       	if (device.tablet() || device.mobile()){
			closest_video.css("visibility","hidden");
		}
		else{
			//if autoplay
			if (typeof play_attr !== typeof undefined && play_attr !== false){
				$(this).find("i").removeClass("de-icon-play").addClass("de-icon-pause");
			}
			//if not autoplay
			else{
				closest_video.css("visibility","hidden").siblings(".loader").hide();
			}
		}
    })

	// 05.2.4 Play Pause On Click
	//----------------------------------------------------------------------------------
	main_slider.find(".play-pause").on( "click", function(e){
		e.preventDefault();

		var closest_video;
		var js_control   = $(this).parents(".js-control");
		var li_parent   = $(this).parents("li");
		var first_click = 1;

		if (js_control.hasClass("multiple")){
			//Get Video
			closest_video = js_control.siblings(".slide-image").children("video");

			//Set Sibling Video to Pause
			if (!isIOS()){

				if ($(this).find("i").hasClass("de-icon-play")){
					$(this).parents("li").siblings().find("video").get(0).pause();
					$(this).parents("li").siblings().find(".play-pause i").removeClass("de-icon-pause").addClass("de-icon-play");

					//Also Pause Image Divider Video
					$(".image-divider video").each(function(){
						$(this).get(0).pause();
						$(this).parents(".image-divider").find(".play-pause i").removeClass("de-icon-pause").addClass("de-icon-play");
					});
				}

			}
		}
		else{
			closest_video = js_control.siblings(".slides").find("video");
		}

		//If Pause then Play
		if (!isIOS()){
			if ($(this).find("i").hasClass("de-icon-play")){
				$(this).find("i").removeClass("de-icon-play").addClass("de-icon-pause");
				closest_video.css("visibility","visible").get(0).play();
				if (first_click == 1){
					closest_video.siblings(".loader").show();
					first_click = 2;
				}
			}
			//If Play then Pause
			else{
				$(this).find("i").removeClass("de-icon-pause").addClass("de-icon-play");
				closest_video.css("visibility","visible").get(0).pause();
			}
		}
		else{
			closest_video.css("visibility","visible").get(0).play();
		}
	});



	// 05.3 HTML Audio
	//================================================================================

	var audio_play_attr = $("#html-audio").attr('autoplay');
	var audio_icon = $("#mute-html-audio i");

	// 05.3.1 Set Mute Icon for Mobile or Not Autoplay Audio
	//----------------------------------------------------------------------------------
	if (device.tablet() || device.mobile() || typeof audio_play_attr === typeof undefined || audio_play_attr === false){
		var audioElm = document.getElementById('html-audio');

		if 	(audioElm != null){
			if (isIOS()){
				audioElm.pause();
			}
			else
			{
				audioElm.muted = true;
			}
		}

		audio_icon.removeClass("de-icon-volume-up").addClass("de-icon-volume-off");
	}

	// 05.3.2 On toggle mute button
	//----------------------------------------------------------------------------------
	 $("#mute-html-audio").on( "click", function(e){
		e.preventDefault();
		var audioElm = document.getElementById('html-audio');

		if (audio_icon.hasClass("de-icon-volume-up")){
			audio_icon.removeClass("de-icon-volume-up").addClass("de-icon-volume-off");
			if (isIOS()){
				audioElm.pause();
			}
			else
			{
				audioElm.muted = true;
			}
		}
		else
		{
			audio_icon.removeClass("de-icon-volume-off").addClass("de-icon-volume-up");
			audioElm.play();
			audioElm.muted = false;
		}
	});





	// 06. ELEMENT
	//=============================================================================================================================================
	//=============================================================================================================================================
	//=============================================================================================================================================

	// 06.1 Photo Item
	//================================================================================
	var photo_item = $('.photo-item');

	if( device.tablet() || device.mobile() ) {
		if (!isIE11desktop()){
			photo_item.find(".hover-animation").css("transition","none");
		 }
	 }

	 photo_item.on( "touchstart touchend", function(e) {
	});


	// 06.2 Countdown
	//================================================================================
	var theday = new Date(2021, 7, 19);
	$('#countdown').countdown({until: theday, format: 'WDHMS'});


	// 06.3 Gift Carousel
	//================================================================================
	if ($("#gift-registry").length){

		var gift_registry = $("#gift-registry");
    	gift_registry.owlCarousel({
			items : 2,
			autoPlay: 2000,
			stopOnHover: true,
			pagination: true,
		});

		if (device.tablet() || device.mobile()) {
			var owl_gift = gift_registry.data('owlCarousel');
			owl_gift.stop()
		}

	}

	// 06.4 Smooth Scroll Link
	//================================================================================
	$('a.smooth-scroll').smoothScroll({
		speed: 1000,
	});


	// 06.5 Magnific Popup
	//================================================================================

	// 06.5.1 Magnific Zoom
	//----------------------------------------------------------------------------------
	if ($(".magnific-zoom").length){
		$('.magnific-zoom').magnificPopup({
 			type: 'image',
			image: {
    			// options for image content type
    			titleSrc: 'title'
 			},
			//fixedContentPos:true,
			callbacks: {
    			open: function() {
      				// Will fire when this exact popup is opened
    			},
    			afterClose: function() {
      				// Will fire when popup is closed
    			}
  			},
		});
	}

	// 06.5.2 Magnific Zoom Gallery
	//----------------------------------------------------------------------------------
	if ($(".magnific-zoom-gallery").length){
		$('.magnific-zoom-gallery').magnificPopup({
 			type: 'image',
			image: {
    			// options for image content type
    			titleSrc: 'title'
 			},
			gallery: {
         		 enabled:true
        	},
			//fixedContentPos:true,
			callbacks: {
    			open: function() {
      				// Will fire when this exact popup is opened
    			},
    			afterClose: function() {
      				// Will fire when popup is closed
    			}
  			},
		});
	}

	// 06.5.3 Magnific Ajax
	//----------------------------------------------------------------------------------
	if ($(".magnific-ajax").length){
		$('.magnific-ajax').magnificPopup({
  			type: 'ajax',
			ajax: {
				settings: {cache:false}
				// Ajax settings object that will extend default one - http://api.jquery.com/jQuery.ajax/#jQuery-ajax-settings
				// For example:
				// settings: {cache:false, async:false}
			},
			callbacks: {
    			open: function() {
      				// Will fire when this exact popup is opened
    			},
    			afterClose: function() {
      				// Will fire when popup is closed

    			}
  			},
		});
	}

	// 06.6 Icon
	//================================================================================
	if( device.tablet() || device.mobile() ) {
		if (!isIE11desktop()){
			$(".de-icon, .de-icon i").css("transition","none");
		 }
	 }

	// 06.7 SoundCloud Button
	//================================================================================
	$("#soundcloud-button").on( "click", function(e){
		e.preventDefault();
		$("#soundcloud-track").toggleClass( "open-window" );

	});


	// 06.8 Image Divider Video
	//================================================================================
	var image_divider = $('.image-divider');

	// 06.8.1 Each Divider Video
	//----------------------------------------------------------------------------------
	image_divider.find("video").each(function(){

		// 06.8.1.1 Pause All Video on load on Mobile
		//----------------------------------------------------------------------------------
		if (device.tablet() || device.mobile()){
			$(this).removeAttr( "autoplay" ).get(0).pause();
		}

		// 06.8.1.2 Resize Video
		//----------------------------------------------------------------------------------
		$(this).on('canplay', function(){
			video_resize(".image-divider");
		});
	});

	// 06.8.2 Set Play or Pause Icon for Video on load
	//----------------------------------------------------------------------------------
	image_divider.find(".play-pause").each(function(){;
		var closest_video = $(this).parents(".image-divider").find("video");
		var play_attr = closest_video.attr('autoplay');

       	if (device.tablet() || device.mobile()){
			closest_video.css("visibility","hidden");
		}
		else{
			//if autoplay
			if (typeof play_attr !== typeof undefined && play_attr !== false){
				$(this).find("i").removeClass("de-icon-play").addClass("de-icon-pause");
			}
			//if not autoplay
			else{
				closest_video.css("visibility","hidden").siblings(".loader").hide();
			}
		}
    })

	// 06.8.3 Play Pause On Click
	//----------------------------------------------------------------------------------
	image_divider.find(".play-pause").on( "click", function(e){
		e.preventDefault();

		var closest_video = $(this).parents(".image-divider").find("video");
		var first_click = 1;

		//Set Sibling Video to Pause
		if (!isIOS()){
			if ($(this).find("i").hasClass("de-icon-play")){
				// Pause other video divider
				$(".image-divider .play-pause").not(this).each(function(){
					$(this).parents(".image-divider").find("video").get(0).pause();
					$(this).parents(".image-divider").find(".play-pause i").removeClass("de-icon-pause").addClass("de-icon-play");
				});

				// Also pause Slide Video
				$("#main-slider video").each(function(){
					$(this).get(0).pause();
					$(this).parents("li").find(".play-pause i").removeClass("de-icon-pause").addClass("de-icon-play");
				});

			}

		}

		//If Pause then Play
		if (!isIOS()){
			if ($(this).find("i").hasClass("de-icon-play")){
				$(this).find("i").removeClass("de-icon-play").addClass("de-icon-pause");
				closest_video.css("visibility","visible").get(0).play();
				if (first_click == 1){
					closest_video.siblings(".loader").show();
					first_click = 2;
				}
			}
			//If Play then Pause
			else{
				$(this).find("i").removeClass("de-icon-pause").addClass("de-icon-play");
				closest_video.css("visibility","visible").get(0).pause();
			}
		}
		else{
			closest_video.css("visibility","visible").get(0).play();
		}
	});





	// 07. RSVP
	//=============================================================================================================================================
	//=============================================================================================================================================
	//=============================================================================================================================================
	if ($("#rsvpform").length){
		$("#rsvpform").ajaxrsvp();
	}

	// 07.1 Custom Checkbox
	//================================================================================
	$(".ajax-checkbox").on( "click", function(e){
		var target = $(e.target);
		if ( target.is('.custom-option-icon') ){
			target.toggleClass( "active-icon" );
		}
	});

	// 07.2 Custom Radio
	//================================================================================
	$(".ajax-radio").on( "click", function(e){
		var target = $(e.target);
		if ( target.is('.custom-option-icon') ){
			if (!(target.parent().hasClass("radio"))){
				target.addClass( "active-icon" ).siblings().removeClass( "active-icon" );
			}
			else{
				target.addClass( "active-icon" ).parent().siblings().children(".custom-option-icon").removeClass( "active-icon" );
			}
		}
	});


	});
})(jQuery);
