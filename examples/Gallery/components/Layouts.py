
from SiliconUI import *
from SiliconUI.SiGlobal import *

from siui.components.widgets import SiPushButton

from .web_url import GithubUrl, browse


class WidgetSticker(SiliconUI.SiSticker):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

        self.button_github = SiButtonFlat(self)
        self.button_github.resize(32, 32)
        self.button_github.load(SiGlobal.icons.get("fi-rr-link"))
        self.button_github.setHint("查看源代码")

        self.button_report_bug = SiButtonFlat(self)
        self.button_report_bug.resize(32, 32)
        self.button_report_bug.load(SiGlobal.icons.get("fi-rr-bug"))
        self.button_report_bug.setHint("报告问题")
        self.button_report_bug.clicked.connect(lambda: browse(GithubUrl.Issues_New))

        self.head.addItem(self.button_github, side="right")
        self.head.addItem(self.button_report_bug, side="right")


class LayoutsExample(SiliconUI.SiScrollFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

        self.setStyleSheet("")
        self.max_width_policy = False  # 取消过长中置

        widgets_width = 580

        ## ================ Stack 开始 ===================

        self.stack_layouts_basics = SiliconUI.SiCategory(self)
        self.stack_layouts_basics.setTitle("基本布局")

        self.sticker_flow_layouts = WidgetSticker(self.stack_layouts_basics)
        self.sticker_flow_layouts.setTitle("流式布局")

        self.flow_layout = SiliconUI.SiFlowLayout(self)
        self.flow_layout.setInterval(8, 8)
        self.flow_layout.setFixedWidth(532)

        for _ in range(12):
            label = ClickableLabel(self)
            label.setStyleSheet(
                f"""
                background-color: {colorset.BG_GRAD_HEX[3]};
                color: {colorset.TEXT_GRAD_HEX[0]};
                padding: 4px;
                border-radius: 4px;
            """
            )
            label.setFixedHeight(32)
            label.animation_move.setFactor(1 / 6)  # byd有点快我给放慢点
            label.setText(str(round(random.random(), int(random.random() * 10))))
            self.flow_layout.addItem(label, ani=False)  # 禁用动画

        self.layout_flow_layouts_buttons = SiLayoutH(self)

        self.button_reverse_label = SiPushButton(self)
        self.button_reverse_label.setText("重排首个元素")
        self.button_reverse_label.resize(128, 32)
        self.button_reverse_label.clicked.connect(lambda: reverse_label(self.flow_layout))

        self.button_shuffle_label = SiPushButton(self)
        self.button_shuffle_label.setText("随机打乱")
        self.button_shuffle_label.resize(128, 32)
        self.button_shuffle_label.clicked.connect(lambda: shuffle_label(self.flow_layout))

        self.layout_flow_layouts_buttons.addItem(self.button_reverse_label)
        self.layout_flow_layouts_buttons.addItem(self.button_shuffle_label)

        self.sticker_flow_layouts.addItem(self.flow_layout)
        self.sticker_flow_layouts.addItem(self.layout_flow_layouts_buttons)

        self.stack_layouts_basics.addItem(self.sticker_flow_layouts)

        ## ================ Stack 开始 ===================

        self.stack_layouts_advanced = SiliconUI.SiCategory(self)
        self.stack_layouts_advanced.setTitle("高级布局")

        self.sticker_stacked_layouts = WidgetSticker(self.stack_layouts_advanced)
        self.sticker_stacked_layouts.setTitle("组布局")

        self.stacked_layout = SiliconUI.SiStackedLayout(self)
        self.stacked_layout.setFixedWidth(500)
        self.stacked_layout.setFixedHeight(160)
        self.stacked_layout.addPage("测试选项卡")
        self.stacked_layout.addPage("鸽鸽")

        self.option_test_1 = SiliconUI.SiOptionSwitch(self)
        self.option_test_1.setText("我是测试1", "这是测试1的内容")
        self.option_test_1.setIcon(SiGlobal.icons.get("fi-rr-band-aid"))

        self.option_test_2 = SiliconUI.SiOptionButton(self)
        self.option_test_2.setText("鸡你太美", "备备，偶哦", "你干嘛")
        self.option_test_2.setIcon(SiGlobal.icons.get("fi-rr-basketball"))

        self.stacked_layout.addItemToPage("测试选项卡", self.option_test_1)
        self.stacked_layout.addItemToPage("鸽鸽", self.option_test_2)
        # self.stacked_layout.setStyleSheet('background-color: #20ff0000')

        self.sticker_stacked_layouts.addItem(self.stacked_layout)

        self.stack_layouts_advanced.addItem(self.sticker_stacked_layouts)

        self.addItem(self.stack_layouts_basics)
        self.addItem(self.stack_layouts_advanced)


def shuffle_label(obj):
    random.shuffle(obj.items)
    obj.adjustSize()
    obj.parent.adjustSize()


def reverse_label(obj):
    obj.items = obj.items[1:] + [obj.items[0]]
    obj.adjustSize()
    obj.parent.adjustSize()
