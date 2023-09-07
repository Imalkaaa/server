<!DOCTYPE html>
<html>

<body>
<?php
if (isset($_SERVER['REQUEST_METHOD']) && $_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['name'])) {
    $user_name = $_POST['name'];
    echo "<h1>Hello, $user_name!</h1>";
} 
?>

</body>
</html>
