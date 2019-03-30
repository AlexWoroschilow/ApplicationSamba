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


class Loader(Loader):

    @property
    def enabled(self):
        return True

    def config(self, binder, options=None, args=None):
        print(12)

        if options is None or args is None: return self

        binder.bind_to_constructor('window.dashboard', self._widget)
        
    @inject.params(widget='window.dashboard')
    def boot(self, binder, options=None, args=None, widget=None):
        if options is None or args is None: return self
        if widget is None: return self

    @inject.params(window='window')
    def _widget(self, window=None):
        if window is None: return None
        from .gui.widget import DashboardWidget
        window.setMainWidget(DashboardWidget())

