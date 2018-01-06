# -*- coding: utf-8 -*-
# Module '__init__.py' of the project 'tingerwork'
# :date_create: 10.12.2017.0:28
# :author: Tingerlink
# :description:


from flask_classy import FlaskView
from flask_classy import route, request

from routes.tools import response_builder
from routes.tools.request_validator import RequestValidator
from tools import yaml_linker as schema


class ApiWeb(FlaskView):
    route_base = '/web/'

    def __init__(self, group_name):
        self.validator = RequestValidator()
        self.group_name = group_name
        self.group_schema = schema.get_methods()[group_name]

    def action(self, method_name, logic, logic_args=None):
        args = request.args.to_dict(flat=True)
        args.update({"ip": request.remote_addr})

        if logic_args:
            args.update(logic_args)

        error = self.validator.check(self.group_schema[method_name], args)

        if error:
            return response_builder.create_error_response(error.get_response_data())

        result = logic(args)

        if type(result) is response_builder.Error:
            return response_builder.create_error_response(result.get_response_data())

        return response_builder.create_response(result)
