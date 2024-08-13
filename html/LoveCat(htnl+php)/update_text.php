<?php
// update_text.php
$host = '替换自己数据库主机'; // 数据库主机
$db   = 'pyui';      // 数据库名
$user = '替换自己数据库用户名'; // 数据库用户名
$pass = '替换自己数据库密码'; // 数据库密码
$charset = 'utf8mb4';

$dsn = "mysql:host=$host;dbname=$db;charset=$charset";
$options = [
    PDO::ATTR_ERRMODE            => PDO::ERRMODE_EXCEPTION,
    PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC,
    PDO::ATTR_EMULATE_PREPARES   => false,
];

try {
    $pdo = new PDO($dsn, $user, $pass, $options);
} catch (\PDOException $e) {
    throw new \PDOException($e->getMessage(), (int)$e->getCode());
}

// 获取 AJAX 请求的数据
$action = $_POST['action'] ?? '';
$id = $_POST['id'] ?? null;
$content = $_POST['content'] ?? '';

if ($action === 'update' && $id !== null) {
    // 更新文本内容
    $stmt = $pdo->prepare("UPDATE pyqtui SET thing = ? WHERE id = ?");
    $stmt->execute([$content, $id]);
    echo json_encode(['status' => 'success']);
} elseif ($action === 'delete' && $id !== null) {
    // 删除文本内容
    $stmt = $pdo->prepare("DELETE FROM pyqtui WHERE id = ?");
    $stmt->execute([$id]);
    echo json_encode(['status' => 'success']);
} elseif ($action === 'add' && !empty($content)) {
    // 添加新文本内容
    $stmt = $pdo->prepare("INSERT INTO pyqtui (thing) VALUES (?)");
    $stmt->execute([$content]);
    echo json_encode(['status' => 'success']);
} else {
    echo json_encode(['status' => 'error', 'message' => 'Invalid request']);
}
?>
