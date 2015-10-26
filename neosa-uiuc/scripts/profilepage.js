$(document).ready(function(){
  var selected_Times = [];
;





  var isMouseDown = false;
  $("#our_table td").mousedown(function () {
    isMouseDown = true;
    //check to see if the object is going from selected to unselected
    if ($(this).hasClass( "highlighted" )){

      selected_Times.splice($(this).html())
    }
    else {
      selected_Times.push($(this).html())
    }
    $(this).toggleClass("highlighted");
  }).mouseover(function () {
      if (isMouseDown) {
        if ($(this).hasClass( "highlighted" )){

          selected_Times.splice($(this).html())
        }
        else {
          selected_Times.push($(this).html())
        }
        $(this).toggleClass("highlighted");
      }
    });

  $('#find_button_id').click(function(){
    console.log(selected_Times)
    //sending to information to a place should be placed here

  })


});
