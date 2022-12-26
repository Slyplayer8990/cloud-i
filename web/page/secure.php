<?php
    $username = "cloudy";
    $password = "cloudy123";
    $host = "sql";
    $database = "cloudy";
    $user = $_POST["username"];
    $pass = $_POST["password"];
    $conn = new mysqli($host, $username, $password, $database);
    $mycommand = "SELECT * FROM users WHERE username = '$user' AND password = '$pass'";
    $result = $conn -> query($mycommand);
    if ($result->num_rows > 0) {
        sleep(3);
        setcookie("cloudy[user]", $user, time()+3600);
        header("Location: dashboard.php");
    }
    else {
        sleep(3);
        header("Location: index.php");
    }
    if (isset($_GET['error'])) {
        echo '<p>Invalid username or password.</p>';
    }
?>