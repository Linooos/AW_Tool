from PyQt5.QtCore import Qt

from siui.components.page import SiPage

from siui.components.titled_widget_group import SiTitledWidgetGroup

from SDK import checkGCfg
from .component.fanControlCard import FanCardContainer
from .component.coreSettinglabel import CoreSettinglabel
from .component.powerSettingLabel import PowerSettinglabel

checkGCfg("fanPage")


class FanPage(SiPage):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setPadding(32)
        self.setScrollMaximumWidth(500)
        self.setScrollAlignment(Qt.AlignLeft)

        # 创建控件组
        self.titled_widgets_group = SiTitledWidgetGroup(self)
        #self.titled_widgets_group.setAdjustWidgetsSize(False)# 禁用调整宽度

        # 侧边栏信息
        with self.titled_widgets_group as group:
            group.addPlaceholder(10)
            self.fan_setting_label = FanCardContainer(self)
            group.addTitle("风扇控制")

            self.fan_setting_label.body().addPlaceholder(12)
            self.fan_setting_label.adjustSize()
            group.addWidget(self.fan_setting_label)

            self.core_setting_label = CoreSettinglabel(self)
            group.addWidget(self.core_setting_label)
            self.power_setting_label = PowerSettinglabel(self)
            group.addWidget(self.power_setting_label)

        # 添加页脚的空白以增加美观性
        self.titled_widgets_group.addPlaceholder(64)

        # 设置控件组为页面对象
        self.setAttachment(self.titled_widgets_group)

        # 创建控件逻辑关联
        self.fanLogiFunc=lambda value: self.controlLogi(value,"fan")
        self.powerLogiFunc = lambda index: self.controlLogi(index,"power")
        self.gModLogiFunc = lambda checked: self.controlLogi(checked, "gmod")
        self.resetFunc = lambda checked: self.controlLogi(checked, "reset")
        for i in self.fan_setting_label.fanSliderlist:
            i.valueChanged.connect(self.fanLogiFunc)
        self.power_setting_label.power_list.menu().indexChanged.connect(self.powerLogiFunc)
        self.fan_setting_label.G_mod_switch.toggled.connect(self.gModLogiFunc)
        self.fan_setting_label.reset_button.clicked.connect(self.resetFunc)

    def controlLogi(self, value,which):
        if which == "fan":
            #print(f"fan action")
            self.power_setting_label.power_list.menu().indexChanged.disconnect(self.powerLogiFunc)
            self.power_setting_label.onlyUpdateUi(0)
            self.power_setting_label.power_list.menu().indexChanged.connect(self.powerLogiFunc)
        elif which == "power":
            #print(f"power action {value}")
            if value == 0:
                return
            elif value == 5:
                for i in self.fan_setting_label.fanSliderlist:
                    #print(f"power 4 set 100")
                    i.valueChanged.disconnect(self.fanLogiFunc)
                    i.onlyUpdateUi(100)
                    i.valueChanged.connect(self.fanLogiFunc)
            else:
                for i in self.fan_setting_label.fanSliderlist:
                    #print(f"power - set 0")
                    i.valueChanged.disconnect(self.fanLogiFunc)
                    i.onlyUpdateUi(0)
                    i.valueChanged.connect(self.fanLogiFunc)
        elif which == "gmod":
            if value:
                self.power_setting_label.power_list.menu().indexChanged.disconnect(self.powerLogiFunc)
                self.power_setting_label.onlyUpdateUi(0)
                self.power_setting_label.power_list.menu().indexChanged.connect(self.powerLogiFunc)
            #print(f"gmod action {value}")
        elif which == "reset":
            self.power_setting_label.power_list.menu().setIndex(0)
            #print(f"reset action {value}")
