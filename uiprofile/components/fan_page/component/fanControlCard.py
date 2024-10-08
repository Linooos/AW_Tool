from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtWidgets import QSizePolicy, QAbstractSlider

import SDK
from SDK import fanCount, getRPM, fanCfgs, setFansBoost, setGMode, globalConfig, checkGCfg
from siui.components import SiDenseVContainer, SiLabel, SiSliderH, SiOptionCardPlane, SiDenseHContainer, SiSwitch, \
    SiPushButton, SiSimpleButton
from siui.core.color import SiColor
from siui.core.globals import SiGlobal
from siui.core.silicon import Si
from uiprofile.resourcePath import exe_resource_path

checkGCfg('fanPage')


class FanInfoLayout(SiDenseHContainer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        #标题
        self.setParent(args[0])
        self.fanTitle = SiLabel(self)
        self.fanTitle.setSiliconWidgetFlag(Si.AdjustSizeOnTextChanged)
        self.fanTitle.setFont(SiGlobal.siui.fonts["M_BOLD"])
        self.fanTitle.setStyleSheet("color: {}".format(SiGlobal.siui.colors["TEXT_E"]))
        #self.fanTitle.setStyleSheet("color: #34f434")
        #self.fanTitle.setColor(SiGlobal.siui.colors["TEXT_C"])
        self.fanTitle.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        self.fanTitle.setFixedHeight(30)

        self.fanType = SiLabel(self)
        #self.fanType.setSiliconWidgetFlag(Si.AdjustSizeOnTextChanged)
        self.fanType.setFont(SiGlobal.siui.fonts["S_BOLD"])
        #self.fanType.setColor(SiGlobal.siui.colors["TEXT_C"])
        self.fanType.setAlignment(Qt.AlignRight)
        self.fanType.setFixedWidth(90)
        self.fanType.setFixedHeight(15)

        self.fanContent = SiLabel(self)
        #self.fanContent.setSiliconWidgetFlag(Si.AdjustSizeOnTextChanged)
        self.fanContent.setFont(SiGlobal.siui.fonts["S_BOLD"])
        self.fanContent.setStyleSheet("color: {}".format(SiGlobal.siui.colors["TEXT_E"]))
        self.fanContent.setAlignment(Qt.AlignRight)
        self.fanContent.setFixedWidth(90)
        self.fanContent.setFixedHeight(15)

        info_container = SiDenseVContainer(self)
        info_container.setSpacing(0)
        info_container.setAlignment(Qt.AlignRight)
        info_container.addWidget(self.fanType)
        info_container.addWidget(self.fanContent)
        info_container.setFixedHeight(30)

        self.addWidget(self.fanTitle)
        self.addWidget(info_container, side="right")
        self.setFixedHeight(30)
        #self.setFixedWidth(350)
        self.setAlignment(Qt.AlignTop)
        #self.setColor("#000000")


class FanSlider(SiSliderH):
    sliderList = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fanid = None
        self.auto_update = True
        self.valueChanged.connect(self.on_slider_value_changed)
        self.qtimer = None
        self.sliderList.append(self)
        self.gMod = False

    def setValue(self,
                 value: int,
                 move_to: bool = True):
        """
        设置滑块的值并移动滑块到指定位置
        :param value: 值
        :param move_to: Use moving animation
        """
        #super().setValue(value)
        QAbstractSlider.setValue(self, value)
        self.handle.setHint(f"风扇速度： {str(self.value())} %")
        self._move_handle_according_to_value(move_to=move_to)

    def onlyUpdateUi(self,value):
        self.valueChanged.disconnect(self.on_slider_value_changed)
        self.setValue(value)
        self.valueChanged.connect(self.on_slider_value_changed)
    def initConfig(self):
        if self.fanid is None:
            return
        try:
            self.setValue(SDK.globalConfig["fanPage"][f'{self.fanid}'])
        except KeyError:
            SDK.globalConfig["fanPage"][f'{self.fanid}'] = 0
        self.saveConfig()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.auto_update = False
        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.auto_update = True
        super().mouseReleaseEvent(event)

    def setGMode(self, enable):
        if enable:
            self.gMod = True
            self.setValue(100)
            self.setEnabled(False)
        else:
            self.gMod = False
            self.setValue(SDK.globalConfig["fanPage"][f'{self.fanid}'])
            self.setEnabled(True)

    def resetValue(self):
        self.setValue(0)

    def on_slider_value_changed(self):
        #if not self.auto_update:
        setFansBoost(self.fanid, self.value())
        if self.fanid is not None:
            if not self.gMod:
                SDK.globalConfig["fanPage"][f'{self.fanid}'] = self.value()
                self.saveConfig()

    def saveConfig(self):
        """ 延迟保存文件"""

        #SDK.saveConfig()
        def saveAndDelTimer(self):  #5秒后，运行停止结束计时并保存配置
            self.qtimer.stop()
            self.qtimer.deleteLater()
            self.qtimer = None
            SDK.saveConfig()

        # 当Qtimer=None时，新建一个qtimer开始计时
        if self.qtimer is None:
            self.qtimer = QTimer(self)
            self.qtimer.timeout.connect(lambda: saveAndDelTimer(self))
            self.qtimer.start(5000)


class FanCardContainer(SiOptionCardPlane):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fanRPMlist = []
        self.fanSliderlist = []
        self.additional_description = SiLabel(self)
        #self.setTitle("风扇设置")
        self.additional_description.setSiliconWidgetFlag(Si.AdjustSizeOnTextChanged)
        self.additional_description.setAlignment(Qt.AlignLeft | Qt.AlignBottom)

        # GMod选择按钮
        self.G_mod_switch = SiSwitch(self)
        self.G_mod_switch.setFixedWidth(40)
        self.G_mod_switch.toggled.connect(self.G_mod_toggle)

        # 重置菜单
        self.reset_button = SiSimpleButton(self)
        self.reset_button.attachment().setFont(SiGlobal.siui.fonts["S_BOLD"])

        self.reset_button.attachment().load(exe_resource_path("uiprofile/icon/arrows-repeat.svg"))
        self.reset_button.colorGroup().assign(SiColor.BUTTON_OFF, "#c8c8c8")
        self.reset_button.reloadStyleSheet()
        self.reset_button.resize(48, 48)
        self.reset_button.clicked.connect(self.reset_adjustment)
        reset_button_container = SiDenseVContainer(self)
        reset_button_container.setAlignment(Qt.AlignBottom)
        reset_button_container.addWidget(self.reset_button, side='bottom')

        # GMod选择标签
        self.power_label = SiLabel(self)
        self.power_label.setSiliconWidgetFlag(Si.AdjustSizeOnTextChanged)
        self.power_label.setFont(SiGlobal.siui.fonts["S_BOLD"])
        self.power_label.setAlignment(Qt.AlignBottom | Qt.AlignRight)
        self.power_label.setFixedHeight(15)
        self.power_label.setText("<font color='{}'>{}</font>".format(SiGlobal.siui.colors["TEXT_C"], "GMod"))

        self.power_container = SiDenseVContainer(self)
        self.power_container.setAlignment(Qt.AlignRight)
        #self.power_container.setAdjustWidgetsSize(True)
        self.power_container.addPlaceholder(8)
        self.power_container.addWidget(self.power_label, side="top")
        self.power_container.addWidget(self.G_mod_switch, side='top')
        self.power_container.addPlaceholder(8)

        self.header().addWidget(reset_button_container, side='right')
        self.header().addWidget(self.power_container, side='right')

        self.body().setMinimumWidth(430)

        # 添加风扇
        for i in range(fanCount):
            #转速显示
            fanRPM = FanInfoLayout(self)
            fanRPM.setGeometry(0, 0, self.body().width(), fanRPM.height())
            self.fanRPMlist.append(fanRPM)
            #fanRPM.setSiliconWidgetFlag(Si.AdjustSizeOnTextChanged)

            typeName = None
            if fanCfgs[i].type == 1:
                typeName = 'CPU/RAM'
            elif fanCfgs[i].type == 6:
                typeName = 'GPU'
            fanRPM.fanTitle.setText(typeName)
            fanRPM.fanType.setText("FAN#" + str(i + 1))

            #滑条设置
            fanContainer = SiDenseVContainer(self)
            fanContainer.setSpacing(15)

            fanSlider = FanSlider(self)
            fanSlider.setParent(fanContainer)
            self.fanSliderlist.append(fanSlider)
            #fanSlider.setFixedHeight(20)
            #fanSlider.setFixedWidth(400)
            fanSlider.resize(self.body().width(), 20)
            fanSlider.setMinimum(0)
            fanSlider.setMaximum(100)
            fanSlider.fanid = i
            fanSlider.initConfig()
            fanSlider.on_slider_value_changed()

            fanContainer.addWidget(fanRPM)
            fanContainer.addWidget(fanSlider)
            fanContainer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            self.body().addWidget(fanContainer)
            self.body().setFixedHeight(self.body().height() + 60)

        #载入保存
        try:
            self.power_label.setEnabled(globalConfig['fanPage']['GModEnable'])
        except KeyError:
            globalConfig['fanPage']['GModEnable'] = False

        #设置检测计时器
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_slider_value)
        self.timer.start(500)

        self.auto_update = True

    def getSliderList(self):
        return self.fanSliderlist

    def update_slider_value(self):
        '''自动设置转速文本'''
        for i in range(fanCount):
            if self.fanSliderlist[i].auto_update:
                self.fanRPMlist[i].fanContent.setText(str(getRPM(i)) + "RPM")

    def G_mod_toggle(self, checked):
        '''开关g模式'''
        if checked:
            setGMode(True)
            globalConfig['fanPage']['GModEnable'] = True
            for i in self.getSliderList():
                i.setGMode(True)

        else:
            setGMode(False)
            globalConfig['fanPage']['GModEnable'] = False
            for i in self.getSliderList():
                i.setGMode(False)
        SDK.saveConfig()

    def reset_adjustment(self):
        if self.G_mod_switch.isChecked():
            self.G_mod_switch.setChecked(False)

            #self.G_mod_toggle(False)
        else:
            for i in self.getSliderList():
                i.resetValue()
