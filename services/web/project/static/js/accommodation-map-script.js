(function ($) {

    'use strict';

    // CHECK WINDOW RESIZE
    let is_windowresize = false;
    $(window).resize(function () {
        is_windowresize = true;
    });

    function parse_lat_long(lat_long) {
        lat_long = lat_long.split(',');
        lat_long[0] = parseFloat(lat_long[0]);
        lat_long[1] = parseFloat(lat_long[1]);
        return lat_long
    }

    function center_of_lat_longs(lat_longs) {
        let num_coords = lat_longs.length;
        let X = 0.0;
        let Y = 0.0;
        let Z = 0.0;

        for (let i = 0; i < num_coords; i++) {
            let lat = lat_longs[i][0] * Math.PI / 180;
            let lon = lat_longs[i][1] * Math.PI / 180;
            let a = Math.cos(lat) * Math.cos(lon);
            let b = Math.cos(lat) * Math.sin(lon);
            let c = Math.sin(lat);

            X += a;
            Y += b;
            Z += c;
        }

        X /= num_coords;
        Y /= num_coords;
        Z /= num_coords;

        let lon = Math.atan2(Y, X);
        let hyp = Math.sqrt(X * X + Y * Y);
        let lat = Math.atan2(Z, hyp);

        let center_lat = lat * 180 / Math.PI;
        let center_long = lon * 180 / Math.PI;

        return [center_lat, center_long];
    }

    function map_fit_bounds(map, lat_longs) {
        let bounds = new google.maps.LatLngBounds();
        if (lat_longs.length > 0) {
            for (let i = 0; i < lat_longs.length; i++) {
                bounds.extend(new google.maps.LatLng(lat_longs[i][0], lat_longs[i][1]));
            }
            map.fitBounds(bounds);
        }
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

        //DEFINE MAP OPTIONS
        //=======================================================================================
        let canvas_elem = document.getElementById('map-canvas');
        const mapOptions = {
            mapTypeId: google.maps.MapTypeId.ROADMAP,
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


        // Add markers for each element found
        let lat_longs = [];
        let first_marker = null;
        $("#map-markers div[data-map-lat-long]").each(function () {
            let that = this;
            let size = parseFloat(that.getAttribute('data-map-marker-size'));
            let lat_long = parse_lat_long(that.getAttribute('data-map-lat-long'));
            lat_longs.push(lat_long);

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

            if (first_marker === null) {
                first_marker = marker;
            }

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

        // Set the map center based on the markers
        const center_lat_long = center_of_lat_longs(lat_longs);
        map.setCenter(new google.maps.LatLng(center_lat_long[0], center_lat_long[1]));

        // Set the zoom level automatically to fit all the markers inside
        map_fit_bounds(map, lat_longs);

        google.maps.event.addListener(map, 'bounds_changed', function () {
            if (is_windowresize) {
                if (first_marker !== null) {
                    window.setTimeout(function () {
                            map.panTo(first_marker.getPosition());
                        },
                        500
                    );
                }
            }
            is_windowresize = false;
        });
    }

    google.maps.event.addDomListener(window, 'load', initialize);

})(jQuery);
