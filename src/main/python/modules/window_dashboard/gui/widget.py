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
from .button import SourceButton
from .button import StartButton

class DashboardWidget(QtWidgets.QWidget):

    tab = QtCore.pyqtSignal(object)

    def __init__(self, parent=None):
        super(DashboardWidget, self).__init__(parent)
        self.setContentsMargins(0, 20, 0, 20)
        
        layout = QtWidgets.QGridLayout()
        layout.setAlignment(Qt.AlignTop)
        layout.setContentsMargins(0, 20, 0, 20)
        self.setLayout(layout)

        layout.addWidget(Title('Server name'))
        layout.addWidget(QtWidgets.QLineEdit(socket.gethostname()))

        layout.addWidget(StartButton(QtGui.QIcon('icons/start'), None))

        source = SourceButton('Folder to share: {}'.format(os.path.expanduser('~')))
        layout.addWidget(source)
