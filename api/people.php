<?php
  include_once("backend/globalVariables/passwordFile.inc");
  $query = "select distinct(page_id) as name from page'";
  if ($stmt = $mysqli->prepare($query)) {
    $stmt->execute();
    $result = $stmt->get_result();
  }

  $pages = array();
  while ($row = $result->fetch_assoc()) {
    $pages[] = $row['name'];
  }

  sort($pages);

  print "<!DOCTYPE html>\n";
  print '<html lang="en">';
  print "<head>";
  print "<title>List of all pages</title>";
  print "</head>";
  print "<pre>";
  foreach ($pages as $page) {
    print '<a href="/?page=' . urlencode($page) . '">' . $page. "</a>\n";
  }
  print "</pre>";
  print "</html>";
