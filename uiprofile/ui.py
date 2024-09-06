
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDesktopWidget
from components.page_about import About
from components.page_dialog import ExampleDialogs
from components.page_homepage import ExampleHomepage
from components.page_icons import ExampleIcons
from components.page_option_cards import ExampleOptionCards
from components.page_widgets import ExampleWidgets
from components.page_container import ExampleContainer
from components.page_functional import ExampleFunctional



import TrayTaskWindow as TrayTaskWindow
from siui.core.color import SiColor
from siui.core.globals import SiGlobal


# siui.core.globals.SiGlobal.siui.loadIcons(
#     icons.IconDictionary(color=SiGlobal.siui.colors.fromToken(SiColor.SVG_NORMAL)).icons
# )


class AW_menu(TrayTaskWindow.TrayTaskWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        screen_geo = QDesktopWidget().screenGeometry()

        self.setWindowFlag(Qt.FramelessWindowHint)

        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setMinimumSize(600, 380)
        self.resize(600, 800)
        self.move(self.screen().availableGeometry().width() - self.width(), self.screen().availableGeometry().height() - self.height())
        #self.move((screen_geo.width() - self.width()) // 2, (screen_geo.height() - self.height()) // 2)


        self.layerMain().setTitle("AW TOOLS")
        self.setWindowTitle("AW TOOLS")
        self.setWindowIcon(QIcon("./uiprofile/icon/AWCC.svg.png"))


        self.layerMain().addPage(ExampleHomepage(self),
                                 icon=SiGlobal.siui.iconpack.get("ic_fluent_home_filled"),
                                 hint="主页", side="bottom")
        # self.layerMain().addPage(ExampleIcons(self),
        #                          icon=SiGlobal.siui.iconpack.get("ic_fluent_diversity_filled"),
        #                          hint="图标包", side="top")
        self.layerMain().addPage(ExampleWidgets(self),
                                 icon=SiGlobal.siui.iconpack.get("ic_fluent_box_multiple_filled"),
                                 hint="控件", side="top")
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


