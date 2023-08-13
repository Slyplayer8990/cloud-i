<?php
echo "<meta name='viewport' content='width=device-width', initial-scale=1.0'/>";
if (isset ($_COOKIE["cloudy"]["user"])) {
    $user = $_COOKIE["cloudy"]["user"];
    echo "<link href='https://fonts.googleapis.com/css?family=Akaya Kanadaka' rel='stylesheet'>";
    echo "<body>";
    echo "<div style='clear:both;' class='header-container'>";
    echo "<h1 style='text-align: left; display: inline-block;' class='right-header'>Welcome to the dashboard, $user</h1>";
    echo "<button style='display: inline-block; float: right;' class='right-header' onclick='window.location.href=\"logout.php\"'>Logout</button>";
    echo "</div>";
    echo "</body>";
    echo "<style>.header-container {padding: 10px; justify-content: space-between; display:flex}</style>";
    echo "<style>body {font-family:Akaya Kanadaka; font-size:32px;} </style>";
    echo "<style>.right-header {float: right;}</style>";
}
else {
    header("Location: index.php");
}
?>