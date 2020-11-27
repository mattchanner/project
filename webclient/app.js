let map;

function getPoints() {
    // points is injected into the page
    return points;
}

function initMap() {
    const points = getPoints();

    const bounds = new google.maps.LatLngBounds();

    map = new google.maps.Map(document.getElementById("map"), {
        zoom: 14,
    });

    const coursePath = new google.maps.Polyline({
        path: points,
        geodesic: true,
        strokeColor: "#FF0000",
        strokeOpacity: 1.0,
        strokeWeight: 2,
    });

    coursePath.setMap(map);

    points.forEach((pt) => {
        bounds.extend(new google.maps.LatLng(pt.lat, pt.lng));
    });

    map.fitBounds(bounds);
}
