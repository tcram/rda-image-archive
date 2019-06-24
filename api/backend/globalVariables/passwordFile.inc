<?php
$mysqli = new mysqli("127.0.0.1", "root", "steveaokiinthehouse858", "aiwatch");
$mysqli->set_charset("utf8");

// This determines which site we are running on, e.g. aiwatch.issarice.com vs
// orgwatch.issarice.com
$subdomain = explode(".", $_SERVER['SERVER_NAME'])[0] ?? 'aiwatch';
?>
