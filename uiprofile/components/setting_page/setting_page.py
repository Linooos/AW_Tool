from uiprofile.resourcePath import exe_resource_path
from siui.components.page import SiPage
from siui.components.titled_widget_group import SiTitledWidgetGroup
from PyQt5.QtCore import Qt
from siui.core.silicon import Si

from uiprofile.components.setting_page.settingLinerCard import SettingLinerCard
from SDK import checkGCfg, globalConfig, saveConfig,switchToAutoStart,switchToLUA
checkGCfg('globalSetting')



class SettingPage(SiPage):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # From here, we can start to build our first page in Silicon Application
        # You can set the name of this page, and add widgets to varify the function to beautify it.

        # Set the title of the page
        # self.setTitle("应用模版")

        # Set X Offset for better outfit.
        self.f = None
        self.setPadding(32)
        self.setScrollMaximumWidth(500)
        self.setScrollAlignment(Qt.AlignLeft)
        self.setTitle("设置")

        # Create a SiTitledWidgetGroup object
        self.titled_widget_group = SiTitledWidgetGroup(self)
        self.titled_widget_group.setSiliconWidgetFlag(Si.EnableAnimationSignals)

        # 开机启动
        self.system_startup_card = SettingLinerCard(self)
        self.system_startup_card.setTitle("开机启动", "用户登录时启动")
        self.system_startup_card.load(exe_resource_path('uiprofile/components/setting_page/computer.svg'))
        self.system_startup_card.switch.toggled.connect(self.switch_on_autostart)

        # 开启最小化
        self.startup_minimize_card = SettingLinerCard(self)
        self.startup_minimize_card.setTitle("启动最小化", "->任务托盘")
        self.startup_minimize_card.load(exe_resource_path('uiprofile/components/setting_page/angle-small-down.svg'))
        self.startup_minimize_card.switch.toggled.connect(self.switch_on_minimize)

        # 关闭管理员批准模式
        self.system_LUA = SettingLinerCard(self)
        self.system_LUA.setTitle("关闭管理员批准模式", "如果管理员模式无法自启动\n可以尝试开启此项")
        self.system_LUA.load(exe_resource_path('uiprofile/components/setting_page/user.svg'))
        self.system_LUA.switch.toggled.connect(self.switch_on_LUA)

        # <- ADD
        self.titled_widget_group.addTitle("全局设置")
        self.addPlaceholder(20)
        self.titled_widget_group.addWidget(self.system_startup_card)
        self.titled_widget_group.addWidget(self.startup_minimize_card)
        self.titled_widget_group.addWidget(self.system_LUA)

        # 开启风扇控制
        self.enable_fan_control_card = SettingLinerCard(self)
        self.enable_fan_control_card.setTitle("ALIENWARE功耗控制", "->激活风扇及功耗模式模块")
        self.enable_fan_control_card.load(exe_resource_path('uiprofile/components/setting_page/AWCC.svg'))

        self.titled_widget_group.addTitle("功能设置")
        self.titled_widget_group.addWidget(self.enable_fan_control_card)

        # add placeholder for better outfit
        self.titled_widget_group.addPlaceholder(64)

        # Set SiTitledWidgetGroup object as the attachment of the page's scroll area
        self.setAttachment(self.titled_widget_group)

        #加载保存设置
        try:
            if globalConfig['globalSetting']['autoStart']:
                self.system_startup_card.switch.setChecked(True)
            else:
                self.system_startup_card.switch.setChecked(False)
        except KeyError:
            globalConfig['globalSetting']['autoStart'] = False
            self.system_startup_card.switch.setChecked(False)

        # 加载保存设置
        try:
            if globalConfig['globalSetting']['minimize']:
                self.startup_minimize_card.switch.setChecked(True)
            else:
                self.startup_minimize_card.switch.setChecked(False)
        except KeyError:
            globalConfig['globalSetting']['minimize'] = False
            self.startup_minimize_card.switch.setChecked(False)

        try:
            if globalConfig['globalSetting']['LUA']:
                self.system_LUA.switch.setChecked(True)
            else:
                self.system_LUA.switch.setChecked(False)
        except KeyError:
            globalConfig['globalSetting']['LUA'] = False
            self.system_LUA.switch.setChecked(False)

    def switch_on_autostart(self, checked):

        if checked:

            switchToAutoStart(checked)
            globalConfig['globalSetting']['autoStart'] = True
        else:
            switchToAutoStart(checked)

            globalConfig['globalSetting']['autoStart'] = False

        saveConfig()
        pass

    def switch_on_minimize(self, checked):
        if checked:
            globalConfig['globalSetting']['minimize'] = True
        else:
            globalConfig['globalSetting']['minimize'] = False
        saveConfig()
        pass

    def switch_on_LUA(self, checked):
        if checked:
            switchToLUA(True)
            globalConfig['globalSetting']['LUA'] = True
        else:
            switchToLUA(False)
            globalConfig['globalSetting']['LUA'] = False
        saveConfig()
        pass