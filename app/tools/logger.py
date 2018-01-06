# -*- coding: utf-8 -*-
# Module 'loger' of the project 'tingerwork'
# :date_create: 11.12.2017.2:44
# :author: Tingerlink
# :description:

import config.settings

from datetime import datetime


def log(code, msg, variant="error"):
    if not config.settings.LOGGER:
        return

    path = config.settings.LOG_ERROR if (variant == "error") else config.settings.LOG_WARNING

    file = open(path, "a")
    file.write("[%s]:(%s) %s\n" % (datetime.now(), code, msg))
    file.close()
