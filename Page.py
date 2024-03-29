import platform
import subprocess
import os
import threading
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QFileDialog, QWidget, QSizePolicy, QSpacerItem, QButtonGroup, QGroupBox
from PyQt5.QtWidgets import QFrame, QHBoxLayout
from qfluentwidgets import SubtitleLabel, PushButton, MessageBox, MessageBoxBase, Theme, setTheme, MessageDialog, \
    TeachingTip, InfoBarIcon, TeachingTipTailPosition, LineEdit, RadioButton
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QFrame
import time
# 检测macOS是否为深色主题
def check_dark_theme(keep):
    result = platform.system() == 'Darwin' and subprocess.run(['defaults', 'read', '-g', 'AppleInterfaceStyle'],\
            capture_output=True).stdout.decode('utf-8').strip() == 'Dark'
    while keep:
        is_macos_dark_theme = platform.system() == 'Darwin' and subprocess.run(['defaults', 'read', '-g',\
            'AppleInterfaceStyle'],capture_output=True).stdout.decode('utf-8').strip() == 'Dark'
        if is_macos_dark_theme != result:
            if is_macos_dark_theme:
                setTheme(Theme.DARK)
            else:
                setTheme(Theme.LIGHT)
            result = is_macos_dark_theme
            time.sleep(0.1)

class Widget(QFrame):
    def __init__(self, text: str, parent=None):
        super().__init__(parent=parent)
        self.setObjectName(text.replace(' ', '-'))

class HomePage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("主页")
        self.setWindowTitle('主页')

        self.text = SubtitleLabel('这是一个含一些常用的 macOS 命令行脚本\n可以帮助您快速执行某些操作', self)
        self.button = PushButton('打开Github地址', self)

        # 设置内部元素的对象名，用于样式引用
        self.text.setObjectName('text')
        self.button.setObjectName('button')

        # 使用垂直布局改善视觉流
        layout = QVBoxLayout()
        layout.addWidget(self.text, alignment=Qt.AlignCenter)
        layout.addWidget(self.button, alignment=Qt.AlignCenter)

        self.setLayout(layout)

class signpage(Widget):
    def __init__(self, parent=None):
        super().__init__('签名', parent)

        # 优化文本显示
        self.text = SubtitleLabel('跳过签名可以解决应用运行时出现的\n「意外退出、崩溃闪退」等大多数问题。', self)
        self.text.setObjectName('text')

        # 优化按钮样式
        self.chose_button = PushButton("选择目录", self)
        self.chose_button.setObjectName('button')

        # 调整布局
        self.vBoxLayout = QVBoxLayout(self)
        self.vBoxLayout.addWidget(self.text, alignment=Qt.AlignCenter)
        self.vBoxLayout.addWidget(self.chose_button, alignment=Qt.AlignCenter)
        self.setLayout(self.vBoxLayout)

        self.chose_button.clicked.connect(self.chose_app)

    def chose_app(self):
        # 选择macOS App
        self.app_path = QFileDialog.getOpenFileName(self, '选择App', '/Applications', 'App (*.app)')[0]
        if self.app_path:
            title = '签名'
            content = """是否进行签名?
            签名后应用将无法修改。"""
            w = MessageBox(title, content, self)
            if w.exec():
                subprocess.run(['plutil', '-replace', 'C', f'{self.app_path}'])
                TeachingTip.create(
                    target=self.chose_button,
                    icon=InfoBarIcon.SUCCESS,
                    title='成功',
                    content='跳过签名完成!',
                    isClosable=True,
                    tailPosition=TeachingTipTailPosition.TOP,
                    duration=5000,
                    parent=self
                )

class LaunchpadPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('启动台')

        # Container for widgets
        main_layout = QVBoxLayout(self)
        main_layout.setAlignment(Qt.AlignCenter)
        main_layout.setContentsMargins(0, 20, 0, 20)

        # Subtitles
        about_text = SubtitleLabel('如果要调整启动台应用程序的显示行数/列数，\n可以使用此工具来实现。这对于一些大屏幕的用户来说很有用。', self)
        about_text.setStyleSheet("font-size: 14px; color: #333333;")


        tips_text = SubtitleLabel('请输入行数和列数，建议输入一个小于 30 且大于 3 的整数。', self)
        tips_text.setStyleSheet("font-size: 14px; color: #333333;")

        # Input fields layout
        input_layout = QHBoxLayout()
        input_layout.setAlignment(Qt.AlignCenter)
        input_layout.setSpacing(10)

        self.width = LineEdit()
        self.width.setPlaceholderText('列数')
        self.width.setMaximumWidth(100)
        self.width.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        self.height = LineEdit()
        self.height.setPlaceholderText('行数')
        self.height.setMaximumWidth(100)
        self.height.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        input_layout.addWidget(self.width)
        input_layout.addWidget(self.height)

        main_layout.addWidget(about_text)
        main_layout.addWidget(tips_text)
        main_layout.addLayout(input_layout)

        # Buttons layout
        button_layout = QVBoxLayout()
        button_layout.setAlignment(Qt.AlignCenter)

        self.restore_button = PushButton('恢复默认', self)
        self.restore_button.setMaximumWidth(120)
        self.restore_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        self.start_button = PushButton('执行操作', self)
        self.start_button.setMaximumWidth(120)
        self.start_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        button_layout.addWidget(self.restore_button)
        button_layout.addWidget(self.start_button)

        main_layout.addLayout(button_layout)

        self.setLayout(main_layout)

        self.start_button.clicked.connect(self.change_icon_size)
        self.restore_button.clicked.connect(self.recovery_icon_size)


    # 修改启动台图标行数/列数
    def change_icon_size(self, parent=None):
        width, height = self.width.text(), self.height.text()
        try:
            width, height = int(width), int(height)
            subprocess.run([f"defaults", "write", "com.apple.dock", "springboard-columns", "-int", f"{width}"])
            subprocess.run([f"defaults", "write", "com.apple.dock", "springboard-rows", "-int", f"{height}"])
            subprocess.run([f"defaults", "write", "com.apple.dock", "ResetLaunchPad", "-bool", "TRUE"])
            subprocess.run(["killall","Dock"])
        except:
            TeachingTip.create(
                target=self.start_button,
                icon=InfoBarIcon.WARNING,
                title='警告',
                content="请输入正确的数据类型，输入整数而不是特殊字符!",
                isClosable=True,
                tailPosition=TeachingTipTailPosition.BOTTOM,
                duration=20000,
                parent=self
            )
    # 备份启动台图标
    def recovery_icon_size(self):
        subprocess.run(["defaults","write", "com.apple.dock", "springboard-rows", "Default"])
        subprocess.run(["defaults","write", "com.apple.dock", "springboard-columns", "Default"])
        subprocess.run(["defaults","write", "com.apple.dock", "ResetLaunchPad", "-bool", "TRUE"])
        subprocess.run(["killall","Dock"])

class ScreenPrintPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('截图设置')

        layout = QVBoxLayout()

        # 截图保存路径部分
        save_path_group = QGroupBox('截图保存路径')
        save_path_layout = QHBoxLayout()
        self.PrintScreenSavePathLineEdit = LineEdit()
        self.PrintScreenSavePathLineEdit.setPlaceholderText("/Desktop")
        self.PrintScreenSavePathLineEdit.setEnabled(False)
        self.PrintScreenSavePathChosesButton = PushButton("选择保存路径")
        save_path_layout.addWidget(self.PrintScreenSavePathLineEdit)
        save_path_layout.addWidget(self.PrintScreenSavePathChosesButton)
        save_path_group.setLayout(save_path_layout)
        layout.addWidget(save_path_group)

        layout.addSpacing(20)  # 添加空白间距

        # 截图文件名前缀部分
        self.screenshot_prefix = SubtitleLabel("截图文件名前缀")
        self.screenshot_prefixLineEdit = LineEdit()
        self.screenshot_prefixLineEdit.setPlaceholderText("截图名称前缀 例如：截图")
        layout.addWidget(self.screenshot_prefix)
        layout.addWidget(self.screenshot_prefixLineEdit)

        layout.addSpacing(20)  # 添加空白间距

        # 截图格式部分
        format_group = QGroupBox('截图格式')
        format_layout = QVBoxLayout()
        self.usebmp = RadioButton('*.bmp')
        self.usejpge = RadioButton('*.jpge')
        self.usegif = RadioButton('*.gif')
        self.usepng = RadioButton('*.png')
        self.usepdf = RadioButton('*.pdf')
        self.usetiff = RadioButton('*.tiff')
        format_layout.addWidget(self.usebmp)
        format_layout.addWidget(self.usejpge)
        format_layout.addWidget(self.usegif)
        format_layout.addWidget(self.usepng)
        format_layout.addWidget(self.usepdf)
        format_layout.addWidget(self.usetiff)
        format_group.setLayout(format_layout)
        layout.addWidget(format_group)

        layout.addSpacing(20)  # 添加空白间距

        # 执行操作按钮
        self.startbutton = PushButton("执行操作")
        layout.addWidget(self.startbutton)
        self.startbutton.clicked.connect(self.start)
        layout.addStretch(1)  # 添加伸缩空间，使按钮位于底部
        self.PrintScreenSavePathChosesButton.clicked.connect(self.PrintScreenSavePathChoses)
        self.setLayout(layout)
    def start(self):
        try:
            result = None
            self.screenshot_save_path = None
            if self.usebmp.isChecked():
                result = "bmp"
            if self.usejpge.isChecked():
                result = "jpge"
            if self.usegif.isChecked():
                result = "gif"
            if self.usepng.isChecked():
                result = "png"
            if self.usepdf.isChecked():
                result = "pdf"
            if self.usetiff.isChecked():
                result = "tiff"

            if self.screenshot_prefixLineEdit != "" or self.screenshot_prefixLineEdit != None:
                subprocess.run(['defaults', 'write', 'com.apple.screencapture', 'name', self.screenshot_prefixLineEdit.text()])

            if result != None:
                subprocess.run(['defaults', 'write', 'com.apple.screencapture', 'type', result])
                print("defaults write com.apple.screencapture type "+ result)
            if self.screenshot_save_path != None or self.screenshot_save_path != "":
                subprocess.run(['defaults', 'write', 'com.apple.screencapture', 'name', self.screenshot_save_path])
            # 重启Finder
            subprocess.run(['killall', 'Finder'])
            subprocess.run(['killall', 'SystemUIServer'])
            TeachingTip.create(
                target=self.startbutton,
                icon=InfoBarIcon.SUCCESS,
                title='成功',
                content="已经成功应用了设置!",
                isClosable=True,
                tailPosition=TeachingTipTailPosition.BOTTOM,
                duration=2000,
                parent=self)

        except Exception as e:
            TeachingTip.create(
                target=self.startbutton,
                icon=InfoBarIcon.ERROR,
                title='失败',
                content=f"因为某些原因无法更改设置!\n详细原因:{e}",
                isClosable=True,
                tailPosition=TeachingTipTailPosition.BOTTOM,
                duration=20000,
                parent=self)
    def PrintScreenSavePathChoses(self):
        self.screenshot_save_path = QFileDialog.getExistingDirectory(self, "选择截图文件夹")
        self.PrintScreenSavePathLineEdit.setPlaceholderText(self.screenshot_save_path)
class system_info(Widget):
    def __init__(self, parent=None):
        super().__init__('系统信息', parent)
        # 获取CPU型号
        self.cpu_info = subprocess.run(['sysctl', '-n', 'machdep.cpu.brand_string'], stdout=subprocess.PIPE,
                                       text=True).stdout.strip()
        self.cpu_info = self.cpu_info.replace('machdep.cpu.brand_string: ', '')
        # 获取内存大小
        self.result = subprocess.run(['sysctl', '-n', 'hw.memsize'], stdout=subprocess.PIPE, text=True).stdout.strip()
        self.mem_info = int(self.result) / (1024.0 ** 3)
        self.mem_info = str(self.mem_info) + "GB"
        self.model_info = subprocess.run(['sysctl', '-n', 'hw.model'], stdout=subprocess.PIPE,
                                       text=True).stdout.strip()
        self.model_info = self.model_info.replace('hw.model: ', '')
        self.MAC_info = subprocess.run
        # 获取系统版本
        self.os_info = str(platform.mac_ver()[0])
        self.hBoxLayout = QHBoxLayout(self)
        self.label = SubtitleLabel(
            "CPU型号：" + self.cpu_info + "\n内存大小：" + self.mem_info + \
            "\n系统版本：" + self.os_info + "\n机型：" + self.model_info,self)
        self.label.setAlignment(Qt.AlignCenter)
        self.hBoxLayout.addWidget(self.label, 1, Qt.AlignCenter)
