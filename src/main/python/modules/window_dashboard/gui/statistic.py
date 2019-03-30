# -*- coding: utf-8 -*-
# Copyright 2015 Alex Woroschilow (alex.woroschilow@gmail.com)
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
import socket
import netifaces
# import interfaces, ifaddresses, AF_INET

from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5.QtCore import Qt

from .label import Text


class StatisticWidget(QtWidgets.QGroupBox):
    activate = QtCore.pyqtSignal(object)

    def __init__(self, parent=None):
        super(StatisticWidget, self).__init__(parent)
        self.setContentsMargins(0, 0, 0, 0)

        layout = QtWidgets.QGridLayout()
        layout.setAlignment(Qt.AlignTop)
        self.setLayout(layout)

        layout.addWidget(Text('Host name:'), 0, 0)
        layout.addWidget(Text(socket.gethostname()), 0, 1)
        for index, ifaceName in enumerate(netifaces.interfaces(), start=1):

            addresses = []
            for interface in netifaces.ifaddresses(ifaceName).setdefault(netifaces.AF_INET, [{'addr': 'No IP addr'}]):
                addresses.append(interface['addr'])

            layout.addWidget(Text('{}:'.format(ifaceName)), index, 0)
            layout.addWidget(Text('{}'.format(', '.join(addresses))), index, 1)
