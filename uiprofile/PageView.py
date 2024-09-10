from siui.templates.application.components.page_view.page_view import PageView


class PageViewModify(PageView):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, *kwargs)

    def addPage(self, page, icon, hint, side="top"):
        """
        添加页面，这会在导航栏添加一个按钮，并在堆叠容器中添加页面
        :param page: 页面控件
        :param icon: 按钮的 svg 数据或路径
        :param hint: 工具提示
        :param side: 按钮添加在哪一侧
        """
        self.stacked_container.addWidget(page)
        button = self.page_navigator.addPageButton(
            icon,
            hint,
            self._get_page_toggle_method(self.stacked_container.widgetsAmount() - 1),
            side
        )
        return button

    def removePage(self, button, page):
        self.stacked_container.removeWidget(page)
        self.page_navigator.removePageButton(button)
