# -*- coding: utf-8 -*-
# Module '__init__.py' of the project 'tingerwork'
# :date_create: 03.12.2017.14:43
# :author: Tingerlink
# :description:

import sys

HOME_PATHS = ["/var/www/tingerwork/app"]


def add_sys_paths():
    for path in HOME_PATHS:
        sys.path.insert(0, path)


add_sys_paths()

