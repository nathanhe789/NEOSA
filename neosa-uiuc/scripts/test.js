function send_key(){
  var key = $('#key').text();
  key = JSON.parse(key);
  console.log(key);

}

$(document).ready(function(){
  send_key();

});
