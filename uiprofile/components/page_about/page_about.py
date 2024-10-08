from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtGui import QDesktopServices
from PyQt5.QtWidgets import QSizePolicy

from siui.components import SiTitledWidgetGroup, SiOptionCardLinear, SiPushButton, SiSimpleButton, SiPixLabel, \
    SiDenseVContainer, SiLabel
from siui.components.page import SiPage
from siui.core.color import SiColor
from siui.core.effect import SiQuickEffect
from siui.core.globals import SiGlobal
from siui.core.silicon import Si
from siui.gui import GlobalFont
from uiprofile.resourcePath import exe_resource_path


class About(SiPage):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setPadding(64)
        self.setScrollMaximumWidth(950)
        self.setTitle("关于")

        self.titled_widget_group = SiTitledWidgetGroup(self)
        self.titled_widget_group.setSiliconWidgetFlag(Si.EnableAnimationSignals)

        version_picture_container = SiDenseVContainer(self)
        version_picture_container.setAlignment(Qt.AlignCenter)
        version_picture_container.setFixedHeight(128 + 48+40)
        SiQuickEffect.applyDropShadowOn(version_picture_container, color=(28, 25, 31, 255), blur_radius=48)

        self.version_picture = SiPixLabel(self)
        self.version_picture.setFixedSize(128, 128)
        self.version_picture.setBorderRadius(0)
        self.version_picture.load(exe_resource_path("uiprofile/icon/AWCC.svg"))

        self.version_label = SiLabel(self)
        self.version_label.setSiliconWidgetFlag(Si.AdjustSizeOnTextChanged)
        self.version_label.setFont(GlobalFont.M_NORMAL.value)
        self.version_label.setStyleSheet(f"color: {self.colorGroup().fromToken(SiColor.TEXT_D)}")
        self.version_label.setText("AW-TOOL")

        version_picture_container.addPlaceholder(10)
        version_picture_container.addWidget(self.version_picture)
        version_picture_container.addWidget(self.version_label)
        self.titled_widget_group.addWidget(version_picture_container)

        with self.titled_widget_group as group:
            group.addTitle("开源")

            self.button_to_repo = SiSimpleButton(self)
            self.button_to_repo.resize(32, 32)
            self.button_to_repo.attachment().load(SiGlobal.siui.iconpack.get("ic_fluent_open_regular"))
            #self.button_to_repo.clicked.connect(lambda: QDesktopServices.openUrl(QUrl("https://github.com/ChinaIceF/PyQt-SiliconUI")))

            self.option_card_repo = SiOptionCardLinear(self)
            self.option_card_repo.setTitle("开源仓库", "在 GitHub 上查看 AWTool 的项目主页")
            self.option_card_repo.load(exe_resource_path("uiprofile/components/page_about/home.svg"))
            self.option_card_repo.addWidget(self.button_to_repo)

            self.option_card_license = SiOptionCardLinear(self)
            self.option_card_license.setTitle("开源许可证", "本项目遵循 GPLv3.0 许可证供非商业使用")
            self.option_card_license.load(exe_resource_path("uiprofile/components/page_about/id-badge.svg"))

            group.addWidget(self.option_card_repo)
            group.addWidget(self.option_card_license)

        with self.titled_widget_group as group:
            group.addTitle("版权")

            self.option_card_copyright = SiOptionCardLinear(self)
            self.option_card_copyright.setTitle("UI引用声明-->PyQt-SiliconUI", "版权所有 © 2024 by ChinaIceF")
            self.option_card_copyright.load(exe_resource_path("uiprofile/components/page_about/info.svg"))

            self.button_to_repo2 = SiSimpleButton(self)
            self.button_to_repo2.resize(32, 32)
            self.button_to_repo2.attachment().load(SiGlobal.siui.iconpack.get("ic_fluent_open_regular"))
            self.button_to_repo2.clicked.connect(lambda: QDesktopServices.openUrl(QUrl("https://github.com/ChinaIceF/PyQt-SiliconUI")))

            group.addWidget(self.option_card_copyright)
            self.option_card_copyright.addWidget(self.button_to_repo2)

            self.option_card_copyright2 = SiOptionCardLinear(self)
            self.option_card_copyright2.setTitle("部分算法声明-->AlienfxTools", "版权所有 © 2020-2023 by T-Troll")
            self.option_card_copyright2.load(exe_resource_path("uiprofile/components/page_about/info.svg"))
            group.addWidget(self.option_card_copyright2)

            self.option_card_copyright3 = SiOptionCardLinear(self)
            self.option_card_copyright3.setTitle("设计声明-->AW TooL", "DESIGNED BY 不锈钢电热水壶")
            self.option_card_copyright3.load(exe_resource_path("uiprofile/components/page_about/info.svg"))
            group.addWidget(self.option_card_copyright3)

        with self.titled_widget_group as group:
            group.addTitle("第三方资源")

            self.option_card_icon_pack = SiOptionCardLinear(self)
            self.option_card_icon_pack.setTitle("图标库", "本项目所使用部分ICON由FLATICON享有版权")
            self.option_card_icon_pack.load(exe_resource_path("uiprofile/components/page_about/home.svg"))

            group.addWidget(self.option_card_icon_pack)

        # add placeholder for better outfit
        self.titled_widget_group.addPlaceholder(64)

        # Set SiTitledWidgetGroup object as the attachment of the page's scroll area
        self.setAttachment(self.titled_widget_group)