<!DOCTYPE html>
<html lang="en">
<?php
include_once("backend/globalVariables/passwordFile.inc");
$head_date = trim(file_get_contents("head_date.txt"));
$title = "";
if ($_REQUEST['page'] ?? '') {
  $title = htmlspecialchars($_REQUEST['page']);
}
$site_name = "RDA Image Archive";
?>

<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=yes">
  <meta name="dcterms.date" content="<?= $head_date ?>">
  <meta property="og:title" content="<?= $title ? $title : $site_name ?>" />
  <meta property="og:site_name" content="<?= $site_name ?>" />
  <meta property="og:locale" content="en_US" />
  <title><?= $title ? $title . " - " . $site_name : $site_name ?></title>
  <link rel="stylesheet" href="/tablesorter.css">
  <script src="/jquery.min.js"></script>
  <script src="/jquery.tablesorter.js"></script>
  <script src="/anchor.min.js"></script>
<?php include_once("style.inc"); ?>
<?php include_once("analytics.inc"); ?>
</head>

<body>
<?php include_once("navbar.inc"); ?>
<?php
include_once("backend/util.inc");
include_once("backend/page.inc");
?>
<h1><?= $site_name ?></h1>

<p>
  This is a website to catalog historical climate documents.
  See the <a href="https://github.com/ncar/rda-image-archive">code repository</a>
  for the source code and data of this website.
</p>

<p>Last updated on <?= $head_date ?>.</p>

<h2 id="table-of-contents">Table of contents</h2>

<ul>
<li><a href="#positions-summary-by-year">Positions summary by year</a></li>
<li><a href="#positions-grouped-by-person">Positions grouped by person</a></li>
<li><a href="#positions-grouped-by-organization">Positions grouped by organization</a></li>
<li><a href="#individuals-not-affiliated-with-any-organization">Individuals
  not affiliated with any organization</a></li>
<li><a href="#products">Products</a></li>
</ul>

<script>
    $(function(){$("table").tablesorter();});
    anchors.add();
</script>
</body>
</html>
