
from components.setting_page.setting_page import SettingPage
from components.page_about import About



import TrayTaskWindow as TrayTaskWindow

from siui.core.globals import SiGlobal

from PyQt5.QtCore import Qt

from uiprofile.components.fan_page.fan_page import FanPage
from SDK import globalConfig as cfg, saveConfig, checkGCfg, checkAPI
from uiprofile.resourcePath import exe_resource_path


checkGCfg('globalSetting/powerName')


class AW_menu(TrayTaskWindow.TrayTaskWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fanButton = None
        self.fanPage = None

        #screen_geo = QDesktopWidget().screenGeometry()

        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setMinimumSize(600, 380)
        self.resize(600, 800)
        self.move(self.screen().availableGeometry().width() - self.width(),
                  self.screen().availableGeometry().height() - self.height())

        #self.layerMain().setTitle("AW TOOLS")
        self.setWindowTitle("AW TOOLS")
        # self.setWindowIcon(QIcon(exe_resource_path("uiprofile/icon/AWCC.svg")))
        # 添加关于界面
        self.aboutPage = About(self)
        self.layerMain().addPage(self.aboutPage,
                                 icon=exe_resource_path("uiprofile/icon/info.svg"),
                                 hint="关于", side="bottom")

        # 添加设置界面
        self.settingPage = SettingPage(self)
        self.layerMain().addPage(self.settingPage,
                                 icon=exe_resource_path("uiprofile/components/setting_page/settings-sliders.svg"),
                                 hint="设置", side="bottom")

        self.layerMain().setPage(1)

        # 配置预开启的页面
        # 风扇页面
        apiList = checkAPI()
        if not (("isAlienware" in apiList) or ("isSupported" in apiList) or ("isGmode" in apiList)):
            # 如果判断可以开启页面
            # 设置加载页面函数与设置页面按钮的链接
            self.settingPage.enable_fan_control_card.switch.toggled.connect(
                lambda checked: self.switchPage(checked, "Fan"))

            # 读取保存配置，是否预开启页面
            try:
                if cfg["globalSetting"]["fanPageEnable"]:
                    self.settingPage.enable_fan_control_card.switch.setChecked(True)
            except KeyError:
                cfg["globalSetting"]["fanPageEnable"] = False
        else:
            # 如果判断不能开启页面
            self.settingPage.enable_fan_control_card.disable_when_not_supported("需要管理员模式\nOR\n不支持的机器")

        self.layerMain().setPage(0)
        SiGlobal.siui.reloadAllWindowsStyleSheet()


    def switchPage(self, checked, str):
        if checked:
            if str == "Fan":
                self.fanPage = FanPage(self)
                self.fanButton = self.layerMain().addPage(self.fanPage,
                                                          icon=exe_resource_path('uiprofile/components/setting_page'
                                                                                 '/AWCC.svg'),
                                                          hint="AW风扇控制", side="top")
                cfg["globalSetting"]["fanPageEnable"] = True
        else:
            if str == "Fan":
                self.layerMain().removePage(self.fanButton, self.fanPage)
                self.fanPage.deleteLater()
                self.fanButton.deleteLater()
                cfg["globalSetting"]["fanPageEnable"] = False
        saveConfig()
        SiGlobal.siui.reloadAllWindowsStyleSheet()
