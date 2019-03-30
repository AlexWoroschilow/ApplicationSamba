#! /usr/bin/python3
#
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
import sys
import inject
import logging
import optparse

from PyQt5 import QtWidgets

from lib.kernel import Kernel

abspath = os.path.abspath(__file__)
os.chdir(os.path.dirname(abspath))

sys.path.append(os.path.join(os.getcwd(), 'lib'))
sys.path.append(os.path.join(os.getcwd(), 'modules'))


class Application(QtWidgets.QApplication):
    kernel = None

    def __init__(self, options=None, args=None):
        super(Application, self).__init__(sys.argv)
        self.setApplicationName('Samba server')

        self.kernel = Kernel(options, args, [
            (os.getcwd(), "modules/**/module.py")
        ])


    @inject.params(kernel='kernel',config='config', widget='window')
    def exec_(self, kernel=None,config=None, widget=None):
        if kernel is None: return None
        if config is None: return None
        if widget is None: return None

        width = int(config.get('window.width', 400))
        height = int(config.get('window.height', 500))  
        widget.resize(width, height)

        widget.show()

        return super(Application, self).exec_()


if __name__ == "__main__":
    parser = optparse.OptionParser()

    parser.add_option("--loglevel", default=logging.DEBUG, dest="loglevel", help="Logging level")
    parser.add_option("--logfile", default='default.log', dest="logfile", help="Logfile location")
    parser.add_option("--config", default='default.conf', dest="config", help="Config file location")

    (options, args) = parser.parse_args()

    log_format = '[%(relativeCreated)d][%(name)s] %(levelname)s - %(message)s'
    logging.basicConfig(level=options.loglevel, format=log_format)

    application = Application(options, args)
    sys.exit(application.exec_())
