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
import glob
import logging
import importlib
import functools
import inject


class Kernel(object):

    loaders = []

    def __init__(self, options=None, args=None, sources=[]):
        self.options = options
        self.sources = sources
        self.args = args

        inject.configure(self.configure)

        logger = logging.getLogger('kernel')
        for index, loader in enumerate(self.loaders, start=1):
            logger.info('{}. boot: {}'.format(index, loader))
            if not hasattr(loader.__class__, 'boot'): continue
            if not callable(getattr(loader.__class__, 'boot')): continue
            loader.boot(options, args)

    def get(self, name=None):
        if name is None: return None
        container = inject.get_injector()
        return container.get_instance(name)

    def append(self, module=None):
        if module is None: return self
        self.loaders.append(module)
        return self

    def configure(self, binder):
        
        logger = logging.getLogger('kernel')
        for source in self.modules(self.sources):
            try:
                module = importlib.import_module(source, False)
                with module.Loader(self.options, self.args) as loader:
                    if not hasattr(loader.__class__, 'enabled'): continue
                    if loader.enabled == True: self.append(loader)
                    if loader.enabled == False: continue
                    
                    if not hasattr(loader.__class__, 'config'): continue
                    if not callable(getattr(loader.__class__, 'config')): continue
                    logger.info("configure: {}".format(loader))
                            
                    binder.install(functools.partial(
                        loader.config, options=self.options, args=self.args
                    ))
                    
            except (SyntaxError, RuntimeError) as ex:
                logger.critical("{}: {}".format(source, ex))

        binder.bind('logger', logging.getLogger('app'))
        binder.bind('kernel', self)

    def modules(self, sources=None):
        
        logger = logging.getLogger('kernel')
        for location, mask in sources:
            for source in glob.glob('{}/{}'.format(location, mask)):
                if not os.path.exists(source): continue
                logger.info('found: {}'.format(source))
                source = source.replace('{}/'.format(location), '')
                source = source.replace('.py', '')
                source = source.replace('/', '.')
                yield source

