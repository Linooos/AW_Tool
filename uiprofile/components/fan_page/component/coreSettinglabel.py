from siui.components import SiOptionCardLinear, SiPushButton, SiToggleButton
from siui.core.color import SiColor
from siui.core.globals import SiGlobal
from uiprofile.resourcePath import exe_resource_path
from SDK import setTurbo, getTurbo


class CoreSettinglabel(SiOptionCardLinear):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.core_battery = SiToggleButton(self)
        self.core_battery.resize(80, 32)
        self.core_battery.attachment().load(exe_resource_path("uiprofile/icon/battery-full.svg"))
        self.core_battery.attachment().setFont(SiGlobal.siui.fonts["S_BOLD"])
        self.core_battery.attachment().setText(
            "<font color='{}'>{}</font>".format(SiGlobal.siui.colors["TEXT_C"], "电池"))
        self.core_battery.setHint("电池模式下设置开关睿频")
        self.core_battery.colorGroup().assign(SiColor.BUTTON_OFF, "#c8c8c8")
        self.core_battery.colorGroup().assign(SiColor.BUTTON_ON, "#2abed8")
        self.core_battery.colorGroup().assign(SiColor.BUTTON_HOVER, "#40855198")

        self.batteryTurboFunc = lambda checked: self.Turbo_on_change(checked, 'battery')
        self.core_battery.toggled.connect(self.batteryTurboFunc)

        self.core_adapter = SiToggleButton(self)
        self.core_adapter.resize(80, 32)
        self.core_adapter.attachment().setFont(SiGlobal.siui.fonts["S_BOLD"])
        self.core_adapter.attachment().load(exe_resource_path(("uiprofile/icon/bolt.svg")))
        self.core_adapter.attachment().setText(
            "<font color='{}'>{}</font>".format(SiGlobal.siui.colors["TEXT_C"], "适配器"))
        self.core_adapter.setHint("适配器模式下设置开关睿频")
        self.core_adapter.colorGroup().assign(SiColor.BUTTON_OFF, "#c8c8c8")
        self.core_adapter.colorGroup().assign(SiColor.BUTTON_ON, "#ff7575")
        self.core_adapter.colorGroup().assign(SiColor.BUTTON_HOVER, "#40855198")

        self.adapterTurboFunc = lambda checked: self.Turbo_on_change(checked, 'adapter')
        self.core_adapter.toggled.connect(self.adapterTurboFunc)

        self.setTitle("睿频设置", "开关电池供电时睿频\n开关适配器供电时睿频")
        self.load(exe_resource_path("uiprofile/icon/microchip.svg"))
        self.addWidget(self.core_adapter)
        self.addWidget(self.core_battery)

        #初始化
        if getTurbo('battery') == 0:
            self.core_battery.setChecked(False)
        else:
            self.core_battery.setChecked(True)

        if getTurbo('adapter') == 0:
            self.core_adapter.setChecked(False)
        else:
            self.core_adapter.setChecked(True)

    def Turbo_on_change(self, checked, type):
        if checked:
            setTurbo(type, 2)

        else:
            setTurbo(type, 0)

