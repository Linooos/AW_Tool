
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDesktopWidget
from PyQt5.QtGui import QPainter, QBrush, QColor

import siui
from siui.core.color import SiColor
from siui.core.globals import SiGlobal
from siui.templates.application.application_mini_window import SiliconApplication

# siui.core.globals.SiGlobal.siui.loadIcons(
#     icons.IconDictionary(color=SiGlobal.siui.colors.fromToken(SiColor.SVG_NORMAL)).icons
# )


class AW_menu(SiliconApplication):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        screen_geo = QDesktopWidget().screenGeometry()

        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setMinimumSize(400, 380)
        self.resize(400, 800)
        self.move((screen_geo.width() - self.width()) // 2, (screen_geo.height() - self.height()) // 2)
        self.setStyleSheet("""
            border-radius: 5px;
        """)

        self.layerMain().setTitle("AW TOOLS")
        self.setWindowTitle("AW TOOLS")
        self.setWindowIcon(QIcon("./img/empty_icon.png"))


        # self.layerMain().addPage(ExampleHomepage(self),
        #                          icon=SiGlobal.siui.iconpack.get("ic_fluent_home_filled"),
        #                          hint="主页", side="top")
        # self.layerMain().addPage(ExampleIcons(self),
        #                          icon=SiGlobal.siui.iconpack.get("ic_fluent_diversity_filled"),
        #                          hint="图标包", side="top")
        # self.layerMain().addPage(ExampleWidgets(self),
        #                          icon=SiGlobal.siui.iconpack.get("ic_fluent_box_multiple_filled"),
        #                          hint="控件", side="top")
        # self.layerMain().addPage(ExampleContainer(self),
        #                          icon=SiGlobal.siui.iconpack.get("ic_fluent_align_stretch_vertical_filled"),
        #                          hint="容器", side="top")
        # self.layerMain().addPage(ExampleOptionCards(self),
        #                          icon=SiGlobal.siui.iconpack.get("ic_fluent_list_bar_filled"),
        #                          hint="选项卡", side="top")
        # self.layerMain().addPage(ExampleDialogs(self),
        #                          icon=SiGlobal.siui.iconpack.get("ic_fluent_panel_separate_window_filled"),
        #                          hint="消息与二级界面", side="top")
        # self.layerMain().addPage(ExampleFunctional(self),
        #                          icon=SiGlobal.siui.iconpack.get("ic_fluent_puzzle_piece_filled"),
        #                          hint="功能组件", side="top")
        #
        # self.layerMain().addPage(About(self),
        #                          icon=SiGlobal.siui.iconpack.get("ic_fluent_info_filled"),
        #                          hint="关于", side="bottom")
        #
        # self.layerMain().setPage(0)

        SiGlobal.siui.reloadAllWindowsStyleSheet()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setBrush(QBrush(QColor(255, 255, 255)))
        painter.setPen(Qt.NoPen)
        painter.drawRoundedRect(self.rect(), 20, 20)
