# -*- coding: utf-8 -*-
# Module 'yaml_linker.py' of the project 'tingerwork'
# :date_create: 04.12.2017.23:58
# :author: Tingerlink
# :description: Модуль компануют объекты схемы API в одну сущность


import yaml
import copy

from config import settings

METHODS_PATH = settings.APP_PATH + "schema/methods.yaml"
RESPONSES_PATH = settings.APP_PATH + "schema/responses.yaml"
FORMATS_PATH = settings.APP_PATH + "schema/formats.yaml"


st = {
    "${hostname}": settings.HOST_IP
}


def insert_resource(schema, resource, tag):
    for key, val in schema.items():
        if key == tag:
            new_key = copy.deepcopy(key).replace('$ref_', '')

            schema[key] = (resource[val] if val in resource.keys() else None)
            schema[new_key] = schema.pop(key)

        elif type(val) is dict:
            schema[key] = insert_resource(val, resource, tag)
        elif type(val) is list:
            for item in val:
                item = insert_resource(item, resource, tag)
    return schema


def get_methods():
    responses = yaml.load(open(RESPONSES_PATH))
    methods = yaml.load(open(METHODS_PATH))
    formats = yaml.load(open(FORMATS_PATH))

    data = insert_resource(methods, responses, tag="$ref_response")
    data = insert_resource(data, formats, tag="$ref_format")

    return static_rewrite(data)


def get_short_methods():
    methods = yaml.load(open(METHODS_PATH))

    return static_rewrite(methods)


def static_rewrite(schema):
    dump = yaml.dump(schema)
    for key, item in st.items():
        dump = dump.replace(key, item)

    return yaml.load(dump)