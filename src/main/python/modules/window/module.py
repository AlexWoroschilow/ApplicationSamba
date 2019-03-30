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
import os
import inject
import functools

from lib.plugin import Loader

from PyQt5 import QtWidgets
from PyQt5 import QtCore

from PyQt5.QtCore import Qt

from .gui.window import MainWindow


class Loader(Loader):

    @property
    def enabled(self):
        return True

    def config(self, binder, options=None, args=None):
        if options is None or args is None: return self

        widget = MainWindow()
        widget.setWindowTitle('Samba server')
        binder.bind('window', widget)

        if not os.path.exists('css/stylesheet.qss'): return widget
        widget.setStyleSheet(open('css/stylesheet.qss').read())

        if not os.path.exists('icons/icon.svg'): return widget
        widget.setWindowIcon(QtGui.QIcon('icons/icon.svg'))
        
