from PyQt5.QtCore import Qt

from siui.components import SiLabel
from siui.components.option_card import SiOptionCardLinear
from siui.components.widgets import SiSwitch
import sys

from siui.core.globals import SiGlobal
from siui.core.silicon import Si


class CardSwitch(SiSwitch):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class SettingLinerCard(SiOptionCardLinear):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.switch = CardSwitch()
        self.widgets_container.addWidget(self.switch)

    def disable_when_not_supported(self,text :str):
        self.widgets_container.removeWidget(self.switch)
        self.switch.setEnabled(False)
        self.switch.setHidden(True)
        self.reason_info = SiLabel(self)
        self.reason_info.setSiliconWidgetFlag(Si.AdjustSizeOnTextChanged)
        self.reason_info.setFixedStyleSheet("padding-top: 20px; padding-bottom: 20px;")
        self.reason_info.setFont(SiGlobal.siui.fonts["S_BOLD"])
        self.reason_info.setAlignment(Qt.AlignRight)
        self.reason_info.setText("<font color='{}'>{}</font>".format("#b9b9b9", text.replace('\n','<br>')))
        self.widgets_container.addWidget(self.reason_info,side='right')
        self.adjustSize()