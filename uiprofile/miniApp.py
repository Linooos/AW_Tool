from siui.templates.application.application import SiliconApplication
from uiprofile.layer_main import miniMenuLayer

class miniApp(SiliconApplication):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.layer_main = miniMenuLayer(self)