from PyQt5.QtCore import QSize, Qt, QProcessEnvironment
from qfluentwidgets import NavigationItemPosition, FluentWindow, SubtitleLabel,PushButton, setFont
from qfluentwidgets import FluentIcon as FIF
from PyQt5.QtWidgets import QVBoxLayout, QSizePolicy, QSpacerItem, QFileDialog
from PyQt5.QtWidgets import QFrame, QHBoxLayout, QApplication as QApplication
import sys
from PyQt5.QtGui import QIcon as QIcon
from Page import *

keep = True
t = threading.Thread(target=check_dark_theme, args=(keep,))
t.start()

class Window(FluentWindow):
    """ 主界面 """
    def __init__(self):
        super().__init__()

        # 创建子界面，实际使用时将 Widget 换成自己的子界面
        self.homeInterface = HomePage()
        self.sign = signpage()
        self.launchpad = LaunchpadPage()
        self.launchpad.setObjectName("launchpad")
        self.screenprint = ScreenPrintPage()
        self.screenprint.setObjectName("screenprint")
        self.anapplication = Widget('单应用', self)
        self.system_update = Widget('系统更新', self)
        self.system_settings = Widget('其他设置', self)
        self.system_info = system_info()
        self.initNavigation()
        self.initWindow()

    def initNavigation(self):
        self.addSubInterface(self.homeInterface, FIF.HOME, '主页')
        self.addSubInterface(self.sign, FIF.CERTIFICATE, '签名')
        self.addSubInterface(self.launchpad, FIF.APPLICATION, '启动台')
        self.addSubInterface(self.screenprint, FIF.FIT_PAGE, '截图')
        self.addSubInterface(self.anapplication, FIF.LAYOUT, '单应用')
        self.addSubInterface(self.system_update, FIF.UPDATE, '系统更新')
        self.addSubInterface(self.system_settings, FIF.TILES, '其他设置')
        self.navigationInterface.addSeparator()
        self.addSubInterface(self.system_info, FIF.INFO, '系统信息')
    def initWindow(self):
        self.resize(900,700)
        self.setWindowIcon(QIcon('./AppIcon.png'))
        self.setWindowTitle('macOS Helper')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Window()
    w.show()
    app.exec()