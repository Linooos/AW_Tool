
from .SiSwitch import *
from .SiComboBox import *
from .SiSliderBar import *
from .SiInputBox import *
from .SiMenu import *

import os
from .SiGlobal import *

# 基类 SiOption, 添加于 2024.4.4
# 所有的 SiOption 都继承这个类，该类提供了图标，文字，颜色管理，布局管理
# 物件会被添加到右侧，牺牲文字空间
class SiOption(QWidget):

    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.items = []

        # 背景
        self.background = QLabel(self)
        self.background.setStyleSheet('''
            background-color: {};
            border-radius: 4px'''.format(colorset.BG_GRAD_HEX[2]))

        # 实例化图标
        self.icon = QSvgWidget(self)
        self.icon.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.icon.setFixedSize(24, 24)

        # 实例化文字
        self.textbar = QLabel(self)
        self.textbar.setStyleSheet("background-color:transparent;")
        self.textbar.setAlignment(QtCore.Qt.AlignVCenter)
        self.textbar.setFont(SiFont.font_L1)  # 设置字体
        self.textbar.setWordWrap(False)  ## 不自动换行
        self.textbar.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.textbar.setMinimumHeight(80 - 32)

        # 可用遮罩
        self.mask = QLabel(self)
        self.mask.setStyleSheet('''
            background-color:#7f{};
            border-radius: 4px'''.format(colorset.BG_GRAD_HEX[1][1:]))
        self.mask.setVisible(False)

    def _setMinimumHeight(self, h):
        self.textbar.setMinimumHeight(h - 32)

    def addItem(self, obj, reverse = False):  # 添加右侧对象
        obj.setParent(self)
        if reverse == False:
            self.items.append(obj)
        else:
            self.items = [obj] + self.items

    def resizeEvent(self, event):
        w = event.size().width()
        h = event.size().height()

        available_width = w

        # 提前加载一些东西
        _icon_area_width = 80
        _g_text = self.textbar.geometry()

        # 更改图标的位置
        icon_x = (_icon_area_width - 24) // 2
        icon_y = (h - 24) // 2
        available_width -= _icon_area_width

        self.icon.move(icon_x, icon_y)

        # 处理自定义项，这些项目都是靠右对齐的，并且从右向左堆叠
        spacing = 16      # 控件之间的间隔，间隔将被添加到控件的左侧
        used_width = 32        # 计数器，数值代表右侧保留的宽度

        for item in self.items:
            g = item.geometry()

            item_x = w - (g.width() + used_width)
            item_y = (h - g.height()) // 2
            used_width += g.width() + spacing

            item.move(item_x, item_y)

        available_width -= used_width

        # 最后处理文本，被夹在中间，使用剩下的空间
        text_x = _icon_area_width
        text_y = 16
        text_w = available_width
        text_h = h - 16 * 2

        self.textbar.setGeometry(text_x, text_y, text_w, text_h)

        # 设置背景和遮罩的大小
        self.background.resize(w, h)
        self.mask.resize(w, h)

    def setUsability(self, status):
        self.mask.setVisible(not status)

    def setIcon(self, path):
        self.icon.load(path)

    def setText(self, title, subtitle):
        # 根据是否有副标题，设置两种文字显示方式
        if subtitle == '':
            self.textbar.setText("<font color='{}'>{}</font>".format(
                colorset.OPT_TITLE_HEX, title))
        else:
            self.textbar.setText("<font color='{}'><strong>{}</strong></font><br><font color='{}'>{}</font>".format(
                colorset.OPT_TITLE_HEX, title, colorset.OPT_DESCRIPTION_HEX, subtitle.replace('\n', '<br>')))

        # 根据文本多少，自适应调节高度
        self.textbar.adjustSize()

        # 重新设置自己的尺寸
        g = self.geometry()
        self.resize(g.width(), self.textbar.height() + 32)  #应用到这个框本身

class SiOptionLink(SiOption):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent =  parent
        

        # 设定大小
        self.btwidth = 32
        self.btheight = 32

        # 实例化按钮
        self.button = SiButtonFlat(self)
        self.button.setGeometry(0, 0, self.btwidth, self.btheight)

        # 把按钮添加到基类的 items 中
        self.items.append(self.button)

        # 把遮罩置顶
        self.mask.raise_()

    def connect(self, func):
        self.button.clicked.connect(func)  # 函数没有传入值

    def load(self, path):
        self.button.load(path)

    def setHint(self, hint):
        self.button.hint = hint


class SiOptionSourceCode(SiOptionLink):  # 源代码
    def __init__(self, parent):
        super().__init__(parent)
        self.parent =  parent
        

        self.url = 'www.baidu.com'

        self._setMinimumHeight(64)
        self.setText('源代码', '')
        self.setIcon(SiGlobal.icons.get('fi-rr-circle-small'))
        self.load(SiGlobal.icons.get('fi-rr-link'))

    def setURL(self, url):
        self.url = url
        self.button.hint = '前往 ' + url
        self.connect(lambda : os.system('start {}'.format(self.url)))

class SiOptionButton(SiOption):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent =  parent
        

        # 规定按钮的几何关系
        self.btwidth = 128
        self.btheight = 32

        # 实例化按钮
        self.button = SiButton(self)
        self.button.setGeometry(0, 0, self.btwidth, self.btheight)

        # 把按钮添加到基类的 items 中
        self.items.append(self.button)

        # 把遮罩置顶
        self.mask.raise_()

    def setText(self, title, subtitle, btntext):
        super().setText(title, subtitle)
        self.button.setText(btntext)

    def setStrong(self, option):
        self.button.setStrong(option)

    def setButtonSize(self, w, h):
        self.btwidth = w
        self.btheight = h
        self.button.setGeometry(0, 0, self.btwidth, self.btheight)

class SiOptionButtonHoldtoConfirm(SiOption):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent =  parent
        

        # 规定按钮的几何关系
        self.btwidth = 128
        self.btheight = 32

        # 实例化按钮
        self.button = SiButtonHoldtoConfirm(self)
        self.button.setGeometry(0, 0, self.btwidth, self.btheight)

        # 把按钮添加到基类的 items 中
        self.items.append(self.button)

        # 把遮罩置顶
        self.mask.raise_()

    def setText(self, title, subtitle, btntext):
        super().setText(title, subtitle)
        self.button.setText(btntext)

    def setStrong(self, option):
        self.button.setStrong(option)

    def setButtonSize(self, w, h):
        self.btwidth = w
        self.btheight = h
        self.button.setGeometry(0, 0, self.btwidth, self.btheight)


class SiOptionSwitch(SiOption):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent =  parent
        

        # 设置大小
        self.schwidth = 128
        self.schheight = 24

        # 实例化开关
        self.switch = SiSwitch(self)
        self.switch.setGeometry(0, 0, self.schwidth, self.schheight)
        self.switch.initialize_stylesheet()
        self.switch.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.switch.setFixedSize(self.schwidth, self.schheight)

        # 把开关添加到基类的 items 中
        self.items.append(self.switch)

        # 把遮罩置顶
        self.mask.raise_()

class SiOptionSliderBar(SiOption):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent =  parent
        

        # 设置大小
        self.sliwidth = 320
        self.sliheight = 16

        # 实例化滑动条
        self.sliderbar = SiSliderBar(self)
        self.sliderbar.setGeometry(0, 0, self.sliwidth, self.sliheight)

        # 把开关添加到基类的 items 中
        self.items.append(self.sliderbar)

        # 把遮罩置顶
        self.mask.raise_()

class SiOptionInputBox(SiOption):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent =  parent
        

        # 设定大小
        self.btwidth = 192
        self.btheight = 32

        # 实例化输入框
        self.inputbox = SiInputBox(self)
        self.inputbox.setGeometry(0, 0, self.btwidth, self.btheight)

        # 把输入框添加到基类的 items 中
        self.items.append(self.inputbox)

        # 把遮罩置顶
        self.mask.raise_()

class SiOptionComboBox(SiOption):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent =  parent
        

        # 设定大小
        self.btwidth = 192
        self.btheight = 32

        # 实例化输入框
        self.combobox = SiComboBox(self)
        self.combobox.setGeometry(0, 0, self.btwidth, self.btheight)

        # 把输入框添加到基类的 items 中
        self.items.append(self.combobox)

        # 把遮罩置顶
        self.mask.raise_()

    def addOption(self, name, value):
        self.combobox.addOption(name, value)

    def setOption(self, name):
        self.combobox.setOption(name)
