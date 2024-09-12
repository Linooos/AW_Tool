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
            group.addPlaceholder(1)
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


