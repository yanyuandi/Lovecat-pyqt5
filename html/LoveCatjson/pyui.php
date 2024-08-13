<?php
header('Content-Type: application/json'); // 设置响应为 JSON 格式

include 'db.php'; // 包含数据库连接文件

$response = array(); // 初始化响应数组

// 查询所有待办事件
$sql = "SELECT id, thing, color FROM pyqtui";
$result = $conn->query($sql);

if ($result->num_rows > 0) {
    $data = array(); // 用于存储待办事件的数组

    // 输出每个待办事件
    while ($row = $result->fetch_assoc()) {
        $data[] = array(
            'id' => $row['id'],
            'thing' => $row['thing'],
            'color' => $row['color']
        );
    }

    $response['code'] = 200; // 状态码
    $response['msg'] = '获取成功'; // 消息
    $response['data'] = $data; // 数据
} else {
    $response['code'] = 404; // 状态码
    $response['msg'] = '暂无待办事件'; // 消息
    $response['data'] = array(); // 空数据
}

$conn->close(); // 关闭数据库连接

echo json_encode($response, JSON_UNESCAPED_UNICODE); // 输出 JSON 数据