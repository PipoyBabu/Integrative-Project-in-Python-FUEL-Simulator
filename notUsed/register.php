<?php

$conn = new mysqli("localhost", "root", "", "fleet_db");

if ($_SERVER["REQUEST_METHOD"] == "POST") {

    $fullname = $_POST['fullname'] ?? '';
    $email = $_POST['email'] ?? '';
    $password = $_POST['password'] ?? '';

    if (!$fullname || !$email || !$password) {
        echo "empty";
        exit;
    }

    // check if email exists
    $check = $conn->query("SELECT * FROM users WHERE email='$email'");
    if ($check->num_rows > 0) {
        echo "exists";
        exit;
    }

    $sql = "INSERT INTO users (fullname, email, password)
            VALUES ('$fullname', '$email', '$password')";

    if ($conn->query($sql)) {
        echo "success";
    } else {
        echo "error";
    }
}
?>