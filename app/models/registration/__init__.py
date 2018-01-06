# -*- coding: utf-8 -*-
# Module '__init__.py' of the project 'tingerwork'
# :date_create: 12.12.2017.0:35
# :author: Tingerlink
# :description:

import db.schema as db
import hashlib

from datetime import datetime, timedelta
from sqlalchemy.orm import sessionmaker
from sqlalchemy import desc
from models import ModelContainer
from models.registration.phone_sender import PhoneSender
from routes.tools.response_builder import Error


class RegistrationModel(ModelContainer):

    COUNT_SECRET_KEY_SENDS = 3

    def __init__(self):
        super().__init__()
        self.maker = sessionmaker(bind=db.engine)

    def registration_check_availability_phone(self, args):
        """
        Проверка доступности номера телефона
        :return: The presence of the phone in the database
        """
        def logic(session, params):
            return not session.query(db.EntryPoint).filter_by(phone=params["phone"]).first()

        return self.db_procedure(logic, args)

    def registration_send_verification_code(self, args):
        """
        Отправка кода верификации номера телефона при регистрации
        :return: Status of about sending verification code
        """
        def logic(session, params):
            if session.query(db.EntryPoint).filter_by(phone=params["phone"]).first():
                return Error(code=7, log=False)

            delta = datetime.now() - timedelta(seconds=60)
            result = session.query(db.RegistrationSession).filter(db.RegistrationSession.phone == params["phone"],
                                                                  db.RegistrationSession.date_request > delta).first()
            if result:
                return Error(code=4, log=False)

            sender = PhoneSender()
            response, status = sender.call(params["phone"])
            print(type(response))
            if status is False:
                return Error(code=5, log=False)
            elif status is None:
                return Error(code=500, msg="Phone calling error")
            else:
                registration_session = db.RegistrationSession(phone=params["phone"],
                                                              secret_key=response["code"],
                                                              ip=params["ip"])
                session.add(registration_session)

                return True

        return self.db_procedure(logic, args)

    def registration_sign_up(self, args):
        """
        Регистрация нового пользователя
        :return: True or Error
        """
        def logic(session, params):
            if session.query(db.EntryPoint).filter_by(phone=params["phone"]).first():
                return Error(code=7, log=False)

            registration_session = session.query(db.RegistrationSession) \
                .filter_by(phone=params["phone"]).order_by(desc(db.RegistrationSession.date_request)).first()

            if not registration_session:
                return Error(code=9, log=False, args=params)

            session.add(db.RegistrationSessionRequest(registration_session.code))

            reg_requests = session.query(db.RegistrationSessionRequest)\
                .filter_by(code_registration_session=registration_session.code).all()

            if reg_requests and (len(reg_requests) > self.COUNT_SECRET_KEY_SENDS):
                session.query(db.RegistrationSessionRequest).filter_by(
                    code_registration_session=registration_session.code).delete()
                session.query(db.RegistrationSession).filter_by(code=registration_session.code).delete()

                return Error(code=8, log=False, args=params)

            if registration_session.secret_key != params["secret_key"]:
                return Error(code=6, log=False, args=params)

            params["password"] = hashlib.sha256(params["password"].encode('utf-8')).hexdigest()
            session.add(db.EntryPoint(phone=params["phone"], password=params["password"]))

            session.query(db.RegistrationSessionRequest).filter_by(
                code_registration_session=registration_session.code).delete()
            session.query(db.RegistrationSession).filter_by(phone=params["phone"]).delete()

            return True

        return self.db_procedure(logic, args)

    def registration_drop(self, args):
        """
        Удаление всего
        :return: True or Error
        """
        def logic(session, params):
            session.query(db.RegistrationSessionRequest).delete()
            session.query(db.RegistrationSession).delete()
            session.query(db.EntryPoint).delete()

            return True

        return self.db_procedure(logic, args)
