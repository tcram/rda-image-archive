<?php
$page_id = $_REQUEST['page_id'];
$seen = array();
?>

<h1>Information for <?= htmlspecialchars($page_id) ?></h1>

<h2>Basic information</h2>

<table>
  <thead>
    <tr>
      <th>Item</th>
      <th>Value</th>
    </tr>
  </thead>
  <tbody>

<?php
if ($stmt = $mysqli->prepare("select * from page where page_id = ?")) {
  $stmt->bind_param("s", $page_id);
  $stmt->execute();
  $result = $stmt->get_result();
}
while ($row = $result->fetch_assoc()) { ?>
  <?php if ($page_id = ($row['page_id'] ?? '')) { ?>
    <tr>
      <td>page_id</td>
      <td><?= $page_id ?></td>
    </tr>
  <?php } ?>
  <?php if ($page_file_ext = ($row['page_file_ext'] ?? '')) { ?>
    <tr>
      <td>page_file_ext</td>
      <td><?= $page_file_ext ?></a></td>
    </tr>
  <?php } ?>
<?php } ?>
