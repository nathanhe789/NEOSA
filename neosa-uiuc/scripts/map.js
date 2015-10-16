// author Joe Tan
var map;
var current_location;

function initialize() {
  map = new google.maps.Map(document.getElementById('map'), {
    center: {lat: 0, lng: 0},
    zoom: 15
  });
  getUserLocation();
}


function getUserLocation() {
  if (navigator.geolocation)
  navigator.geolocation.getCurrentPosition(setLocation);
  else
    document.getElementById("locationData").innerHTML = "Sorry - your browser doesn't support geolocation!";
}

function setLocation(position) {
  lat = position.coords.latitude
  long = position.coords.longitude;
  current_location = new google.maps.LatLng(lat,long);
  map.setCenter({lat: lat, lng: long})
  createMarker({lat: lat, lng: long});
}

function ClearMarker() {
  if(marker != null ){
    marker.setMap(null);
  }
  marker = null;
}

function createMarker(latLng) {
  marker = new google.maps.Marker({
    map: map,
    position: latLng,
    title: 'You'
  });
}

google.maps.event.addDomListener(window, 'load', initialize);
