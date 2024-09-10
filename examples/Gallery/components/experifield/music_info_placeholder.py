from PyQt5.Qt import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.Qt import *
from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel, QLineEdit
import numpy
import time
import os

import SiliconUI
import SiliconUI.SiGlobal as SiGlobal

from SiliconUI.SiFont import *
from SiliconUI.SiGlobal import colorset

class MusicInfoPlaceholder(SiliconUI.SiSticker):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent =  parent
        

        self.bg = SiliconUI.SiPixLabel(self)
        self.bg.setRadius(8)
        self.opacity = QGraphicsOpacityEffect()
        self.opacity.setOpacity(0.3)
        self.bg.setGraphicsEffect(self.opacity)

        # 所有内容 水平布局
        # 图片 信息 操作按钮
        self.layout_all_content = SiliconUI.SiLayoutH(self)
        self.layout_all_content.move(24, 24)
        self.layout_all_content.setInterval(24)

        # 封面
        self.cover = SiliconUI.SiPixLabel(self)
        self.cover.setRadius(24)
        self.cover.resize(80, 80)

        # 中间信息栏
        self.layout_info = SiliconUI.SiLayoutV(self)
        self.layout_info.setInterval(0)

        # 曲名
        self.title = SiliconUI.SiLabel(self)
        self.title.setFont(font_L2)
        self.title.setText('歌曲名')

        # 作者
        self.artist = SiliconUI.SiButtonLabel(self)
        self.artist.setText('艺术家')
        self.artist.setStyleSheet('''
            color: {}'''.format(colorset.TEXT_GRAD_HEX[2]))

        # 专辑
        self.album = SiliconUI.SiButtonLabel(self)
        self.album.setText('专辑')
        self.album.setStyleSheet('''
            color: {}'''.format(colorset.TEXT_GRAD_HEX[2]))

        self.layout_info.addItem(self.title)
        self.layout_info.addVacant(4)
        self.layout_info.addItem(self.artist)
        self.layout_info.addItem(self.album)

        self.layout_all_content.addItem(self.cover)
        self.layout_all_content.addItem(self.layout_info)


        # 右侧操作栏
        self.layout_operation = SiliconUI.SiLayoutV(self)
        self.layout_operation.setInterval(0)

        # 下载
        self.download = SiliconUI.SiButtonFlat(self)
        self.download.resize(32, 32)
        self.download.load(SiGlobal.icons.get('fi-rr-download'))
        self.download.setHint('下载单曲')

        # 收藏
        self.like = SiliconUI.SiButtonFlat(self)
        self.like.resize(32, 32)
        self.like.load(SiGlobal.icons.get('fi-rr-heart'))
        self.like.setHint('收藏')

        # 评论
        self.comments = SiliconUI.SiButtonFlat(self)
        self.comments.resize(32, 32)
        self.comments.load(SiGlobal.icons.get('fi-rr-comment'))
        self.comments.setHint('评论')

        self.layout_operation.addItem(self.download)
        self.layout_operation.addItem(self.like)
        self.layout_operation.addItem(self.comments)


    def setText(self, title = '', artist = '', album = ''):
        self.title.setText(title)
        self.artist.setText(artist)
        self.artist.setHint('艺术家 {}'.format(artist))
        self.album.setText(album)
        self.album.setHint('专辑 {}'.format(album))

    def setProgress(self, p):
        self.substrate.setStyleSheet('''
            background-color:qlineargradient(x1:{}, y1:0, x2:{}, y2:0,
                                             stop:0 {}, stop:1 {});
            border-radius:6px '''.format(
                p, p+0.00001, '#fed966', colorset.BG_GRAD_HEX[0]
            ))

    def load(self, path):
        self.cover.load(path)
        self.bg.load(path)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        size = event.size()
        w, h = size.width(), size.height()
        self.layout_all_content.resize(w - 48, h - 48)
        self.layout_info.resize(self.layout_all_content.size())
        self.layout_operation.move(
            w - 24 - 32, (h - self.layout_operation.height()) // 2 - 2)
        self.bg.resize(w, h-3)
