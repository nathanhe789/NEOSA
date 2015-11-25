<!DOCTYPE html>
<?php
$user = $_GET['u'];
?>

<html>
  <head>
    <title>Public Chat</title>
    <link rel="stylesheet" type="text/css" href="chat.css"></linK>
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/2.1.3/jquery.min.js"></script>
    <!-- <script src="//www.parsecdn.com/js/parse-1.6.7.min.js"></script>
    <script type="text/javascript" src="http://ajax.googleapis.com/ajax/libs/jquery/1.7.2/jquery.min.js"></script>
    <script type="text/javascript" src="http://www.parsecdn.com/js/parse-latest.js"></script>
    <script src="parse.js"/> -->

  </head>
  <body>
    <div class="chat_container">
        <div class="chat_header">
          <h3>Public Chat <?php echo ucwords($user);?></h3>
        </div>
        <div class="chat_messages"></div>
        <div class="chat_bottom">
          <form action="#" onsubmit="return false;" id="chat_form">
            <input type="hidden" id="name" value="<?php echo $user;?>"/>
            <input type="text" name="text" id="text" value="" placeholder="Type Your Messgae"/>
            <input type="submit" name="submit" value="Post"/>
          </form>
        </div>
    </div>
  </body>
</html>
