from PyQt5.QtCore import pyqtSignal, Qt

from siui.core.globals import SiGlobal
from siui.components.widgets import SiLabel, SiToggleButton
from siui.components.widgets.abstracts import ABCSiNavigationBar
from siui.components.widgets import SiDenseHContainer, SiDenseVContainer, SiStackedContainer
from siui.core.color import SiColor


class PageButton(SiToggleButton):
    activated = pyqtSignal()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # 设置自身样式
        self.setBorderRadius(6)
        #self.colorGroup().assign(SiColor.BUTTON_OFF, "#00FFFFFF")
        #self.colorGroup().assign(SiColor.BUTTON_ON, "#10FFFFFF")

        # 创建高光指示条，用于指示被选中
        self.active_indicator = SiLabel(self)
        self.active_indicator.setFixedStyleSheet("border-radius: 2px")
        self.active_indicator.resize(4, 20)
        self.active_indicator.setOpacity(0)

        # 绑定点击事件到切换状态的方法
        self.clicked.connect(self._on_clicked)

        # 设置自身索引
        self.index_ = -1

    def reloadStyleSheet(self):
        super().reloadStyleSheet()
        self.active_indicator.setStyleSheet(
            f"background-color: {self.colorGroup().fromToken(SiColor.THEME)}"
        )

    def setActive(self, state):
        """
        设置激活状态
        :param state: 状态
        """
        self.setChecked(state)
        self.active_indicator.setOpacityTo(1 if state is True else 0)
        if state is True:
            self.activated.emit()

    def setIndex(self, index: int):
        """
        设置索引
        """
        self.index_ = index

    def index(self):
        """
        获取自身索引
        :return: 索引
        """
        return self.index_

    def on_index_changed(self, index):
        if index == self.index():
            self.setChecked(True)
            self.active_indicator.setOpacityTo(1)

    def _on_clicked(self):
        self.setActive(True)

        # 遍历统一父对象下的所有同类子控件，全部设为未激活
        for obj in self.parent().children():
            if isinstance(obj, PageButton) and obj != self:
                obj.setActive(False)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.active_indicator.move(0, (self.height() - self.active_indicator.height()) // 2)


class PageNavigator(ABCSiNavigationBar):
    """
    页面导航栏
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # 清空自己的样式表防止继承
        self.setStyleSheet("")

        # 创建容器用于放置按钮
        self.container = SiDenseVContainer(self)
        self.container.setSpacing(8)
        self.container.setAlignment(Qt.AlignCenter)

        # 所有按钮
        self.buttons = []
        self.sideList = []

    def addPageButton(self, svg_data, hint, func_when_active, side="top"):
        """
        添加页面按钮
        :param svg_data: 按钮的 svg 数据
        :param hint: 工具提示
        :param func_when_active: 当被激活时调用的函数
        :param side: 添加在哪一侧
        """
        new_page_button = PageButton(self)
        new_page_button.setIndex(self.maximumIndex())
        new_page_button.setStyleSheet("background-color: {};".format(self.colorGroup().fromToken(SiColor.INTERFACE_BG_F)))

        new_page_button.resize(40, 40)
        new_page_button.setHint(hint)
        new_page_button.attachment().setSvgSize(20, 20)
        new_page_button.attachment().load(svg_data)
        new_page_button.activated.connect(func_when_active)

        # 绑定索引切换信号，当页面切换时，会使按钮切换为 checked 状态
        self.indexChanged.connect(new_page_button.on_index_changed)
        self.buttons.append(new_page_button)
        self.sideList.append(side)

        # 新建垂直容器
        container = SiDenseVContainer(self)
        container.setSpacing(8)
        container.setAlignment(Qt.AlignCenter)

        # 重新将button加入布局
        for i in range(len(self.buttons)):
            self.buttons[i].setParent(None)
            container.addWidget(self.buttons[i], side=self.sideList[i])

        # 删除原布局
        self.container.deleteLater()

        # 添加新建布局
        self.container = container
        self.container.show()

        # 重新设置标签宽度以解决向左偏移问题
        self.container.resize(self.size())

        self.setMaximumIndex(self.maximumIndex() + 1)

        return new_page_button

    def removePageButton(self, button):
        self.buttons.remove(button)

        # 新建垂直容器
        container = SiDenseVContainer(self)
        container.setSpacing(8)
        container.setAlignment(Qt.AlignCenter)

        # 重新将button加入布局
        for i in range(len(self.buttons)):
            self.buttons[i].setParent(None)
            container.addWidget(self.buttons[i], side=self.sideList[i])

        # 删除原布局
        self.container.deleteLater()

        # 添加新建布局
        self.container = container
        self.container.show()

        # 重新设置标签宽度以解决向左偏移问题
        self.container.resize(self.size())

        self.setMaximumIndex(self.maximumIndex() - 1)


    def resizeEvent(self, event):
        super().resizeEvent(event)
        size = event.size()

        self.container.resize(size)


class StackedContainerWithShowUpAnimation(SiStackedContainer):
    def setCurrentIndex(self, index: int):
        super().setCurrentIndex(index)

        self.widgets[index].animationGroup().fromToken("move").setFactor(1 / 5)
        self.widgets[index].move(0, 64)
        self.widgets[index].moveTo(0, 0)


class PageView(SiDenseVContainer):
    """
    页面视图，包括左侧的导航栏和右侧的页面
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, *kwargs)

        # 清空自己的样式表防止继承
        self.setStyleSheet("")

        self.setSpacing(0)
        self.setAdjustWidgetsSize(True)

        # 创建导航栏
        self.page_navigator = PageNavigator(self)
        self.page_navigator.setFixedWidth(16+24+16)

        # 创建堆叠容器
        self.stacked_container = StackedContainerWithShowUpAnimation(self)
        self.stacked_container.setObjectName("stacked_container")

        # <- 添加到水平布局
        self.addWidget(self.page_navigator)
        self.addWidget(self.stacked_container)

    def _get_page_toggle_method(self, index):
        return lambda: self.stacked_container.setCurrentIndex(index)

    def addPage(self, page, icon, hint, side="top"):
        """
        添加页面，这会在导航栏添加一个按钮，并在堆叠容器中添加页面
        :param page: 页面控件
        :param icon: 按钮的 svg 数据或路径
        :param hint: 工具提示
        :param side: 按钮添加在哪一侧
        """
        self.stacked_container.addWidget(page)
        button = self.page_navigator.addPageButton(
            icon,
            hint,
            self._get_page_toggle_method(self.stacked_container.widgetsAmount() - 1),
            side
        )

        return button

    def removePage(self,button,page):
        self.stacked_container.removeWidget(page)
        self.page_navigator.removePageButton(button)


    def reloadStyleSheet(self):
        super().reloadStyleSheet()
        self.stacked_container.setStyleSheet(
            """
            #stacked_container {{
                border-top-left-radius:10px; border-bottom-right-radius: 10px;
                background-color: {}; border:1px solid {};
            }}
            """.format(SiGlobal.siui.colors["INTERFACE_BG_B"], SiGlobal.siui.colors["INTERFACE_BG_C"])
        )

    def resizeEvent(self, event):
        super().resizeEvent(event)
        size = event.size()
        w, h = size.width(), size.height()

        self.page_navigator.resize(56, h - 8)
        self.stacked_container.setGeometry(56, 0, w-56, h)
