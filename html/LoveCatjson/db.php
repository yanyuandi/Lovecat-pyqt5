<?php
    // 连接数据库
    $conn = new mysqli('替换自己数据库主机', '替换自己数据库用户名', '替换自己数据库密码', 'pyui');

    if ($conn->connect_error) {
        die("连接失败: " . $conn->connect_error);
    }
?>