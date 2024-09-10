from siui.components.option_card import SiOptionCardLinear
from siui.components.widgets import SiSwitch
import sys

class CardSwitch(SiSwitch):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class SettingLinerCard(SiOptionCardLinear):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.switch = CardSwitch()
        self.widgets_container.addWidget(self.switch)
