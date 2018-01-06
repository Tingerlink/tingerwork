# -*- coding: utf-8 -*-
# Module 'registration' of the project 'tingerwork'
# :date_create: 10.12.2017.0:28
# :author: Tingerlink
# :description:

from flask_classy import route, request
from routes.platforms.web import ApiWeb
from models.registration import RegistrationModel


class Registration(ApiWeb):
    group_name = "registration"

    def __init__(self):
        super().__init__(self.group_name)
        self.model = RegistrationModel()

    @route("registration.checkAvailabilityPhone", methods=["GET", "POST"])
    def registration_check_availability_phone(self):
        return self.action("checkAvailabilityPhone",
                           self.model.registration_check_availability_phone)

    @route("registration.sendVerificationCode", methods=["GET", "POST"])
    def registration_send_verification_code(self):
        return self.action("sendVerificationCode",
                           self.model.registration_send_verification_code)

    @route("registration.signUp", methods=["GET", "POST"])
    def registration_sign_up(self):
        return self.action("signUp",
                           self.model.registration_sign_up)

    @route("registration.drop", methods=["GET", "POST"])
    def registration_drop(self):
        return self.action("drop",
                           self.model.registration_drop)

