# -*- coding: utf-8 -*-
# Module 'docs.py' of the project 'tingerwork'
# :date_create: 04.12.2017.1:33
# :author: Tingerlink
# :description:

from flask_classy import route, request
from flask_classy import FlaskView
from flask import jsonify, render_template
from tools import yaml_linker
from config import settings


class Index(FlaskView):
    route_base = '/'

    @route("/", methods=["GET"])
    def docs_start(self):
        params = {
            "title": "API Tingerwork"
        }
        return render_template("docs/pages/index.html", **params)




    @route("/docs/web/schema/methods", methods=["GET"])
    def docs_schema_methods(self):
        short = request.args.get('short')
        if short:
            data = yaml_linker.get_short_methods()
        else:
            data = yaml_linker.get_methods()

        return jsonify(data)


    @route("/docs/platforms/web/<string:group>/<string:method>", methods=["GET"])
    def method(self):
        params = {
            "title": "API common info",
            "host_ip": settings.HOST_IP
        }
        return render_template("docs/web.html", **params)
