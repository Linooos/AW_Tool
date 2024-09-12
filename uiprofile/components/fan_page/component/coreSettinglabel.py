from siui.components import SiOptionCardLinear, SiPushButton, SiToggleButton
from siui.core.color import SiColor
from siui.core.globals import SiGlobal


class CoreSettinglabel(SiOptionCardLinear):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.core_adapter = SiToggleButton(self)
        self.core_adapter.resize(80, 32)
        self.core_adapter.attachment().load("uiprofile/icon/battery-full.svg")
        self.core_adapter.attachment().setFont(SiGlobal.siui.fonts["S_BOLD"])
        self.core_adapter.attachment().setText(
            "<font color='{}'>{}</font>".format(SiGlobal.siui.colors["TEXT_C"], "电池"))
        self.core_adapter.setHint("电池模式下设置开关睿频")
        self.core_adapter.colorGroup().assign(SiColor.BUTTON_OFF, "#c8c8c8")
        self.core_adapter.colorGroup().assign(SiColor.BUTTON_ON, "#2abed8")
        self.core_adapter.colorGroup().assign(SiColor.BUTTON_HOVER, "#40855198")

        self.core_battery = SiToggleButton(self)
        self.core_battery.resize(80, 32)
        self.core_battery.attachment().setFont(SiGlobal.siui.fonts["S_BOLD"])
        self.core_battery.attachment().load("uiprofile/icon/bolt.svg")
        self.core_battery.attachment().setText(
            "<font color='{}'>{}</font>".format(SiGlobal.siui.colors["TEXT_C"], "适配器"))
        self.core_battery.setHint("适配器模式下设置开关睿频")
        self.core_battery.colorGroup().assign(SiColor.BUTTON_OFF, "#c8c8c8")
        self.core_battery.colorGroup().assign(SiColor.BUTTON_ON, "#ff7575")
        self.core_battery.colorGroup().assign(SiColor.BUTTON_HOVER, "#40855198")

        self.setTitle("睿频设置", "供电模式睿频")
        self.load("uiprofile/icon/microchip.svg")
        self.addWidget(self.core_adapter)
        self.addWidget(self.core_battery)

