<?php
include_once("../backend/globalVariables/passwordFile.inc");
$site_name = "RDA Image Archive";
?>
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=yes">
  <meta name="dcterms.date" content="2019-06-24">
  <meta property="og:title" content="About" />
  <meta property="og:site_name" content="<?= $site_name ?>" />
  <meta property="og:locale" content="en_US" />
  <title>About - <?= $site_name ?></title>
  <link rel="stylesheet" href="/tablesorter.css">
  <script src="/jquery.min.js"></script>
  <script src="/jquery.tablesorter.js"></script>
  <script src="/anchor.min.js"></script>
<?php include_once("../style.inc"); ?>
<?php include_once("../analytics.inc"); ?>
</head>
<body>
<?php include_once("../navbar.inc"); ?>

<h1>About</h1>

<script>
    $(function(){$("table").tablesorter();});
    anchors.add();
</script>
</body>
</html>
