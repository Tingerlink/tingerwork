# -*- coding: utf-8 -*-
# Module 'call' of the project 'tingerwork'
# :date_create: 10.12.2017.22:31
# :author: Tingerlink
# :description: DB table Call, fix user list confirmation phone

import sqlalchemy as sql
import config.settings

from datetime import datetime, timedelta
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, func, Sequence
from sqlalchemy import event, DDL


declarative = declarative_base()

DEBUG = True

# Регистрация
#   Создание сессии при запросе кода
#   Создание точки входа
# Авторизация
#   Проверка наличия токена доступа
#       а) Токена нет: создание токена
#       б) Токен есть: обновление
# ########################################################################################################


class EntryPoint(declarative):
    """
    Точка входа, создаётся при регистрации
    При создании нового объекта необходимо удалить все сессии регистрации
    """
    __tablename__ = "entry_point"

    code = sql.Column("code", sql.Integer, primary_key=True)
    phone = sql.Column("phone", sql.String(15), unique=True, nullable=False)
    password = sql.Column("password", sql.String(64), nullable=False)
    date_create = sql.Column("date_create", sql.DateTime, nullable=False, default=func.now())

    def __init__(self, phone, password):
        self.phone = phone
        self.password = password


class RegistrationSessionRequest(declarative):
    __tablename__ = "registration_session_request"

    code = sql.Column("code", sql.Integer, primary_key=True)
    code_registration_session = sql.Column("code_registration_session",
                                           sql.Integer,
                                           sql.ForeignKey("registration_session.code"),
                                           nullable=False)
    date_request = sql.Column("date_request", sql.DateTime, nullable=False, default=func.now())

    def __init__(self, code_registration_session, ):
        self.code_registration_session = code_registration_session


class RegistrationSession(declarative):
    """
    Сессия регистрации
    Создаётся при запросе кода для регистрации, буферная таблица, и не связана с остальными
    """
    __tablename__ = "registration_session"

    code = sql.Column("code", sql.Integer, primary_key=True)
    phone = sql.Column("phone", sql.String(15), nullable=False)
    date_request = sql.Column("date_request", sql.DateTime, nullable=False)
    secret_key = sql.Column("secret_key", sql.String(6), nullable=False)
    ip = sql.Column("ip", sql.String(15), nullable=True)

    def __init__(self, phone, secret_key, ip=""):
        self.phone = phone
        self.secret_key = secret_key
        self.date_request = datetime.now()
        self.ip = ip


class AccessSession(declarative):
    """
    Сессия доступа к API для конкретного девайса
    """
    __tablename__ = "access_session"

    code = sql.Column("code", sql.Integer, primary_key=True)
    code_entry_point = sql.Column("code_entry_point", sql.Integer, sql.ForeignKey("entry_point.code"), nullable=False)
    code_device_type = sql.Column("code_device_type", sql.Integer, sql.ForeignKey("device_type.code"), nullable=False)
    expires_in = sql.Column("expires_in", sql.Integer, nullable=False)
    date_create = sql.Column("date_create", sql.DateTime, nullable=False, default=func.now())
    token = sql.Column("token", sql.String(128), nullable=False, unique=True)
    ip = sql.Column("ip", sql.String(15), nullable=True)

    def __init__(self, code_entry_point, code_device_type, token, ip, period=3600):
        self.code_entry_point = code_entry_point
        self.code_device_type = code_device_type
        self.expires_in = period
        self.token = token
        self.ip = ip



class Methods(declarative):
    __tablename__ = "methods"

    code = sql.Column("code", sql.Integer, primary_key=True)
    name = sql.Column("name", sql.String(128), unique=True, nullable=False)

    def __init__(self, name):
        self.name = name


class DeviceType(declarative):
    __tablename__ = "device_type"

    code = sql.Column("code", sql.Integer, primary_key=True)
    name = sql.Column("name", sql.String(32), unique=True, nullable=False)

    def __init__(self, name):
        self.name = name


class Limits(declarative):
    """
    Лимиты выполнения методов
    """
    __tablename__ = "limits"

    code = sql.Column("code", sql.Integer, primary_key=True)
    in_second = sql.Column("in_second", sql.Integer)
    in_minute = sql.Column("in_minute", sql.Integer)
    in_hours = sql.Column("in_hours", sql.Integer)
    in_day = sql.Column("in_day", sql.Integer)


class Request(declarative):
    """
    Запросы к API
    """
    __tablename__ = "request"

    code = sql.Column("code", sql.Integer, primary_key=True)
    code_access = sql.Column("code_access", sql.Integer, nullable=False)
    code_method = sql.Column("code_method", sql.Integer, nullable=False)

    def __init__(self, code_access, code_method):
        self.code_access = code_access
        self.code_method = code_method


engine = create_engine(config.settings.CONNECT_STRING, echo=False)


def inset_default_values():
    from sqlalchemy.orm import sessionmaker
    maker = sessionmaker(bind=engine)
    session = maker()

    try:
        device_types = [
            DeviceType("web"),
            DeviceType("android"),
            DeviceType("mweb")
        ]

        for item in device_types:
            session.add(item)
        session.commit()

    except Exception as err:
        session.rollback()
    finally:
        session.close()


def migrate():
    try:
        if DEBUG:
            AccessSession.__table__.drop(engine)
            RegistrationSessionRequest.__table__.drop(engine)
            RegistrationSession.__table__.drop(engine)
            
            Request.__table__.drop(engine)
            EntryPoint.__table__.drop(engine)
            Methods.__table__.drop(engine)
            Limits.__table__.drop(engine)
            DeviceType.__table__.drop(engine)

    except Exception as err:
        pass
    finally:
        declarative.metadata.create_all(engine)
        inset_default_values()
