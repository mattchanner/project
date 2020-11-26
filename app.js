let map;

function getPoints() {
    const rows = document.querySelectorAll("#dataframe table tbody tr");
    const points = Array.from(rows).map((row) => {
        const cells = row.querySelectorAll("td");
        return {
            lng: parseFloat(cells[0].innerHTML),
            lat: parseFloat(cells[1].innerHTML)
        }
    });

    return points;
}

function initMap() {
    const points = getPoints();

    let minLat = 0, maxLat = 0, minLng = 0, maxLng = 0;

    points.forEach((pt) => {
        minLat = minLat != 0 ? Math.min(minLat, pt.lat) : pt.lat;
        minLng = minLng != 0 ? Math.min(minLng, pt.lng) : pt.lng;
        maxLat = maxLat != 0 ? Math.max(maxLat, pt.lat) : pt.lat;
        maxLng = maxLng != 0 ? Math.max(maxLng, pt.lng) : pt.lng;
    });

    map = new google.maps.Map(document.getElementById("map"), {
        center: { lat: (maxLat + minLat) / 2, lng: (maxLng + minLng) / 2 },
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
}
