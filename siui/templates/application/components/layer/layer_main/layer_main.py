import os

from PyQt5.QtCore import Qt
import sys
from siui.components import SiLabel, SiDenseVContainer, SiDenseHContainer, SiPixLabel,SiSimpleButton,DragSiLabel,SiSvgLabel
from siui.core.color import SiColor
from siui.core.globals import SiGlobal
from siui.core.silicon import Si
from siui.templates.application.components.page_view import PageView
from ..layer import SiLayer



class LayerMain(SiLayer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # 整个窗口的垫底标签
        self.background_label = SiLabel(self)
        self.background_label.setFixedStyleSheet("border-radius: 8px")

        # -> 垂直容器，上方是标题，下方是窗口内容
        self.container_title_and_content = SiDenseVContainer(self)
        self.container_title_and_content.setSpacing(0)
        self.container_title_and_content.setAdjustWidgetsSize(True)

        # -> 标题栏处的水平容器，左侧是图标和标题，右侧是操作按钮
        self.container_title = SiDenseHContainer(self)
        self.container_title.setSpacing(0)
        self.container_title.setAlignment(Qt.AlignCenter)
        self.container_title.setFixedHeight(64)

        # 应用内图标
        self.app_icon = SiPixLabel(self)
        self.app_icon.resize(24, 24)
        self.app_icon.load("./img/logo_new.png")

        # 应用标题
        self.app_title = SiLabel(self)
        self.app_title.setAlignment(Qt.AlignVCenter | Qt.AlignLeft)
        self.app_title.setFont(SiGlobal.siui.fonts["S_NORMAL"])
        self.app_title.setSiliconWidgetFlag(Si.AdjustSizeOnTextChanged)
        self.app_title.setText("Silicon 应用模版")

        self.container_title.addPlaceholder(2)
        self.container_title.addPlaceholder(16)
        self.container_title.addWidget(self.app_icon)
        self.container_title.addPlaceholder(16)
        self.container_title.addWidget(self.app_title)

        self.page_view = PageView(self)

        # <- 添加到垂直容器
        self.container_title_and_content.addWidget(self.container_title)
        self.container_title_and_content.addWidget(self.page_view)

        # 隐藏阴影层，因为没有任何用
        self.dim_.hide()

    def reloadStyleSheet(self):
        self.background_label.setStyleSheet("background-color: {}; border: 1px solid {};".format(
            self.colorGroup().fromToken(SiColor.INTERFACE_BG_A),
            self.colorGroup().fromToken(SiColor.INTERFACE_BG_B))
        )
        self.app_title.setStyleSheet("color: {}".format(self.colorGroup().fromToken(SiColor.TEXT_B)))

    def setTitle(self, title):
        self.app_title.setText(title)

    def addPage(self, page, icon, hint: str, side="top"):
        """
        添加新页面
        :param page: 页面控件
        :param icon: 页面按钮的 svg 数据或路径
        :param hint: 页面按钮的工具提示
        :param side: 页面按钮置于哪一侧
        """
        self.page_view.addPage(page, icon, hint, side)

    def setPage(self, index):
        """ Set current page by index """
        self.page_view.stacked_container.setCurrentIndex(index)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.background_label.resize(event.size())
        self.container_title_and_content.resize(event.size())
        self.page_view.resize(event.size().width(), event.size().height() - 64)
        self.dim_.resize(event.size())


class miniMenuLayer(SiLayer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # 整个窗口的垫底标签
        self.background_label = SiLabel(self)
        self.background_label.setFixedStyleSheet("border-radius: 8px")

        # 顶栏
        self.app_top_tip = SiDenseHContainer(self)
        self.app_top_tip.setSpacing(0)
        self.app_top_tip.setAlignment(Qt.AlignCenter)
        self.app_top_tip.setFixedHeight(40)

        #关闭按钮
        self.link_button = SiSimpleButton(self)

        self.link_button.setFixedSize(32, 32)
        self.link_button.attachment().load("./uiprofile/icon/cross.svg")
        self.link_button.setHint("quit")
        self.link_button.clicked.connect(lambda :quit())
        link_button_container = SiDenseVContainer(self)
        link_button_container.setAlignment(Qt.AlignCenter)

        link_button_container.setFixedSize(50,32)
        link_button_container.addWidget(self.link_button)


        # -> 垂直容器，上方是标题，下方是窗口内容
        self.container_title_and_content = SiDenseVContainer(self)
        self.container_title_and_content.setSpacing(0)
        self.container_title_and_content.setAdjustWidgetsSize(True)
        self.container_title_and_content.setContentsMargins(0,0,0,0)

        # -> 标题栏处的水平容器，左侧是图标和标题，右侧是操作按钮
        self.container_title = SiDenseHContainer(self)
        self.container_title.setSpacing(0)
        self.container_title.setAlignment(Qt.AlignCenter)
        self.container_title.setFixedHeight(64)

        # 应用内图标
        self.app_icon = SiSvgLabel(self)
        self.app_icon.resize(40, 40)
        self.app_icon.setSvgSize(40,40)
        self.app_icon.load("./uiprofile/icon/AWCC.svg")

        # 应用标题
        self.app_title = SiLabel(self)
        self.app_title.setAlignment(Qt.AlignVCenter | Qt.AlignLeft)
        self.app_title.setFont(SiGlobal.siui.fonts["S_NORMAL"])
        self.app_title.setSiliconWidgetFlag(Si.AdjustSizeOnTextChanged)
        self.app_title.setText("Silicon 应用模版")

        self.container_title.addPlaceholder(2)
        self.container_title.addPlaceholder(16)
        self.container_title.addWidget(self.app_icon)
        self.container_title.addPlaceholder(16)
        self.container_title.addWidget(self.app_title)


        self.page_view = PageView(self)
        self.page_view.setContentsMargins(0,0,0,0)

        self.drag_label = DragSiLabel(self)
        self.drag_label.setFixedSize(self.window().width(), 40)
        self.background_label.setFixedStyleSheet("")
        self.background_label.setFixedStyleSheet("border-radius: 5px")
        self.drag_label.setAlignment(Qt.AlignCenter)
        self.drag_label.setColor(self.colorGroup().fromToken(SiColor.INTERFACE_BG_F))


        # <- 添加到垂直容器
        self.app_top_tip.addWidget(self.drag_label,side='left')
        self.app_top_tip.addWidget(link_button_container,side='right')
        self.container_title_and_content.addWidget(self.app_top_tip)
        self.container_title_and_content.addWidget(self.container_title)
        self.container_title_and_content.addWidget(self.page_view)


        # 隐藏阴影层，因为没有任何用
        self.dim_.hide()

    def reloadStyleSheet(self):
        self.background_label.setStyleSheet("background-color: {};".format(
            self.colorGroup().fromToken(SiColor.INTERFACE_BG_A),
            self.colorGroup().fromToken(SiColor.INTERFACE_BG_B))
        )
        self.app_title.setStyleSheet("color: {}".format(self.colorGroup().fromToken(SiColor.TEXT_B)))

    def setTitle(self, title):
        self.app_title.setText(title)

    def addPage(self, page, icon, hint: str, side="top"):
        """
        添加新页面
        :param page: 页面控件
        :param icon: 页面按钮的 svg 数据或路径
        :param hint: 页面按钮的工具提示
        :param side: 页面按钮置于哪一侧
        """
        self.page_view.addPage(page, icon, hint, side)

    def setPage(self, index):
        """ Set current page by index """
        self.page_view.stacked_container.setCurrentIndex(index)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.background_label.resize(event.size())
        self.container_title_and_content.resize(event.size())
        self.page_view.resize(event.size().width(), event.size().height() - 64)
        self.dim_.resize(event.size())
