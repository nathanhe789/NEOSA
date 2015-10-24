// author Joe Tan & Jonathan Reynolds
var map;
var current_location;
var marker;

//Location update interval in milliseconds.
var interval = 10000;

function initialize() {
  map = new google.maps.Map(document.getElementById('map'), {
    center: {lat: 0, lng: 0},
    zoom: 15
  });
  initCenterMapButton();
  getUserLocation();
  createAllMarker();
}

function getAllUsersLatLng(){
  latlng = $('#latlng').text();
  // console.log(latlng);
  latlng = JSON.parse(latlng);
  // console.log(latlng);
  return latlng;

}

function getUserLocation() {
  if (navigator.geolocation){
    /*
     * REPLACE setInterval with HTML5 watchPosition. Should be a
     * a cleaner implementation of what we want.
     */
     var options = {
       enableHighAccuracy: true
     }
     function error(err) {
       console.warn('ERROR(' + err.code + '): ' + err.message);
     }
    navigator.geolocation.watchPosition(setLocation, error, options);
  }
  else
    document.getElementById("locationData").innerHTML = "Sorry - your browser doesn't support geolocation!";
}

function setLocation(position) {

  lat = position.coords.latitude
  long = position.coords.longitude;
  positionData = {lat: lat, lng: long};
  //If the marker has already been created
  if(marker != null){
    //update the position
    updateMarker(positionData);
  }
  else{
    //otherwise, create a new marker
    current_location = new google.maps.LatLng(lat,long);
    map.setCenter(positionData);
    createMarker(positionData);
  }
  //POST lat and long to backend
  jQuery.ajax({
    type: 'POST',
    url: "/map",
    name: "latlng",
    data: positionData,
    success:
    function(data){
      // console.log(data);
    },
    error:
    function(data){
      // console.log(data);
    }
  });
}

function ClearMarker() {
  if(marker != null ){
    marker.setMap(null);
  }
  marker = null;
}

function createAllMarker(){
  userlatlngs = getAllUsersLatLng();
  for(var i = 0; i < userlatlngs.length; i++){
    console.log(userlatlngs[i]);
    // var marker = new google.maps.Marker({
    //   map: map,
    //   position: place.geometry.location
    // bounds.extend(marker.getPosition());
    // map.fitBounds(bounds);
    // });
  }
}

function createMarker(latLng) {
  var pinColor = "FE7569";
  var pinImage = new google.maps.MarkerImage("http://chart.apis.google.com/chart?chst=d_map_pin_letter&chld=%E2%80%A2|" + pinColor,
    new google.maps.Size(21, 34),
    new google.maps.Point(0,0),
    new google.maps.Point(10, 34));

  marker = new google.maps.Marker({
    map: map,
    position: latLng,
    icon: pinImage,
    title: 'You'
  });
  console.log(latLng);
}

function updateMarker(latLng) {
  marker.setPosition(latLng);
}

/**
 * The CenterControl adds a control to the map that recenters the map on a given location.
 * This constructor takes the control DIV as an argument.
 * @constructor
 */
function CenterControl(controlDiv, map) {

  // Set CSS for the control border.
  var controlUI = document.createElement('div');
  controlUI.style.backgroundColor = '#fff';
  controlUI.style.border = '2px solid #fff';
  controlUI.style.borderRadius = '3px';
  controlUI.style.boxShadow = '0 2px 6px rgba(0,0,0,.3)';
  controlUI.style.cursor = 'pointer';
  controlUI.style.marginBottom = '22px';
  controlUI.style.textAlign = 'center';
  controlUI.title = 'Click to recenter the map';
  controlDiv.appendChild(controlUI);

  // Set CSS for the control interior.
  var controlText = document.createElement('div');
  controlText.style.color = 'rgb(25,25,25)';
  controlText.style.fontFamily = 'Roboto,Arial,sans-serif';
  controlText.style.fontSize = '16px';
  controlText.style.lineHeight = '38px';
  controlText.style.paddingLeft = '5px';
  controlText.style.paddingRight = '5px';
  controlText.innerHTML = 'Center Map';
  controlUI.appendChild(controlText);

  // Setup the click event listeners: simply set the map to Chicago.
  controlUI.addEventListener('click', function() {
    map.setCenter(marker.getPosition());
  });

}

function initCenterMapButton() {

  // Create the DIV to hold the control and call the CenterControl() constructor
  // passing in this DIV.
  var centerControlDiv = document.createElement('div');
  var centerControl = new CenterControl(centerControlDiv, map);

  centerControlDiv.index = 1;
  map.controls[google.maps.ControlPosition.TOP_CENTER].push(centerControlDiv);
}

google.maps.event.addDomListener(window, 'load', initialize);
