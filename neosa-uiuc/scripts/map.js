// author Joe Tan & Jonathan Reynolds
var map;
var current_location;
var marker;
var userMarkers={};

function initialize() {
  map = new google.maps.Map(document.getElementById('map'), {
    center: {lat: 0, lng: 0},
    zoom: 15
  });
  initCenterMapButton();
  getUserLocation();
  getAllActiveUsersLatLng()
  setInterval(getAllActiveUsersLatLng, 30000);
  setUserActive();
  activateSocketIO();
}

function activateSocketIO() {
  var socket = io.connect('http://salty-shore-2311.herokuapp.com:80')
  $('form').submit(function(){
    socket.emit('chat message', $('#m').val());
    $('#m').val('');
    return false;
  });
  socket.on('chat message', function(msg){
    $('#messages').append($('<li>').text(msg));
  });
}

function setUserActive(){
  $.ajax({
    type: "POST",
    url: "/"
  });
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

  var lat = position.coords.latitude
  var long = position.coords.longitude;
  var positionData = {lat: lat, lng: long};
  var blob = JSON.stringify(positionData);
  //If the marker has already been created
  if(marker != null){
    //update the position
    updateMarker(positionData);
  }
  else{
    //otherwise, create a new marker
    var current_location = new google.maps.LatLng(lat,long);
    createMarker(current_location);
    map.setCenter(positionData);
    //Commented out since it'll be fetched from db anyways
    //createMarker(positionData);
  }
  //POST lat and long to backend
  jQuery.ajax({
    type: 'POST',
    url: "/map",
    name: "latlng",
    data: {"json":blob},
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

function createMarker(latLng) {
  var pinColor = "1aff1a";
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
}

function updateMarker(latLng) {
  marker.setPosition(latLng);
}


function getAllActiveUsersLatLng(){
  jQuery.ajax({
    type: 'GET',
    url: "/users",
    success:
    function(data){
      setUsersPositions(data.latlngArray);
    },
    error:
    function(data){
    }
  });
}

function setUsersPositions(latlngArray){
  for(var i = 0; i < latlngArray.length; i = i + 1){
    //if the userMarkers dict already has this user
    if(userMarkers.hasOwnProperty(latlngArray[i].user_id)){
      //update their marker
      updateUserMarker(latlngArray[i]);
    }
    //otherwise, create a new marker.
    else {
      createUsersMarker(latlngArray[i]);
    }
  }
}

function createUsersMarker(object){
  var latLng = object.latlng;
  var userId = object.user_id;
  var pinColor = "FE7569";
    var pinImage = new google.maps.MarkerImage("http://chart.apis.google.com/chart?chst=d_map_pin_letter&chld=%E2%80%A2|" + pinColor,
      new google.maps.Size(21, 34),
      new google.maps.Point(0,0),
      new google.maps.Point(10, 34));

    var userMarker = new google.maps.Marker({
      map: map,
      position: latLng,
      icon: pinImage,
      title: 'User: ' +userId
    });
//
  userMarkers[userId] = {"marker": userMarker};
  console.log("Creating marker for user: " + userId + "'s location.'");
  console.log(userMarkers);
}

function updateUserMarker(object) {
    var latLng = object.latlng;
    var userId = object.user_id;
    var userMarker = userMarkers[userId]["marker"];
    userMarker.setPosition(latLng);
    console.log("Updating user: " + userId + "'s location.'");
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
