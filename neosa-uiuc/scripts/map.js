// author Joe Tan & Jonathan Reynolds
var map;
var current_location;
var marker;

//Location update interval in milliseconds.
var interval = 200;

function initialize() {
  map = new google.maps.Map(document.getElementById('map'), {
    center: {lat: 0, lng: 0},
    zoom: 15
  });
  getUserLocation();
}

function getUserLocation() {
  if (navigator.geolocation){
    //Repeatedly makes calls to getCurrentPosition and sets that on the map.
    //Interval is 200ms
    setInterval(function () {
          navigator.geolocation.getCurrentPosition(setLocation);
    }, interval);
  }
  else
    document.getElementById("locationData").innerHTML = "Sorry - your browser doesn't support geolocation!";
}

function setLocation(position) {
  lat = position.coords.latitude
  long = position.coords.longitude;
  current_location = new google.maps.LatLng(lat,long);
  map.setCenter({lat: lat, lng: long})
  //If the marker has already been created
  if(marker != null){
    //update the position
    updateMarker({lat: lat, lng: long});
  }
  else{
    //otherwise, create a new marker
    createMarker({lat: lat, lng: long});
  }
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

function updateMarker(latLng) {
  marker.setPosition(latLng);
}

google.maps.event.addDomListener(window, 'load', initialize);
