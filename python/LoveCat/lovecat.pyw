import os
import sys
import requests
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QMenu, QPushButton
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QPixmap, QPainter, QFont, QIcon

class CountdownApp(QWidget):
    def __init__(self):
        super().__init__()

        # 初始化标签列表
        self.labels = []

        # 图片序列相关变量
        self.image_sequence = []
        self.current_image_index = 0
        self.image_change_interval = 40  # 图片切换间隔（毫秒）

        self.initUI()

        # 定时器
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_data)
        self.timer.start(10000)  # 每10秒更新一次

        # 定时器用于切换图片
        self.image_timer = QTimer(self)
        self.image_timer.timeout.connect(self.change_background_image)
        self.image_timer.start(self.image_change_interval)  # 每40ms切换一次图片

        # 记录鼠标位置
        self.startPos = None
        self.update_data()  # 初始化时获取数据

        # 加载图片序列
        self.load_image_sequence("01")  # 加载01文件夹的PNG序列

        # 置顶状态
        self.is_topmost = True  # 初始状态为置顶
        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)  # 确保窗口置顶

    def initUI(self):
        self.setWindowTitle('LOVECAT')
        self.setGeometry(1000, 0, 400, 232)  # 设置固定大小为400x232
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)  # 隐藏边框并置顶
        self.setAttribute(Qt.WA_TranslucentBackground)  # 设置窗口背景透明

        # 设置任务栏图标
        current_dir = os.path.dirname(os.path.abspath(__file__))
        icon_path = os.path.join(current_dir, "ico.png")  # 替换为你的图标文件名
        self.setWindowIcon(QIcon(icon_path))  # 设置窗口图标

        # 创建布局
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.layout.setContentsMargins(10, 100, 10, 10)  # 左、上、右、下边距

        # 创建最多四个标签，初始化为空
        for _ in range(4):
            label = QLabel('', self)
            label.setFont(QFont("微软雅黑", 16, QFont.Bold))  # 设置字体
            label.setWordWrap(True)  # 允许文本换行
            label.setAlignment(Qt.AlignCenter)  # 设置文本居中对齐
            
            self.labels.append(label)  # 添加到标签列表
            self.layout.addWidget(label)  # 添加到布局

        # 设置按钮路径与背景图相同
        close_icon_path = os.path.join(current_dir, "close.png")  # 使用与4.png相同的目录
        hide_path = os.path.join(current_dir, "hide.png")  # 使用与4.png相同的目录
        top_path = os.path.join(current_dir, "top.png")  # 使用与4.png相同的目录
        top_done_path = os.path.join(current_dir, "topdone.png")  # 置顶完成图标

        # 检查图标文件是否有效
        if not os.path.exists(close_icon_path):
            print(f"错误: 找不到图标文件 {close_icon_path}")
        if not os.path.exists(top_done_path):  # 检查置顶完成图标
            print(f"错误: 找不到图标文件 {top_done_path}")

        # 添加按钮
        self.pushButton = QPushButton(self)
        self.pushButton.setGeometry(50, 69, 19, 19)  # 设置按钮的大小和位置
        self.pushButton_hide = QPushButton(self)
        self.pushButton_hide.setGeometry(32, 69, 19, 19)  # 设置按钮的大小和位置
        self.pushButton_top = QPushButton(self)
        self.pushButton_top.setGeometry(14, 69, 19, 19)  # 设置按钮的大小和位置

        # 使用 QPixmap 加载图标
        pixmap = QPixmap(close_icon_path)
        pixmap_hide = QPixmap(hide_path)
        pixmap_top_done = QPixmap(top_done_path)  # 使用置顶完成图标

        if pixmap.isNull():
            print(f"错误: 图标文件 {close_icon_path} 无法加载")
        else:
            self.pushButton.setIcon(QIcon(pixmap))  # 设置按钮图标
            self.pushButton.setIconSize(pixmap.size())  # 设置图标大小与原图一致
            
        if pixmap_hide.isNull():
            print(f"错误: 图标文件 {hide_path} 无法加载")
        else:
            self.pushButton_hide.setIcon(QIcon(pixmap_hide))  # 设置按钮图标
            self.pushButton_hide.setIconSize(pixmap_hide.size())  # 设置图标大小与原图一致

        if pixmap_top_done.isNull():
            print(f"错误: 图标文件 {top_done_path} 无法加载")
        else:
            self.pushButton_top.setIcon(QIcon(pixmap_top_done))  # 设置按钮图标为置顶完成图标
            self.pushButton_top.setIconSize(pixmap_top_done.size())  # 设置图标大小与原图一致

        # 设置按钮样式，保持透明背景并添加 hover 效果
        self.pushButton.setStyleSheet("""
            QPushButton {
                background-color: rgba(0, 0, 0, 0);
            }
            QPushButton:hover {
                padding-bottom:3px;
  /* Hover 背景效果，可自定义 */
            }
        """)

        self.pushButton_hide.setStyleSheet("""
            QPushButton {
                background-color: rgba(0, 0, 0, 0);
            }
            QPushButton:hover {
                padding-bottom:3px;
            }
        """)

        self.pushButton_top.setStyleSheet("""
            QPushButton {
                background-color: rgba(0, 0, 0, 0);
            }
            QPushButton:hover {
                padding-bottom:3px;
            }
        """)

        self.pushButton.clicked.connect(self.close)  # 连接按钮点击事件
        self.pushButton_hide.clicked.connect(self.showMinimized)  # 连接按钮点击事件以最小化窗口
        self.pushButton_top.clicked.connect(self.toggle_topmost)  # 连接置顶按钮点击事件

        # 右键菜单
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_context_menu)

    def toggle_topmost(self):
        """切换窗口的置顶状态"""
        self.is_topmost = not self.is_topmost
        if self.is_topmost:
            self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)  # 置顶
            self.pushButton_top.setIcon(QIcon(os.path.join(os.path.dirname(os.path.abspath(__file__)), "topdone.png")))  # 设置置顶完成图标
        else:
            self.setWindowFlags(self.windowFlags() & ~Qt.WindowStaysOnTopHint)  # 取消置顶
            self.pushButton_top.setIcon(QIcon(os.path.join(os.path.dirname(os.path.abspath(__file__)), "top.png")))  # 恢复原图标
        self.show()  # 更新窗口显示

    def load_image_sequence(self, folder):
        """加载指定文件夹中的所有PNG图片"""
        try:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            folder_path = os.path.join(current_dir, folder)
            for filename in sorted(os.listdir(folder_path)):
                if filename.endswith('.png'):
                    image_path = os.path.join(folder_path, filename)
                    pixmap = QPixmap(image_path)
                    if not pixmap.isNull():
                        self.image_sequence.append(pixmap)
            if not self.image_sequence:
                print("没有找到有效的PNG图片。")
        except Exception as e:
            print(f"加载图片序列时出错: {e}")

    def change_background_image(self):
        """切换背景图片"""
        if self.image_sequence:
            self.current_image_index = (self.current_image_index + 1) % len(self.image_sequence)
            self.update()  # 请求重新绘制

    def show_context_menu(self, pos):
        menu = QMenu(self)
        close_action = menu.addAction("关闭")
        minimize_action = menu.addAction("最小化")  # 添加最小化选项
        action = menu.exec_(self.mapToGlobal(pos))
        
        if action == close_action:
            self.close()
        elif action == minimize_action:
            self.showMinimized()  # 执行最小化操作

    def update_data(self):
        """从指定网址获取数据并更新标签内容"""
        url = "http://你的域名/pyui.php"  # 替换为你的实际网址

        # 先清空所有标签
        for label in self.labels:
            label.setText('')  # 清空标签文本
            
        try:
            response = requests.get(url)
            response.raise_for_status()  # 检查请求是否成功
            json_data = response.json()

            if json_data.get("code") == 200 and json_data["data"]:
                data = json_data["data"]

                # 更新每个标签的文本和颜色，最多显示四个
                for i in range(min(4, len(data))):
                    thing = data[i]["thing"]
                    color = data[i]["color"]
                    self.labels[i].setText(thing)
                    self.labels[i].setStyleSheet(f"color: white;")  # 设置文本颜色
            else:
                # 如果数据为空或其他错误，显示一行获取数据失败
                self.labels[0].setText("暂时没有数据哦~")
                self.labels[0].setStyleSheet("color: black;")  # 设置颜色为黑色

        except Exception as e:
            print(f"获取数据时出错: {e}")
            self.labels[0].setText("获取数据失败!")  # 只在第一行显示错误消息
            self.labels[0].setStyleSheet("color: black;")  # 设置颜色为黑色

    def paintEvent(self, event):
        # 绘制背景图片
        painter = QPainter(self)
        if self.image_sequence:
            # 绘制当前的图片
            painter.drawPixmap(self.rect(), self.image_sequence[self.current_image_index])
        else:
            painter.fillRect(self.rect(), Qt.lightGray)  # 如果没有背景图，填充灰色

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.startPos = event.globalPos() - self.frameGeometry().topLeft()
        event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton and self.startPos is not None:
            self.move(event.globalPos() - self.startPos)
        event.accept()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.startPos = None
        event.accept()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    countdown_app = CountdownApp()
    countdown_app.show()
    sys.exit(app.exec_())
