from PyQt5.QtCore import Qt

from siui.components.page import SiPage

from siui.components.titled_widget_group import SiTitledWidgetGroup

from SDK import checkGCfg
from .component.fanControlCard import FanCardContainer
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
            self.side_messages = FanCardContainer(self)
            group.addTitle("风扇控制")
            self.side_messages.body().addPlaceholder(12)
            self.side_messages.adjustSize()

            group.addWidget(self.side_messages)

        with self.titled_widgets_group as group:
            group.addTitle("电源模式")

        # 添加页脚的空白以增加美观性
        self.titled_widgets_group.addPlaceholder(64)

        # 设置控件组为页面对象
        self.setAttachment(self.titled_widgets_group)


