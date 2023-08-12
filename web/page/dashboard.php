<?php
echo "<meta name='viewport' content='width=device-width', initial-scale=1.0'/>";
if (isset ($_COOKIE["cloudy"]["user"])) {
    $user = $_COOKIE["cloudy"]["user"];
    echo "<link href='https://fonts.googleapis.com/css?family=Akaya Kanadaka' rel='stylesheet'>";
    echo "<body>";
    echo "<h1>Welcome to the dashboard, $user</h1>";
    echo "</body>";
    echo "<style>button {background-color: #4CAF50; border: none; color: white; padding: 15px 32px; text-align: right; text-decoration: none; display: inline-block; font-size: 16px; margin: 4px 2px; cursor: pointer;}</style>";
    echo "<style>h1 {text-align: left; background-color:#00b71e; color: white;}</style>";
    echo "<style>body {font-family:Akaya Kanadaka; font-size:32px;} </style>";
}
else {
    header("Location: index.php");
}
?>