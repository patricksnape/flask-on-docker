(function ($) {

    'use strict';

    // CHECK WINDOW RESIZE
    let is_windowresize = false;
    $(window).resize(function () {
        is_windowresize = true;
    });

    // function create_marker_div() {
    //     '<div id="house-marker" class="main-icon-wrapper"><div class="big-circle scale-animation"></div><div class="main-icon-text">Ceremony</div></div>'
    // '<div id="taxi-marker" class="de-icon circle medium-size animation fadeIn" style="background-color:rgba(255, 255, 255, 0.8); color:#333333; font-size:24px;"><i class="de-icon-taxi"></i></div>'
    // }

    function parse_lat_long(lat_long) {
        lat_long = lat_long.split(',');
        lat_long[0] = parseFloat(lat_long[0]);
        lat_long[1] = parseFloat(lat_long[1]);
        return lat_long
    }


    //INITIALIZE MAP
    function initialize() {


        // Create an array of styles.
        const styles = [
            {
                stylers: [
                    {hue: "#f08080"},
                    {saturation: -50}
                ]
            }, {
                featureType: "road",
                elementType: "geometry",
                stylers: [
                    {lightness: 100},
                    {visibility: "simplified"}
                ]
            }, {
                featureType: "road",
                elementType: "labels",
                stylers: [
                    {visibility: "off"}
                ]
            }
        ];

        // Create a new StyledMapType object, passing it the array of styles,
        // as well as the name to be displayed on the map type control.
        let styledMap = new google.maps.StyledMapType(styles, {name: "Styled Map"});

        // House: 49.374088, 8.158309 ()
        // Tafel und Wein:  49.3870215,8.1601126 ()
        // Middle of map between house and tafel und wein ()
        //DEFINE MAP OPTIONS
        //=======================================================================================
        let canvas_elem = document.getElementById('map-canvas');
        let map_center = parse_lat_long(canvas_elem.getAttribute('data-map-center'));
        const mapOptions = {
            zoom: 14,
            mapTypeId: google.maps.MapTypeId.ROADMAP,
            center: new google.maps.LatLng(map_center[0], map_center[1]),
            zoomControl: true,
            mapTypeControl: true,
            streetViewControl: true,
            overviewMapControl: true,
            scrollwheel: false,
        };
        let map = new google.maps.Map(canvas_elem, mapOptions);

        //Associate the styled map with the MapTypeId and set it to display.
        map.mapTypes.set('map_style', styledMap);
        map.setMapTypeId('map_style');

        // Create single shared info window
        let info_window = new google.maps.InfoWindow({
            maxWidth: 300,
        });
        info_window.set('closed', true);

        let contentString1 = '' +
            '<div class="info-window-wrapper">' +
            '<h5>Wedding Ceremony</h5>' +
            '<div class="info-window-desc">Lorem ipsum dolor sit amet, consectetur.<br/><a href="#" class="with-underline">Click Here</a></div>' +
            '</div>';


        //ADD NEW MARKER WITH LABEL
        //=======================================================================================
        $("#map-markers div[data-map-lat-long]").each(function() {
            let that = this;
            let size = parseFloat(that.getAttribute('data-map-marker-size'));
            let lat_long = parse_lat_long(that.getAttribute('data-map-lat-long'));

            let marker_circle = $($(that).children('.marker')[0]);
            marker_circle.width(size);
            marker_circle.height(size);

            let marker = new MarkerWithLabel({
                position: new google.maps.LatLng(lat_long[0], lat_long[1]),
                draggable: false,
                raiseOnDrag: false,
                icon: ' ',
                map: map,
                labelContent: that,
                labelAnchor: new google.maps.Point(size / 2, size / 2),
                labelClass: "labels"
            });

            google.maps.event.addListener(marker, 'click', function () {
                info_window.set("pixelOffset", new google.maps.Size(0, -size / 4));
                info_window.setContent(contentString1);
                if (info_window.get('closed')) {
                    info_window.open(map, marker);
                    info_window.set('closed', false);
                } else {
                    info_window.close();
                    info_window.set('closed', true);
                }
            });
        });

        //ON BOUND EVENTS AND WINDOW RESIZE
        //=======================================================================================
        google.maps.event.addListener(map, 'bounds_changed', function () {
            if (is_windowresize) {
                window.setTimeout(function () {
                    map.panTo(marker1.getPosition());
                }, 500);
            }
            is_windowresize = false;
        });
    }

    // LOAD GMAP
    google.maps.event.addDomListener(window, 'load', initialize);

})(jQuery);
