<?php
$menu_items = array(
  '<a href="/">Home</a>'
  /* '<a href="/about/">About</a>', */
  /* '<a href="/compare.php">Compare</a>' */
);

?>
<nav>
  <?= implode(", ", $menu_items) ?>
</nav>
