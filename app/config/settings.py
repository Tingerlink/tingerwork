# -*- coding: utf-8 -*-
# Module 'settings' of the project 'tingerwork'
# :date_create: 05.12.2017.3:26
# :author: Tingerlink
# :description:

import sys

CONNECT_STRING = "postgresql://tingerwork:wlOxmomDidDVukzSW25K@localhost/tingerwork"

LOGGER = True
CALLING_LOGIN = "xcrea"
CALLING_PASS = "KbKYnK9RiXjtGEUbBWpNCyFRIE7qr0l6"
HOST_NAME = "web.tingerwork.com"

if sys.platform == 'win32':
    APP_PATH = ""
    HOST_IP = "http://127.0.0.1:5000"
    LOG_ERROR = "logs/error.log"
    LOG_WARNING = "logs/warning.log"
else:
    APP_PATH = "/var/www/tingerwork/app/"
    HOST_IP = "http://web.tingerwork.com"
    LOG_ERROR = "/var/www/tingerwork/app/logs/error.log"
    LOG_WARNING = "/var/www/tingerwork/app/logs/warning.log"


