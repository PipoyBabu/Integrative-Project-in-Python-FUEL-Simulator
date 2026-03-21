<?php

$conn = new mysqli("localhost", "root", "", "fleet_db");

if ($_SERVER["REQUEST_METHOD"] == "POST") {

    $email = $_POST['email'] ?? '';
    $password = $_POST['password'] ?? '';

    if (!$email || !$password) {
        echo "empty";
        exit;
    }

    $result = $conn->query("SELECT * FROM users WHERE email='$email'");

    if ($result->num_rows == 0) {
        echo "notfound";
        exit;
    }

    $user = $result->fetch_assoc();

    if ($user['password'] === $password) {
        echo "success";
    } else {
        echo "wrong";
    }
}
?>