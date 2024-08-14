<?php
// 数据库连接配置
$host = '替换自己数据库主机'; // 数据库主机
$db   = 'pyui';      // 数据库名
$user = '替换自己数据库用户名'; // 数据库用户名
$pass = '替换自己数据库密码'; // 数据库密码
$charset = 'utf8mb4';

// 数据库连接
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

// 从数据库获取数据
$stmt = $pdo->query("SELECT * FROM pyqtui");
$texts = $stmt->fetchAll();
?>

<!DOCTYPE html>
<html lang="zh">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    //下面这个ico为创建手机桌面应用时用到的
    <link rel="apple-touch-icon-precomposed" sizes="120x120" href="http://你的域名/ico.png">
    <link rel="shortcut icon" href="favicon.ico" type="image/x-icon">
    <link rel="icon" href="favicon.ico" type="image/x-icon">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, minimal-ui" />
    <meta name="apple-mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent" />
    <title>LOVECAT</title>
    <link rel="stylesheet" href="styles.css">
    <style>
        .button-container {
            display: none;
        }

        .input-box {
            display: none;
        }

        .add-container {
            display: none;
            margin-top: 20px;
        }
    </style>
</head>

<body>
    <div class="container">
        <img src="logo.png" alt="logo" class="logo-image" id="logoImage" />
        <input type="text" id="inputBox" class="input-box" maxlength="18"/>

        <div class="button-container">
            <button id="completeButton" class="button">完成</button>
            <button id="deleteButton" class="button">删除</button>
        </div>

        <div class="add-container">
            <input type="text" id="newInput" class="new-input-box" placeholder="输入新内容" maxlength="18"/>
            <div class="button-container-add">
            <button id="addButton" class="button">添加</button>
        
        </div>
        </div>

        <div class="add-item-overlay" id="addItemButton"></div>



        <?php foreach ($texts as $index => $text): ?>
        <div class="additional-text text<?php echo $index + 1; ?>" id="text<?php echo $index + 1; ?>" data-id="<?php echo $text['id']; ?>"><?php echo htmlspecialchars($text['thing']); ?></div>
        <?php endforeach; ?>
    </div>
        <div class="footer">
    Design by YYD@2024
</div>
    <script>
        const inputBox = document.getElementById('inputBox');
        const completeButton = document.getElementById('completeButton');
        const deleteButton = document.getElementById('deleteButton');
        const buttonContainer = document.querySelector('.button-container');
        const addItemButton = document.getElementById('addItemButton');
        const newInput = document.getElementById('newInput');
        const addButton = document.getElementById('addButton');
        const addContainer = document.querySelector('.add-container');
        let currentTextElement = null;

        // 通用函数用于处理文字点击
        function handleTextClick(textElement) {
            currentTextElement = textElement;
            inputBox.value = textElement.textContent;
            inputBox.style.display = 'block';
            buttonContainer.style.display = 'block';
            inputBox.focus();
        }

        // 获取所有额外文字元素并添加事件
        document.querySelectorAll('.additional-text').forEach(textElement => {
            textElement.addEventListener('click', () => {
                handleTextClick(textElement);
            });
        });

        // 完成按钮点击事件
        completeButton.addEventListener('click', () => {
            //console.log('完成按钮被点击');
            if (currentTextElement) {
                const currentId = currentTextElement.dataset.id;
                const updatedContent = inputBox.value;

                //console.log(`更新文本ID: ${currentId}, 新内容: ${updatedContent}`);

                currentTextElement.textContent = updatedContent;
                inputBox.style.display = 'none';
                buttonContainer.style.display = 'none';
                currentTextElement = null;

                // 发送 AJAX 请求更新数据库
                fetch('update_text.php', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/x-www-form-urlencoded',
                        },
                        body: new URLSearchParams({
                            action: 'update',
                            id: currentId,
                            content: updatedContent
                        })
                    })
                    .then(response => response.json())
                    .then(data => {
                        //console.log('更新响应:', data);
                        if (data.status !== 'success') {
                            console.error('更新失败:', data.message);
                        }
                    })
                    .catch(error => {
                        console.error('请求失败:', error);
                    });
            } else {
                //console.log('没有选择任何文本元素进行更新。');
            }
        });

        // 删除按钮点击事件
        deleteButton.addEventListener('click', () => {
            if (currentTextElement) {
                const currentId = currentTextElement.dataset.id;

                //console.log(`删除文本ID: ${currentId}`);

                fetch('update_text.php', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/x-www-form-urlencoded',
                        },
                        body: new URLSearchParams({
                            action: 'delete',
                            id: currentId
                        })
                    })
                    .then(response => {
                        if (!response.ok) {
                            throw new Error('网络响应不正常');
                        }
                        return response.json();
                    })
                    .then(data => {
                        //console.log('删除响应:', data);
                        if (data.status !== 'success') {
                            console.error('删除失败:', data.message);
                        } else {
                            location.reload();
                        }
                    })
                    .catch(error => {
                        console.error('请求失败:', error);
                    });
            } else {
                //console.log('没有选择任何文本元素进行删除。');
            }
        });

        // 输入框失去焦点时隐藏
        inputBox.addEventListener('blur', () => {
            if (currentTextElement) {
                setTimeout(() => {
                    if (!buttonContainer.contains(document.activeElement)) {
                        inputBox.style.display = 'none';
                        buttonContainer.style.display = 'none';
                        currentTextElement = null;
                    }
                }, 0);
            }
        });

        // 新输入框失去焦点时隐藏
        newInput.addEventListener('blur', () => {
            setTimeout(() => {
                if (!addContainer.contains(document.activeElement)) {
                    addContainer.style.display = 'none'; // 隐藏添加容器
                }
            }, 0);
        });

        // 在按钮上添加 mousedown 事件
        completeButton.addEventListener('mousedown', (event) => {
            event.preventDefault();
        });

        deleteButton.addEventListener('mousedown', (event) => {
            event.preventDefault();
        });

        // 按下 Enter 键时隐藏输入框并更新文字
        inputBox.addEventListener('keydown', (event) => {
            if (event.key === 'Enter') {
                completeButton.click();
            }
        });

        // 按下 Enter 键时隐藏输入框并更新文字
        newInput.addEventListener('keydown', (event) => {
            if (event.key === 'Enter') {
                addButton.click();
            }
        });

        // 添加按钮点击事件
        addItemButton.addEventListener('click', () => {
            addContainer.style.display = 'block'; // 显示添加容器
            newInput.value = ''; // 清空输入框
            newInput.focus(); // 聚焦到输入框
        });

        // 添加按钮点击事件
        addButton.addEventListener('click', () => {
            // 检查当前的文本行数
            const currentCount = document.querySelectorAll('.additional-text').length;
            if (currentCount >= 4) {
                alert('已经到四行了，请删除一行后继续添加'); // 提示用户
                addContainer.style.display = 'none'; // 隐藏添加容器
                return; // 阻止继续执行
            }


            const newContent = newInput.value; // 获取输入框的值
            if (newContent.trim() === '') {
                alert('请输入内容。'); // 如果输入框为空，提示用户
                addContainer.style.display = 'none'; // 隐藏添加容器
                return;
            }
        
            // 禁用添加按钮以避免重复提交
            addButton.disabled = true;
        
            // 发送 AJAX 请求添加新数据
            fetch('update_text.php', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: new URLSearchParams({
                    action: 'add',
                    content: newContent
                })
            })
            .then(response => response.json())
            .then(data => {
                 //console.log('添加响应:', data);
                if (data.status === 'success') {
                    location.reload(); // 刷新页面
                } else {
                     console.error('添加失败:', data.message);
                    alert('添加失败：' + data.message); // 提示用户失败信息
                }
            })
            .catch(error => {
                 console.error('请求失败:', error);
                alert('请勿多次点击添加按钮'); // 提示用户请求失败
            })
            .finally(() => {
                // 恢复添加按钮以允许再次提交
                addButton.disabled = false;
            });
        });

           // 禁止滚动的函数
        function preventScroll(e) {
            e.preventDefault(); // 阻止默认的滚动行为，在手机端模拟app页面
        }

        // 添加事件监听器以禁止滚动
        window.addEventListener('wheel', preventScroll, { passive: false });
        window.addEventListener('touchmove', preventScroll, { passive: false });
        
        document.getElementById('logoImage').addEventListener('click', function() {
        location.reload(); // 刷新页面
        });
    </script>
</body>

</html>
