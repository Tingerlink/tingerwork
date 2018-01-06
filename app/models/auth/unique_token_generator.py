# -*- coding: utf-8 -*-
# Module 'unique_token_generator' of the project 'tingerwork'
# :date_create: 21.12.2017.3:56
# :author: Tingerlink
# :description:


import hashlib


def create_unique_token(text):
    token = hashlib.sha512(text.encode('utf-8')).hexdigest()

