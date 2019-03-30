# -*- coding: utf-8 -*-
# Copyright 2019 Alex Woroschilow (alex.woroschilow@gmail.com)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import os
import socket

from PyQt5 import QtGui
from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5.QtCore import Qt

from .label import Title
from .label import Text
from .button import SourceButton
from .button import StartButton
from .statistic import StatisticWidget


class DashboardWidget(QtWidgets.QGroupBox):
    start = QtCore.pyqtSignal(object)
    networkname = QtCore.pyqtSignal(object)
    source = QtCore.pyqtSignal(object)

    def __init__(self, parent=None):
        super(DashboardWidget, self).__init__(parent)
        self.setContentsMargins(0, 0, 0, 0)

        layout = QtWidgets.QGridLayout()
        layout.setAlignment(Qt.AlignTop)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

        layout.addWidget(Title('Server settings'), 0, 0, 1, 2)

        layout.addWidget(Text('Network name:'), 1, 0)

        widget_network_name = QtWidgets.QLineEdit(socket.gethostname())
        widget_network_name.textEdited.connect(self.networkname.emit)
        layout.addWidget(widget_network_name, 1, 1)

        layout.addWidget(Text('Network share:'), 2, 0)

        widget_button_source = SourceButton(os.path.expanduser('~'))
        widget_button_source.clicked.connect(self.source.emit)
        layout.addWidget(widget_button_source, 2, 1)

        widget_button_start = StartButton(QtGui.QIcon('icons/start'), None)
        widget_button_start.clicked.connect(self.start.emit)
        layout.addWidget(widget_button_start, 3, 0, 1, 2)

        layout.addWidget(Title('Server information'), 4, 0, 1, 2)
        layout.addWidget(StatisticWidget(), 5, 0, 1, 2)
