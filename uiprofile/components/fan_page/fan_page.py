from PyQt5.QtCore import Qt, QTimer
from SiliconUI import SiSlider

import server
from siui.components import SiSliderH
from siui.components.combobox.combobox import SiComboBox
from siui.components.option_card import SiOptionCardPlane
from siui.components.page import SiPage

from siui.components.titled_widget_group import SiTitledWidgetGroup
from siui.components.widgets import SiLabel
from siui.core.globals import SiGlobal
from siui.core.silicon import Si

from siui.components.widgets.container import SiDividedHContainer, SiDenseVContainer
from server import fanCount, getRPM, setFansBoost


class FanSlider(SiSliderH):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fanid = None
        self.auto_update = True
        self.valueChanged.connect(self.on_slider_value_changed)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.auto_update = False
        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.auto_update = True
        super().mouseReleaseEvent(event)

    def on_slider_value_changed(self):
        #if not self.auto_update:
            pass
            #setFanBoost(self.fanid, self.value())



class FanCardContainer(SiOptionCardPlane):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fanRPMlist = []
        self.fanSliderlist = []
        self.additional_description = SiLabel(self)
        #self.setTitle("风扇设置")
        self.additional_description.setSiliconWidgetFlag(Si.AdjustSizeOnTextChanged)
        self.additional_description.setAlignment(Qt.AlignLeft | Qt.AlignBottom)

        # 电源选择按钮
        self.power_choice = SiComboBox(self)
        self.power_choice.setFixedWidth(10)
        self.power_choice.setFixedWidth(150)
        # 电源选择标签
        self.power_label = SiLabel(self)
        self.power_label.setSiliconWidgetFlag(Si.AdjustSizeOnTextChanged)
        self.power_label.setFont(SiGlobal.siui.fonts["S_BOLD"])
        self.power_label.setAlignment(Qt.AlignBottom | Qt.AlignRight)
        self.power_label.setFixedHeight(20)
        self.power_label.setText("<font color='{}'>{}</font>".format(SiGlobal.siui.colors["TEXT_C"], "电源模式"))

        self.power_container = SiDenseVContainer(self)
        self.power_container.setAlignment(Qt.AlignRight)
        self.power_container.setAdjustWidgetsSize(True)
        self.power_container.addPlaceholder(8)
        self.power_container.addWidget(self.power_label)
        self.power_container.setSpacing(8)
        #self.power_container.addPlaceholder(5)
        self.power_container.addWidget(self.power_choice)

        self.header().addWidget(self.power_container, side='right')
        self.header().adjustSize()

        # 添加风扇
        for i in range(fanCount):
            #转速显示
            fanRPM = SiLabel(self)
            self.fanRPMlist.append(fanRPM)
            fanRPM.setSiliconWidgetFlag(Si.AdjustSizeOnTextChanged)
            fanRPM.setFont(SiGlobal.siui.fonts["M_BOLD"])
            fanRPM.setAlignment(Qt.AlignBottom | Qt.AlignLeft)
            fanRPM.setFixedHeight(24)
            fanRPM.setText("<font color='{}'>{}</font>".format(SiGlobal.siui.colors["TEXT_C"], "5650RPM"))

            #滑条设置
            fanSlider = FanSlider(self)
            self.fanSliderlist.append(fanSlider)
            fanSlider.setFixedHeight(20)
            fanSlider.setFixedWidth(400)
            fanSlider.setMinimum(0)
            fanSlider.setMaximum(100)
            fanSlider.fanid = i

            fanContainer = SiDenseVContainer(self)
            fanContainer.setSpacing(15)
            fanContainer.addWidget(fanRPM)
            fanContainer.addWidget(fanSlider)
            fanContainer.adjustSize()
            self.body().addWidget(fanContainer)
            self.body().setFixedHeight(self.body().height() + 60)

        #设置检测计时器
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_slider_value)
        self.timer.start(500)  # 每隔2秒执行一次

        self.auto_update = True

    def update_slider_value(self):
        for i in range(fanCount):
            if self.fanSliderlist[i].auto_update:
                rpm = getRPM(i)
                self.fanRPMlist[i].setText(
                    "<font color='{}'>{}</font>".format(SiGlobal.siui.colors["TEXT_C"], str(rpm) + "RPM"))
                setFansBoost(i,self.fanSliderlist[i].value())



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
            group.addPlaceholder(12)
            self.side_messages = FanCardContainer(self)
            group.addTitle("风扇控制")

            #

            # 自动消失
            # self.ctrl_auto_close = SiComboBox(self)
            # self.ctrl_auto_close.resize(80, 32)
            # self.ctrl_auto_close.addOption("禁用", value=False)
            # self.ctrl_auto_close.addOption("启用", value=True)
            # self.ctrl_auto_close.menu().setShowIcon(False)
            # self.ctrl_auto_close.menu().setIndex(0)
            # self.ctrl_auto_close.valueChanged.connect(self.set_message_box_auto_close)
            #
            # self.option_card_auto_close = SiOptionCardLinear(self)
            # self.option_card_auto_close.load(SiGlobal.siui.iconpack.get("ic_fluent_panel_right_contract_regular"))
            # self.option_card_auto_close.setTitle("自动隐藏", "以降低操作复杂性，或是保留重要信息")
            # self.option_card_auto_close.addWidget(self.ctrl_auto_close)

            # -- 停留时长
            # self.ctrl_stay_duration = SiDoubleSpinBox(self)
            # self.ctrl_stay_duration.resize(128, 32)
            # self.ctrl_stay_duration.lineEdit().textChanged.connect(self.set_message_box_auto_close)
            # self.ctrl_stay_duration.setValue(1.0)
            #
            # self.option_card_stay_duration = SiOptionCardLinear(self)
            # self.option_card_stay_duration.load(SiGlobal.siui.iconpack.get("ic_fluent_timer_regular"))
            # self.option_card_stay_duration.setTitle("停留时长", "如果自动隐藏被启用，提示消息将在设定的秒数后隐藏")
            # self.option_card_stay_duration.addWidget(self.ctrl_stay_duration)
            #
            # self.side_messages.body().setAdjustWidgetsSize(True)

            #self.side_messages.body().addWidget(self.option_card_type)
            #self.side_messages.body().addWidget(self.option_card_auto_close)
            #self.side_messages.body().addWidget(self.option_card_stay_duration)
            self.side_messages.body().addPlaceholder(12)
            self.side_messages.adjustSize()

            group.addWidget(self.side_messages)

        with self.titled_widgets_group as group:
            group.addTitle("电源模式")

        # 添加页脚的空白以增加美观性
        self.titled_widgets_group.addPlaceholder(64)

        # 设置控件组为页面对象
        self.setAttachment(self.titled_widgets_group)

        # self.f = None
        # self.setPadding(32)
        # self.setScrollMaximumWidth(500)
        # self.setScrollAlignment(Qt.AlignLeft)
        # #self.setTitle("设置")
        #
        # # Create a SiTitledWidgetGroup object
        # self.titled_widget_group = SiTitledWidgetGroup(self)
        # self.titled_widget_group.setSiliconWidgetFlag(Si.EnableAnimationSignals)

        # # <- ADD
        # self.titled_widget_group.addTitle("全局设置")
        # self.addPlaceholder(20)
        # self.titled_widget_group.addWidget(self.system_startup_card)

        # # 平面选项卡
        # header_button = SiSimpleButton(self)
        # header_button.setFixedHeight(32)
        # header_button.attachment().setText("Header 区域")
        # header_button.attachment().load(SiGlobal.siui.iconpack.get("ic_fluent_window_header_horizontal_regular"))
        # header_button.adjustSize()
        #
        # body_label = SiLabel(self)
        # body_label.setSiliconWidgetFlag(Si.AdjustSizeOnTextChanged)
        # body_label.setStyleSheet("color: {}".format(SiGlobal.siui.colors["TEXT_B"]))
        # body_label.setText("平面选项卡提供了三个容器：header，body，footer，每个容器都可以独立访问\n其中 header 和 footer 是水平容器，body 是垂直容器\n这个容器是平面选项卡的 body，在这里尽情添加控件吧！")
        #
        # footer_button_a = SiSimpleButton(self)
        # footer_button_a.resize(32, 32)
        # footer_button_a.attachment().load(SiGlobal.siui.iconpack.get("ic_fluent_pen_regular"))
        # footer_button_a.setHint("绘制")
        #
        # footer_button_b = SiSimpleButton(self)
        # footer_button_b.resize(32, 32)
        # footer_button_b.attachment().load(SiGlobal.siui.iconpack.get("ic_fluent_eyedropper_regular"))
        # footer_button_b.setHint("取色器")
        #
        # footer_button_c = SiSimpleButton(self)
        # footer_button_c.resize(32, 32)
        # footer_button_c.attachment().load(SiGlobal.siui.iconpack.get("ic_fluent_save_regular"))
        # footer_button_c.setHint("保存")
        #
        # self.option_card_plane_beginning = SiOptionCardPlane(self)
        # self.option_card_plane_beginning.setTitle("平面选项卡")
        # self.option_card_plane_beginning.header().addWidget(header_button, side="right")
        # self.option_card_plane_beginning.body().addWidget(body_label, side="top")
        # self.option_card_plane_beginning.footer().setFixedHeight(64)
        # self.option_card_plane_beginning.footer().setSpacing(8)
        # self.option_card_plane_beginning.footer().setAlignment(Qt.AlignCenter)
        # self.option_card_plane_beginning.footer().addWidget(footer_button_a, side="left")
        # self.option_card_plane_beginning.footer().addWidget(footer_button_b, side="left")
        # self.option_card_plane_beginning.footer().addWidget(footer_button_c, side="left")
        # self.option_card_plane_beginning.adjustSize()
        #
        # # <- ADD
        # self.titled_widget_group.addTitle("平面选项卡")
        # self.titled_widget_group.addWidget(self.option_card_plane_beginning)
        #
        # # 容器
        #
        # container_h = SiDenseHContainer(self)
        # container_h.setSpacing(8)
        # container_h.setFixedHeight(80+8+250)
        #
        # container_v = SiDenseVContainer(self)
        # container_v.setSpacing(8)
        # container_v.setAdjustWidgetsSize(True)
        # self.titled_widget_group.resized.connect(lambda pos: container_v.setFixedWidth(pos[0] - 320 - 8))
        #
        # container_description = SiOptionCardLinear(self)
        # container_description.setTitle("嵌套容器", "让你的界面布局更加美观和直观")
        # container_description.load(SiGlobal.siui.iconpack.get("ic_fluent_slide_layout_regular"))
        #
        # container_plane_left_bottom = SiOptionCardPlane(self)
        # container_plane_left_bottom.setTitle("资源监视器")
        # container_plane_left_bottom.setFixedHeight(250)
        #
        # label_cpu = SiLabel(self)
        # label_cpu.setStyleSheet("color: {}".format(SiGlobal.siui.colors["TEXT_C"]))
        # label_cpu.setText("CPU")
        #
        # progress_bar_cpu = SiProgressBar(self)
        # progress_bar_cpu.setFixedHeight(8)
        # progress_bar_cpu.setValue(0.12)
        #
        # label_ram = SiLabel(self)
        # label_ram.setStyleSheet("color: {}".format(SiGlobal.siui.colors["TEXT_C"]))
        # label_ram.setText("内存")
        #
        # progress_bar_ram = SiProgressBar(self)
        # progress_bar_ram.setFixedHeight(8)
        # progress_bar_ram.setValue(0.61)
        #
        # label_gpu = SiLabel(self)
        # label_gpu.setStyleSheet("color: {}".format(SiGlobal.siui.colors["TEXT_C"]))
        # label_gpu.setText("GPU")
        #
        # progress_bar_gpu = SiProgressBar(self)
        # progress_bar_gpu.setFixedHeight(8)
        # progress_bar_gpu.setValue(0.23)
        #
        # container_plane_left_bottom.body().setAdjustWidgetsSize(True)
        # container_plane_left_bottom.body().addWidget(label_cpu)
        # container_plane_left_bottom.body().addWidget(progress_bar_cpu)
        # container_plane_left_bottom.body().addWidget(label_ram)
        # container_plane_left_bottom.body().addWidget(progress_bar_ram)
        # container_plane_left_bottom.body().addWidget(label_gpu)
        # container_plane_left_bottom.body().addWidget(progress_bar_gpu)
        #
        # container_v.addWidget(container_description)
        # container_v.addWidget(container_plane_left_bottom)
        #
        # container_plane_right = SiOptionCardPlane(self)
        # container_plane_right.setTitle("操作面板")
        # container_plane_right.setFixedHeight(80+8+250)
        # container_plane_right.setFixedWidth(320)
        #
        # label_nothing = SiLabel()
        # label_nothing.setStyleSheet("color: {}".format(SiGlobal.siui.colors["TEXT_D"]))
        # label_nothing.setText("这里好像什么也没有")
        # label_nothing.setAlignment(Qt.AlignCenter)
        # label_nothing.setFixedHeight(220)
        #
        # container_plane_right.body().setAdjustWidgetsSize(True)
        # container_plane_right.body().addWidget(label_nothing)
        #
        # container_h.addWidget(container_v)
        # container_h.addWidget(container_plane_right)
        #
        # # <- ADD
        # self.titled_widget_group.addTitle("容器")
        # self.titled_widget_group.addWidget(container_h)

        # add placeholder for better outfit
        #self.titled_widget_group.addPlaceholder(64)

        # Set SiTitledWidgetGroup object as the attachment of the page's scroll area
        #self.setAttachment(self.titled_widget_group)
