# -*- coding: utf-8 -*-
# Module 'request_parser' of the project 'tingerwork'
# :date_create: 10.12.2017.23:52
# :author: Tingerlink
# :description:


import re

from routes.tools.response_builder import Error


class RequestValidator:
    """The class implements methods for verifying the query parameters for the API"""

    def check(self, method_schema, args):
        result = self.check_required_parameters(method_schema, args)
        if result:
            return Error(code=3, msg=result, args=args)

        result = self.check_value_parameters(method_schema, args)
        if result:
            return Error(code=3, msg=result, args=args)

        return None

    @staticmethod
    def check_required_parameters(method_schema, request_params):
        """Checking for all required parameters in the query
        :param method_schema: description of the web method
        :type method_schema: dict()
        :param request_params: request parameters
        :type request_params: dict()
        :return: error string
        :rtype: str
        """
        for param_schema in method_schema["parameters"]:
            if param_schema["required"] and not(param_schema["name"] in request_params.keys()):
                return "Missing required parameter '{0}'".format(param_schema["name"])
        return None

    def check_value_parameters(self, method_schema, request_params):
        """Checking for all required parameters in the query by regular expression
        :param method_schema: description of the web method
        :type method_schema: dict()
        :param request_params: request parameters
        :type request_params: dict()
        :return: error string
        :rtype: str
        """

        for param_schema in method_schema["parameters"]:
            if (param_schema["required"] and
                    not self.regular_check(request_params[param_schema["name"]], param_schema["format"])):
                return "Parameter '{0}' contains non-valid characters ".format(param_schema["name"])
        return None

    @staticmethod
    def regular_check(value, expression):
        prog = re.compile(expression)
        result = prog.match(value)

        return bool(result)