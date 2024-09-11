
from components.setting_page.setting_page import SettingPage
from components.page_about import About
from components.page_container import ExampleContainer
from components.page_dialog import ExampleDialogs
from components.page_functional import ExampleFunctional
from components.page_homepage import ExampleHomepage
from components.page_icons import ExampleIcons
from components.page_option_cards import ExampleOptionCards
from components.page_page_control import ExamplePageControl
from components.page_widgets import ExampleWidgets

import TrayTaskWindow as TrayTaskWindow
from siui.core.color import SiColor
from siui.core.globals import SiGlobal
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDesktopWidget
from uiprofile.components.fan_page.fan_page import FanPage

# siui.core.globals.SiGlobal.siui.loadIcons(
#     icons.IconDictionary(color=SiGlobal.siui.colors.fromToken(SiColor.SVG_NORMAL)).icons
# )


class AW_menu(TrayTaskWindow.TrayTaskWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fanButton = None
        self.fanPage = None

        screen_geo = QDesktopWidget().screenGeometry()

        self.setWindowFlag(Qt.FramelessWindowHint)
        #self.setAttribute(Qt.WA_TranslucentBackground)
        self.setMinimumSize(600, 380)
        self.resize(600, 800)
        self.move(self.screen().availableGeometry().width() - self.width(),
                  self.screen().availableGeometry().height() - self.height())

        self.layerMain().setTitle("AW TOOLS")
        self.setWindowTitle("AW TOOLS")
        self.setWindowIcon(QIcon("./uiprofile/icon/AWCC.svg.png"))

        # 添加设置界面
        self.settingPage = SettingPage(self)
        self.layerMain().addPage(self.settingPage,
                                 icon="./uiprofile/components/setting_page/settings-sliders.svg",
                                 hint="设置", side="bottom")
        # 添加关于界面
        self.aboutPage = About(self)
        self.layerMain().addPage(self.aboutPage,
                                 icon=SiGlobal.siui.iconpack.get("ic_fluent_info_filled"),
                                 hint="关于", side="bottom")



        # 链接设置界面按钮回调
        self.settingPage.enable_fan_control_card.switch.toggled.connect(
            lambda checked: self.switchPage(checked, "Fan"))



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
        # self.layerMain().addPage(ExamplePageControl(self),
        #                          icon=SiGlobal.siui.iconpack.get("ic_fluent_wrench_screwdriver_filled"),
        #                          hint="页面控制", side="top")
        # self.layerMain().addPage(ExampleFunctional(self),
        #                          icon=SiGlobal.siui.iconpack.get("ic_fluent_puzzle_piece_filled"),
        #                          hint="功能组件", side="top")
        #
        # self.layerMain().addPage(About(self),
        #                          icon=SiGlobal.siui.iconpack.get("ic_fluent_info_filled"),
        #                          hint="关于", side="bottom")

        self.layerMain().setPage(0)
        SiGlobal.siui.reloadAllWindowsStyleSheet()

    def switchPage(self,checked,str):
        if checked:
            if str == "Fan":
                self.fanPage = FanPage(self)
                self.fanButton = self.layerMain().addPage(self.fanPage,
                                         icon='uiprofile/components/setting_page/AWCC.svg',
                                         hint="主页", side="top")
        else:
            if str == "Fan":
                self.layerMain().removePage(self.fanButton,self.fanPage)
                self.fanPage.deleteLater()
                self.fanButton.deleteLater()

        SiGlobal.siui.reloadAllWindowsStyleSheet()


