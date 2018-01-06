# -*- coding: utf-8 -*-
# Module 'db_create' of the project 'tingerwork'
# :date_create: 10.12.2017.1:22
# :author: Tingerlink
# :description:

import sys

if not (sys.platform == 'win32'):
    APP_PATH = "/var/www/tingerwork/app/"
    sys.path.insert(0, APP_PATH)

import db.schema

db.schema.migrate()

