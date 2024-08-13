import os
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QMenu, QSpacerItem, QSizePolicy
from PyQt5.QtCore import QTimer, QTime, Qt
from PyQt5.QtGui import QPixmap, QPainter, QFont, QFontDatabase, QIcon

class CountdownApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

        # 设置下班时间
        self.work_end_time = QTime(18, 00)  # 下班时间: 18:00

        # 定时器
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)  # 每秒更新一次

        # 图片序列帧的定时器
        self.frame_timer = QTimer(self)
        self.frame_timer.timeout.connect(self.update_frame)
        self.frame_timer.start(20)  # 每100毫秒更新一次帧

        # 记录鼠标位置
        self.startPos = None

        # 初始化帧索引和图片列表
        self.frame_index = 0
        self.frames = self.load_frames(os.path.join(os.path.dirname(os.path.abspath(__file__)), "03"))  # 替换为你的PNG帧文件夹
        
        # 初始化置顶状态
        self.is_topmost = True  # 默认置顶

    def initUI(self):
        self.setWindowTitle('Cat')
        self.setGeometry(100, 100, 400, 232)  # 设置固定大小为400x232
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)  # 隐藏边框并置顶
        self.setAttribute(Qt.WA_TranslucentBackground)  # 设置窗口背景透明

        # 设置任务栏图标
        current_dir = os.path.dirname(os.path.abspath(__file__))
        icon_path = os.path.join(current_dir, "ico.png")  # 替换为你的图标文件名
        self.setWindowIcon(QIcon(icon_path))  # 设置窗口图标

        # 加载自定义字体
        self.load_custom_font()

        # 创建布局和标签
        self.layout = QVBoxLayout()
        
        # 创建三个标签用于显示小时、分钟和秒
        self.hours_label = QLabel('', self)
        self.minutes_label = QLabel('', self)
        self.seconds_label = QLabel('', self)

        # 设置字体
        font = QFont("YouSheBiaoTiHei", 30, QFont.Bold)  # 使用自定义字体，字号为30，粗体
        for label in (self.hours_label, self.minutes_label, self.seconds_label):
            label.setFont(font)
            label.setAlignment(Qt.AlignVCenter)  # 设置文本垂直居中

        # 设置标签的固定宽度
        self.hours_label.setFixedWidth(60)
        self.minutes_label.setFixedWidth(60)
        self.seconds_label.setFixedWidth(60)

        # 创建水平布局并添加标签
        time_layout = QHBoxLayout()
        time_layout.addWidget(self.hours_label)
        time_layout.addItem(QSpacerItem(-33, 20, QSizePolicy.Fixed, QSizePolicy.Minimum))  # 调整小时与分钟之间的间距
        time_layout.addWidget(self.minutes_label)
        time_layout.addItem(QSpacerItem(-23, 20, QSizePolicy.Fixed, QSizePolicy.Minimum))  # 调整分钟与秒之间的间距
        time_layout.addWidget(self.seconds_label)

        # 将水平布局添加到主布局
        self.layout.addLayout(time_layout)
        self.layout.setContentsMargins(25, 94, 10, 10)  # 左、上、右、下边距
        self.setLayout(self.layout)

        # 右键菜单
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_context_menu)

    def load_custom_font(self):
        """加载自定义字体文件"""
        font_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "1.ttf")  # 替换为你的字体文件名
        font_id = QFontDatabase.addApplicationFont(font_path)
        if font_id != -1:
            family = QFontDatabase.applicationFontFamilies(font_id)[0]
            print(f"成功加载字体: {family}")
        else:
            print("加载字体失败")

    def load_frames(self, directory):
        """加载PNG序列帧"""
        frames = []
        for filename in sorted(os.listdir(directory)):
            if filename.endswith('.png'):
                frame_path = os.path.join(directory, filename)
                frames.append(QPixmap(frame_path))
        return frames

    def show_context_menu(self, pos):
        menu = QMenu(self)

        # 添加最小化和关闭操作
        minimize_action = menu.addAction("最小化")
        close_action = menu.addAction("关闭")
        
        # 添加置顶/取消置顶操作
        toggle_topmost_action = menu.addAction("取消置顶" if self.is_topmost else "置顶")

        action = menu.exec_(self.mapToGlobal(pos))

        # 执行相应的操作
        if action == minimize_action:
            self.showMinimized()  # 最小化窗口
        elif action == close_action:
            self.close()  # 关闭窗口
        elif action == toggle_topmost_action:
            self.toggle_topmost()  # 切换置顶状态

    def toggle_topmost(self):
        """切换窗口的置顶状态"""
        self.is_topmost = not self.is_topmost
        if self.is_topmost:
            self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        else:
            self.setWindowFlags(Qt.FramelessWindowHint)
        self.show()  # 更新显示

    def update_time(self):
        current_time = QTime.currentTime()
        remaining_time = current_time.secsTo(self.work_end_time)

        if remaining_time > 0:
            hours = remaining_time // 3600
            minutes = (remaining_time % 3600) // 60
            seconds = remaining_time % 60

            # 使用格式化字符串确保每个部分都是两位数
            self.hours_label.setText(f'{hours:02}')
            self.minutes_label.setText(f'{minutes:02}')
            self.seconds_label.setText(f'{seconds:02}')
        else:
            self.hours_label.setText('下')
            self.minutes_label.setText('班')
            self.seconds_label.setText('啦！')

    def update_frame(self):
        """更新显示的帧"""
        if self.frames:
            self.frame_index = (self.frame_index + 1) % len(self.frames)
            self.set_background_pixmap(self.frames[self.frame_index])

    def set_background_pixmap(self, pixmap):
        """设置窗口背景为指定的图像"""
        self.background_pixmap = pixmap
        self.update()  # 请求重绘

    def paintEvent(self, event):
        # 绘制背景图像
        painter = QPainter(self)
        if hasattr(self, 'background_pixmap') and not self.background_pixmap.isNull():
            # 计算绘制位置以居中
            img_rect = self.background_pixmap.rect()
            img_rect.moveCenter(self.rect().center())  # 将图像移动到窗口中心
            painter.drawPixmap(img_rect, self.background_pixmap)
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
