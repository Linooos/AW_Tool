from siui.components import SiOptionCardLinear, SiPushButton, SiToggleButton
from siui.components.combobox import SiComboBox
from siui.core.color import SiColor
from siui.core.globals import SiGlobal
from SDK import globalConfig,checkGCfg
checkGCfg("globalSetting/powerName")


class PowerSettinglabel(SiOptionCardLinear):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.power_list = SiComboBox(self)
        self.power_list.resize(180, 40)
        for i in globalConfig["globalSetting"]["powerName"].values():
            self.power_list.addOption(i)
        self.power_list.menu().setShowIcon(False)
        self.power_list.menu().setIndex(3)

        #self.addWidget(self.power_list)
        #self.addPlaceholder(12)
        #self.adjustSize()
        self.setTitle("电源模式", "ALIENWARE电源模式")
        self.load("uiprofile/icon/dashboard.svg")

        self.addWidget(self.power_list)
