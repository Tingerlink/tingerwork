# -*- coding: utf-8 -*-
# Module 'builder' of the project 'tingerwork'
# :date_create: 10.12.2017.0:37
# :author: Tingerlink
# :description:

from flask import jsonify

import tools.logger as logger

ERRORS = {
    "1": "Unknown error",
    "2": "Transferred to unknown method",
    "3": "Bad request",
    "4": "Many requests per minute",
    "5": "Phone number is incorrect",
    "6": "Incorrect secret key",
    "7": "The user already exists",
    "8": "Secret key obsolete",
    "9": "Registration session not found",
    "10": "The user is not found",
    "11": "Unknown api device lib",
    "500": "Internal server error"
}


class Error:
    def __init__(self, code=500, msg="", args=None, log=True, variant="error"):
        self.code = code
        self.msg = msg.replace('"', "'")
        self.args = args if args else dict()

        if log:
            logger.log(code, msg, variant)


    def get_response_data(self):
        """
        :return: Response in json
        """
        if not (str(self.code) in ERRORS.keys()):
            self.code = 1

        msg = ERRORS[str(self.code)]

        if self.code != 500:
            self.msg = "%s. %s" % (ERRORS[str(self.code)], self.msg)
        else:
            self.msg = msg

        data = {
            "code": self.code,
            "msg": self.msg,
            "params": self.args
        }

        return data


def create_response(params):
    """
    :param params: The result of the request
    :return: Response in jsonify
    """
    response = {
        "response": params
    }

    return jsonify(response)


def create_error_response(params):
    """
    :param params: The result of the request
    :return: Response in jsonify
    """
    response = {
        "error": params
    }

    return jsonify(response)

