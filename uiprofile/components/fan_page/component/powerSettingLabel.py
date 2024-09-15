from PyQt5.QtCore import pyqtSignal

import SDK
from siui.components import SiOptionCardLinear, SiPushButton, SiToggleButton
from siui.components.combobox import SiComboBox
from siui.core.color import SiColor
from siui.core.globals import SiGlobal
from SDK import globalConfig, checkGCfg, powerCount, powerCfgs, setPower, saveConfig
from uiprofile.resourcePath import exe_resource_path

checkGCfg("globalSetting/powerName")
checkGCfg("fanPage")


class PowerSettinglabel(SiOptionCardLinear):
    switchGmod = pyqtSignal(bool)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


        self.power_list = SiComboBox(self)
        self.power_list.resize(180, 40)
        for i in globalConfig["globalSetting"]["powerName"].values():
            self.power_list.addOption(i)
        self.power_list.menu().setShowIcon(False)
        # self.power_list.menu().setIndex(3)
        self.power_list.menu().indexChanged.connect(self.power_plan_on_change)

        self.setTitle("温控模式选择", "预设模式加载自带温控方案\n自定义模式手动调控风扇")
        self.load(exe_resource_path("uiprofile/icon/dashboard.svg"))
        self.addWidget(self.power_list)

        #加载保存选项
        try:
            saveOption = globalConfig["fanPage"]["powerEnable"]
            for i in range(powerCount):
                if powerCfgs[i] == saveOption:
                    self.power_list.menu().setIndex(i)
                    break
        except KeyError:
            globalConfig["fanPage"]["powerEnable"] = 1
            self.power_list.menu().setIndex(1)
            saveConfig()

    def power_plan_on_change(self, index):
        setPower(index)
        globalConfig["fanPage"]["powerEnable"] = powerCfgs[index]
        saveConfig()

    def OnEditManual(self, enable):
        self.power_list.menu().setIndex(0)

    def onlyUpdateUi(self,index):
        self.power_list.menu().indexChanged.disconnect(self.power_plan_on_change)
        self.power_list.menu().setIndex(index)
        self.power_list.menu().indexChanged.connect(self.power_plan_on_change)