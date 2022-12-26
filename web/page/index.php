<?php
    if (isset($_COOKIE["cloudy"]["user"])) {
        header("Location: dashboard.php");
    }
    echo "<meta name='viewport' content='width=device-width', initial-scale=1.0'/>";
    echo "<center>";
    echo "<h1>Please sign in.</h1>";
    echo "<form name='login' action='secure.php' method='post'>";
    echo "<p>Username: <input type='text' name='username' /></p>";
    echo "<p>Password: <input type='password' name='password' /></p>";
    echo "<p><input type='submit' name='submit' value='Login' /></p>";
    echo "</form>";
    echo "</center>";
    $parts = parse_url($url);
    parse_str($parts['query'], $query);
?>