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

    function map_compute_bounds(map, lat_longs) {
        let bounds = new google.maps.LatLngBounds();
        if (lat_longs.length > 0) {
            for (let i = 0; i < lat_longs.length; i++) {
                bounds.extend(new google.maps.LatLng(lat_longs[i][0], lat_longs[i][1]));
            }
        }
        return bounds;
    }

    function get_zoom_by_bounds(map, bounds) {
        let MAX_ZOOM = map.mapTypes.get(map.getMapTypeId()).maxZoom || 21;
        let MIN_ZOOM = map.mapTypes.get(map.getMapTypeId()).minZoom || 0;

        let ne = map.getProjection().fromLatLngToPoint(bounds.getNorthEast());
        let sw = map.getProjection().fromLatLngToPoint(bounds.getSouthWest());

        let worldCoordWidth = Math.abs(ne.x - sw.x);
        let worldCoordHeight = Math.abs(ne.y - sw.y);

        let FIT_PAD = 40;

        for (let zoom = MAX_ZOOM; zoom >= MIN_ZOOM; --zoom) {
            if (worldCoordWidth * (1 << zoom) + 2 * FIT_PAD < $(map.getDiv()).width() &&
                worldCoordHeight * (1 << zoom) + 2 * FIT_PAD < $(map.getDiv()).height())
                return zoom;
        }
        return 0;
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

        // Add markers for each element found
        let lat_longs = [];
        let first_marker = null;
        $("#map-markers .marker-and-label").each(function () {
            let marker_div = $(this).children('div[data-map-lat-long]')[0];
            let label_div = $(this).children('.marker-label-content')[0];

            let size = parseFloat(marker_div.getAttribute('data-map-marker-size'));
            let lat_long = parse_lat_long(marker_div.getAttribute('data-map-lat-long'));
            lat_longs.push(lat_long);

            let marker_circle_div = $($(marker_div).children('.marker')[0]);
            marker_circle_div.width(size);
            marker_circle_div.height(size);

            let marker = new MarkerWithLabel({
                position: new google.maps.LatLng(lat_long[0], lat_long[1]),
                draggable: false,
                raiseOnDrag: false,
                icon: ' ',
                map: map,
                labelContent: marker_div,
                labelAnchor: new google.maps.Point(size / 2, size / 2),
                labelClass: "labels"
            });

            if (first_marker === null) {
                first_marker = marker;
            }

            google.maps.event.addListener(marker, 'click', function () {
                info_window.set("pixelOffset", new google.maps.Size(0, -size / 4));
                info_window.setContent(label_div);
                info_window.open(map, marker);
            });
        });

        // Set the map center based on the markers
        const center_lat_long = center_of_lat_longs(lat_longs);
        map.setCenter(new google.maps.LatLng(center_lat_long[0], center_lat_long[1]));

        // Set the zoom level automatically to fit all the markers inside
        let bounds = map_compute_bounds(map, lat_longs);
        map.fitBounds(bounds);

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

        $("#reset-map-mobile").click(function () {
            map.panTo(new google.maps.LatLng(center_lat_long[0], center_lat_long[1]));
            map.setZoom(get_zoom_by_bounds(map, bounds));
            info_window.close()
        });
    }

    google.maps.event.addDomListener(window, 'load', initialize);

})(jQuery);
