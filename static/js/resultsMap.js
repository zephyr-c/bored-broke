"use strict";

function initMap() {
    const userCoords = {
        lat: 37.7887459,
        lng: -122.4115852
    };

    const resultMap = new google.maps.Map(
        document.querySelector('#map'),
        {
            center: userCoords,
            zoom: 12
        }
        );


  let locations = [];
  const places = document.querySelectorAll('.marker-info');
  for (const place of places) {
    let marker = JSON.parse(place.value);
    marker.coords.lat = parseFloat(marker.coords.lat);
    marker.coords.lng = parseFloat(marker.coords.lng);
    locations.push(marker);
  };

  const markers = [];
  for (const location of locations) {
    markers.push(new google.maps.Marker({
      position: location.coords,
      title: location.name,
      map: resultMap,
      icon: {  // custom icon
        url: '/static/marker.svg',
        scaledSize: {
          width: 30,
          height: 30
        }
      }
    }));
  }

  for (const marker of markers) {
    const markerInfo = (`
      <h3>${marker.title}</h3>
      <p>
        Located at: <code>${marker.position.lat()}</code>,
        <code>${marker.position.lng()}</code>
      </p>
    `);

    const infoWindow = new google.maps.InfoWindow({
      content: markerInfo,
      maxWidth: 200
    });

    marker.addListener('click', () => {
      infoWindow.open(resultMap, marker);
    });

  }
}