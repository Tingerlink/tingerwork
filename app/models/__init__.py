# -*- coding: utf-8 -*-
# Module '__init__.py' of the project 'tingerwork'
# :date_create: 16.12.2017.01:03
# :author: Tingerlink
# :description:

import db.schema as db

from sqlalchemy.orm import sessionmaker
from routes.tools.response_builder import Error


class ModelContainer:
    def __init__(self):
        self.maker = sessionmaker(bind=db.engine)

    def db_procedure(self, action, args):
        session = self.maker()
        try:
            result = action(session, args)
            session.commit()

            return result
        except Exception as err:
            session.rollback()
            return Error(code=500, msg=str("%s | %s" % (action.__name__, err)))
        finally:
            session.close()

    @staticmethod
    def procedure(action, args):
        try:
            return action(args)
        except Exception as err:
            return Error(code=500, msg=str("%s | %s" % (action.__name__, err)))
