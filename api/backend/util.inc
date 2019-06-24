<?php
function url_format($urls_string, &$seen) {
  if (!$urls_string) {
    return null;
  }
  $urls = explode(" ", $urls_string);
  $result = "";
  $first = true;
  foreach ($urls as $url) {
    if (!array_key_exists($url, $seen)) {
      $seen[$url] = count($seen) + 1;
    }
    $result .= ($first ? '' : ', ') . '<a href="' . htmlspecialchars($url) . '">[' . $seen[$url] . ']</a>';
    $first = false;
  }
  return $result;
}

function formatted_notes($notes, &$seen) {
  $resList = array();
  $words = explode(" ", $notes);
  foreach ($words as $w) {
    if ((substr($w, 0, 7) === "http://") || (substr($w, 0, 8) === "https://")) {
      $resList[] = url_format($w, $seen);
    } else if ((substr($w, 0, 8) === "<http://") ||
               (substr($w, 0, 9) === "<https://")) {
      $end = strpos($w, ">");
      $resList[] = url_format(substr($w, 1, $end-1), $seen) . substr($w, $end+1);
    } else {
      $resList[] = $w;
    }
  }
  return implode(" ", $resList);
}

function link_person($person, $title_text = '', $style = '') {
  $ps = explode("; ", $person);
  $linked = array_map(
    function ($p) use ($title_text, $style) {
      return '<a href="/?person=' . urlencode($p) . '"'
        . ($title_text ? ' title="' . htmlspecialchars($title_text) . '"' : '') . $style . '>' . $p . '</a>';
    },
    $ps);
  return implode("; ", $linked);
}

function link_organization($organization) {
  return '<a href="/?organization=' . urlencode($organization) . '">'
    . $organization . '</a>';
}

function link_agenda($agenda) {
  return '<a href="/?agenda=' . urlencode($agenda) . '">'
    . $agenda . '</a>';
}

function anchorText(string $text)
{
    $text = strtolower($text);
    $text = str_replace(array('&', ','), "", $text);
    $text = preg_replace('/\s+/', '-', $text);
    $text = urlencode($text);
    return $text;
}
?>
