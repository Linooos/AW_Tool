from siui.templates.application.components.page_view.page_view import PageView, PageNavigator, PageButton

from uiprofile.Container import SiStackedContainerModify
from siui.components.widgets.container import SiDenseHContainer


class PageNavigatorModify(PageNavigator):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def addPageButton(self, svg_data, hint, func_when_active, side="top"):
        """
        添加页面按钮
        :param svg_data: 按钮的 svg 数据
        :param hint: 工具提示
        :param func_when_active: 当被激活时调用的函数
        :param side: 添加在哪一侧
        """
        new_page_button = PageButton(self.container)
        new_page_button.setIndex(self.maximumIndex())
        new_page_button.setStyleSheet("background-color: #20FF0000")
        new_page_button.resize(40, 40)
        new_page_button.setHint(hint)
        new_page_button.attachment().setSvgSize(20, 20)
        new_page_button.attachment().load(svg_data)
        new_page_button.activated.connect(func_when_active)
        new_page_button.show()
        new_page_button.reloadStyleSheet()

        # 绑定索引切换信号，当页面切换时，会使按钮切换为 checked 状态
        self.indexChanged.connect(new_page_button.on_index_changed)

        # 新按钮添加到容器中
        self.container.addWidget(new_page_button, side=side)
        self.container.arrangeWidget()
        self.setMaximumIndex(self.maximumIndex() + 1)

        self.buttons.append(new_page_button)
        return new_page_button

    def removePageButton(self, button):
        self.buttons.remove(button)
        self.container.removeWidget(button)

        self.setMaximumIndex(self.maximumIndex() - 1)


class StackedContainerWithShowUpAnimationModify(SiStackedContainerModify):
    def setCurrentIndex(self, index: int):
        super().setCurrentIndex(index)

        self.widgets[index].animationGroup().fromToken("move").setFactor(1 / 5)
        self.widgets[index].move(0, 64)
        self.widgets[index].moveTo(0, 0)


class PageViewModify(PageView):
    def __init__(self, *args, **kwargs):
        SiDenseHContainer.__init__(self, *args, **kwargs)
        # 清空自己的样式表防止继承
        self.setStyleSheet("")

        self.setSpacing(0)
        self.setAdjustWidgetsSize(True)

        # 创建导航栏
        self.page_navigator = PageNavigatorModify(self)
        self.page_navigator.setFixedWidth(16 + 24 + 16)

        # 创建堆叠容器
        self.stacked_container = StackedContainerWithShowUpAnimationModify(self)
        self.stacked_container.setObjectName("stacked_container")

        # <- 添加到水平布局
        self.addWidget(self.page_navigator)
        self.addWidget(self.stacked_container)

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
