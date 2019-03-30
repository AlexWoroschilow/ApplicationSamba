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
# WITHOUT WARRANTIES OR CONDITION
import os
import time
import inject
import logging
from watchdog.observers import Observer

from watchdog.events import FileSystemEventHandler


class Watchdog(FileSystemEventHandler):

    def __init__(self):
        self.observer = Observer()
        self.export = False
        self.counter = 0
        self.timeout = 5
    
    def on_any_event(self, event=None):
        if event is None: return None
        logger = logging.getLogger('watchdog')
        logger.info("{}: {}".format(event.event_type, event.src_path))
        self.export = True

    @inject.params(config='config', mailer='mailer')
    def status(self, config=None, mailer=None):
        self.counter = self.counter + 1
        if self.counter < 30 * 60 / self.timeout: return None
        transport = config.get('transfer.transport', 'sftp')
        if transport not in ['sftp', 's-ftp', 'secure-ftp']:
            logger = logging.getLogger('watchdog')
            logger.error("Only sftp protocol is available for now")
            return None
            
        injector = inject.get_injector()
        transport = injector.get_instance('transport-sftp')
        if transport.check(config.get('transfer.to')): return None

        mailer.mail('Kurse: data export service', 'Can not connect to {}'.format(
            config.get('transfer.to')
        ))

    @inject.params(config='config')
    def sleep(self, config=None):
        if config is None: return None
        time.sleep(int(config.get('transfer.timeout', self.timeout)))

    @inject.params(config='config', mailer='mailer')
    def transfer(self, config=None, mailer=None):        
        source = config.get('transfer.from', '')
        if not len(source): return None
        destination = config.get('transfer.to')
        if not len(destination): return None
        
        transport = config.get('transfer.transport', 'sftp')
        if transport not in ['sftp', 's-ftp', 'secure-ftp']:
            logger = logging.getLogger('watchdog')
            logger.error("Only sftp protocol is available for now")
            return None
        
        injector = inject.get_injector()
        transport = injector.get_instance('transport-sftp')
        if not transport.transfer(source, destination):
            mailer.mail('Kurse: data export service', 'Can not transfer data to {}'.format(
                config.get('transfer.to')
            ))
  
        self.export = False

    @inject.params(config='config')
    def run(self, config=None):
        if config is None: return None

        source = config.get('transfer.from', '')

        logger = logging.getLogger('watchdog')                        
        logger.info("Folder to watch: {}".format(source))
        if not os.path.exists(source): return None
        
        self.observer.schedule(self, source, recursive=True)
        self.observer.start()
        try:
            # start monitoring of the given folder 
            # transfer the files collected during the time
            # the server was offline
            self.transfer()
            
            while True:
                if self.export == False: self.status()
                if self.export == False: self.sleep()
                if self.export == True: self.transfer()
                
        except (BaseException) as exception:
            logger.exception(exception)
            self.observer.stop()

        self.observer.join()

