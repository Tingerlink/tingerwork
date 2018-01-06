# -*- coding: utf-8 -*-
# Module '__init__.py' of the project 'tingerwork'
# :date_create: 10.12.2017.23:25
# :author: Tingerlink
# :description:

import db.schema as db
import hashlib

from sqlalchemy.orm import sessionmaker
from models import ModelContainer
from datetime import datetime, timedelta
from sqlalchemy import desc
from models.registration.phone_sender import PhoneSender
from routes.tools.response_builder import Error


class AuthModel(ModelContainer):
    def __init__(self):
        super().__init__()
        self.maker = sessionmaker(bind=db.engine)

    def auth_token(self, args):
        """
        Получение токена доступа к методам
        :return: Getting access token
        """
        def logic(session, params):
            if not ("device_type" in params.keys()) or params["device_type"] == "":
                params["device_type"] = "web"

            device_type = session.query(db.DeviceType).filter_by(name=params["device_type"]).first()
            if not device_type:
                return Error(code=11, log=False, args=params)

            params["password"] = hashlib.sha256(params["password"].encode('utf-8')).hexdigest()

            entry_point = session.query(db.EntryPoint).filter_by(phone=params["phone"],
                                                                 password=params["password"]).first()
            if not entry_point:
                return Error(code=10, log=False, args=params)

            token = None

            while not token or session.query(db.AccessSession).filter_by(token=token).first():
                token = params["phone"] + params["password"] + str(datetime.now())
                token = hashlib.sha512(token.encode('utf-8')).hexdigest()

            session.query(db.AccessSession).filter_by(code_entry_point=entry_point.code,
                                                      code_device_type=device_type.code).delete()

            access_session = db.AccessSession(code_entry_point=entry_point.code,
                                              code_device_type=device_type.code,
                                              token=token,
                                              ip=params["ip"])

            session.add(access_session)

            return {"token": token, "code_user": entry_point.code, "expires_in": access_session.expires_in}

        return self.db_procedure(logic, args)
