<html>
 <head>
<title>Czech News Classification</title>
<meta charset="UTF-8" />
<link rel="stylesheet" type="text/css" href="./grafika.css">

</head> 
<body >

<header>

</header>

<div id="obal">

<nav>
<ul>
	<li><a href="index.html">Home</a></li>
  <li><a href="online.php">Demo</a></li>
</ul>
</nav>
<!--<rightPanel/>-->

<main>
<?php
if (isset($_POST['sum'])&&isset($_POST['text']))
{
  $socket = socket_create(AF_INET, SOCK_STREAM, SOL_TCP);
  $result = socket_connect($socket, 'xxx.xxx.xxx.xxx', 8888);
  if (!$result) { echo "<h3>Server not found.</h3> <br/>"; }
  else
  {
    $text=$_POST['text'];
    if (87552 > (strlen($text)))
    {
      socket_send($socket, $text, strlen($text), 0);
	  socket_send($socket, 0, 1, 0);
    
      $input = socket_read($socket, 87552) or die("Could not read input\n");
      $input = trim(html_entity_decode($input));
	  
	  echo "<h1>Detected class: $input</h1>";
	  echo "<h2>Text:</h2><div style='text-align:justify'>$text</div>";
    }
    else
    {
      echo "Input text is to lagre!";
    }
    socket_close($socket);
  }
}
else
{
?>
<form method="POST" action="<?php echo $_SERVER['PHP_SELF']; ?>">
	Input text:<br/>
	<textarea name="text" wrap="soft" style="width:99%" rows="30"></textarea>
	<br/>
	<table>
	<tr style="border:0px">
	<td>
	Language:</td><td><select name="jazyk">
	<option value="cs" selected="selected">čeština</option>
	<!--
	<option value="sk">slovenština</option>
	<option value="pl">polština</option>
	<option value="ru">ruština</option>
	<option value="sr">srbština</option>
	<option value="sl">slovinština</option>
	<option value="hr">chorvatština</option>
	-->
	</select></td>
	</tr>
	</table>
	<input type="submit" name="sum" value="Classify!">
	</form>
<?php
}	?>
</main>

<div class="clr"></div>
</div>

<footer>
<p>
ITE TUL
</p>
</footer>