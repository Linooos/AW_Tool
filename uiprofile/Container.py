from siui.components.widgets.container import SiStackedContainer


class SiStackedContainerModify(SiStackedContainer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def removeWidget(self, widget):
        """
        去除传入子控件，但不delete
        :param widget: 子控件
        """
        if widget in self.widgets:
            widget.setParent(None)
            widget.hide()
            self.widgets.remove(widget)
            # if len(self.widgets) == 1:
            #     self.setCurrentIndex(0)
