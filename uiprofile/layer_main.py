from siui.templates.application.components.layer.layer import SiLayer

from siui.components import SiLabel, SiDenseVContainer, SiDenseHContainer, SiPixLabel, SiSimpleButton, SiSvgLabel
from PyQt5.QtCore import Qt, pyqtSignal
from siui.core.color import SiColor
from siui.core.globals import SiGlobal
from siui.core.silicon import Si
from uiprofile.PageView import PageViewModify
from uiprofile.resourcePath import exe_resource_path

class SiDragWindowLabel(SiLabel):
    """
    为拖动事件提供支持的标签
    """
    dragged = pyqtSignal(object)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.setMouseTracking(True)
        # self.anchor = QPoint(0, 0)

        self.drag_start_position = None
        self.dragging = None
        self.track = True  # 是否跟随鼠标

    def setTrack(self, b: bool):
        """
        设置是否每次鼠标移动时调用 moveTo 移动到鼠标位置
        :param b: 是否跟踪
        :return:
        """
        self.track = b

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragging = True
            self.drag_start_position = event.globalPos() - self.window().frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if self.dragging:
            self.window().move(event.globalPos() - self.drag_start_position)
            event.accept()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragging = False
            event.accept()

class miniMenuLayer(SiLayer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # 整个窗口的垫底标签
        self.background_label = SiLabel(self)
        self.background_label.setFixedStyleSheet("border-radius: 8px")

        # 顶栏
        # self.app_top_tip = SiDenseHContainer(self)
        # self.app_top_tip.setSpacing(0)
        # self.app_top_tip.setAlignment(Qt.AlignCenter)
        # self.app_top_tip.setFixedHeight(20)

        # -> 垂直容器，上方是标题，下方是窗口内容
        self.container_title_and_content = SiDenseVContainer(self)
        self.container_title_and_content.setSpacing(0)
        self.container_title_and_content.setAdjustWidgetsSize(True)
        self.container_title_and_content.setContentsMargins(0, 0, 0, 0)
        #
        # # -> 标题栏处的水平容器，左侧是图标和标题，右侧是操作按钮
        # self.container_title = SiDenseHContainer(self)
        # self.container_title.setSpacing(0)
        # self.container_title.setAlignment(Qt.AlignCenter)
        # self.container_title.setFixedHeight(60)
        #
        # # 应用内图标
        # self.app_icon = SiSvgLabel(self)
        # self.app_icon.resize(40, 40)
        # self.app_icon.setSvgSize(28, 28)
        # self.app_icon.load(exe_resource_path("./uiprofile/icon/AWCC.svg"))
        # app_icon_container = SiDenseVContainer(self)
        # app_icon_container.setAlignment(Qt.AlignCenter)
        # app_icon_container.setFixedSize(50, 50)
        # app_icon_container.addWidget(self.app_icon, side='bottom')
        #
        # # 应用标题
        # self.app_title = SiLabel(self)
        # self.app_title.setAlignment(Qt.AlignVCenter | Qt.AlignLeft)
        # self.app_title.setFont(SiGlobal.siui.fonts["M_BOLD"])
        # self.app_title.setSiliconWidgetFlag(Si.AdjustSizeOnTextChanged)
        # self.app_title.setText("Silicon 应用模版")
        # app_title_container = SiDenseVContainer(self)
        # app_title_container.setAlignment(Qt.AlignCenter)
        # app_title_container.setFixedSize(110, 40)
        # app_title_container.addWidget(self.app_title, side='bottom')
        #
        # self.container_title.addPlaceholder(2)
        # self.container_title.addPlaceholder(5)
        # self.container_title.addWidget(app_icon_container)
        # self.container_title.addPlaceholder(10)
        # self.container_title.addWidget(app_title_container)
        # self.container_title.setFixedHeight(120)

        self.page_view = PageViewModify(self)

        self.drag_label = SiDragWindowLabel(self)
        self.drag_label.setFixedStyleSheet("border-radius: 5px")
        self.drag_label.setFixedHeight(10)
        self.drag_label.setAlignment(Qt.AlignCenter)
        self.drag_label.setColor(self.colorGroup().fromToken(SiColor.INTERFACE_BG_A))

        # <- 添加到垂直容器
        #self.app_top_tip.addWidget(self.container_title, side='left', index=0)
        #self.app_top_tip.addWidget(self.drag_label, side='left')
        #self.app_top_tip.addWidget(hide_button_container, side='right')
        #self.container_title_and_content.addWidget(self.app_top_tip,side="top")
        self.container_title_and_content.addWidget(self.page_view, side="top")

        #关闭按钮
        self.hide_button = SiSimpleButton(self)
        self.hide_button.colorGroup().assign(SiColor.BUTTON_OFF, "#c8c8c8")
        self.hide_button.setFixedSize(40, 40)
        self.hide_button.attachment().load(exe_resource_path("./uiprofile/icon/minus-small.svg"))
        self.hide_button.setHint("quit")
        self.hide_button.clicked.connect(lambda: self.window().hide())
        self.hide_button_container = SiDenseVContainer(self)
        self.hide_button_container.setAlignment(Qt.AlignCenter)
        self.hide_button_container.setFixedSize(50, 40)
        self.hide_button_container.addWidget(self.hide_button, side='bottom')


        # 隐藏阴影层，因为没有任何用
        self.dim_.hide()

    def reloadStyleSheet(self):
        self.background_label.setStyleSheet("background-color: {};border-radius:10px".format(
            self.colorGroup().fromToken(SiColor.INTERFACE_BG_A),
            self.colorGroup().fromToken(SiColor.INTERFACE_BG_B))
        )
        self.app_title.setStyleSheet("color: {}".format(self.colorGroup().fromToken(SiColor.TEXT_B)))

    # def setTitle(self, title):
    #     self.app_title.setText(title)

    def addPage(self, page, icon, hint: str, side="top"):
        """
        添加新页面
        :param page: 页面控件
        :param icon: 页面按钮的 svg 数据或路径
        :param hint: 页面按钮的工具提示
        :param side: 页面按钮置于哪一侧
        """
        return self.page_view.addPage(page, icon, hint, side)

    def removePage(self, button, page):
        self.page_view.removePage(button, page)

    def setPage(self, index):
        """ Set current page by index """
        self.page_view.stacked_container.setCurrentIndex(index)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.background_label.resize(event.size())
        self.container_title_and_content.resize(event.size())
        self.page_view.resize(event.size().width(), event.size().height())
        self.dim_.resize(event.size())
        self.hide_button_container.setGeometry(event.size().width()-53,8,self.hide_button_container.size().width(),self.hide_button_container.size().height())
        self.drag_label.setGeometry(90,8,event.size().width()-150,self.drag_label.size().height())
