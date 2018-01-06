# -*- coding: utf-8 -*-
# Module 'auth' of the project 'tingerwork'
# :date_create: 21.12.2017.3:01
# :author: Tingerlink
# :description:

from flask_classy import route, request
from routes.platforms.web import ApiWeb
from models.auth import AuthModel


class Auth(ApiWeb):
    group_name = "auth"

    def __init__(self):
        super().__init__(self.group_name)
        self.model = AuthModel()

    @route("auth.token", methods=["GET", "POST"])
    def auth_token(self):
        return self.action("token",
                           self.model.auth_token)
