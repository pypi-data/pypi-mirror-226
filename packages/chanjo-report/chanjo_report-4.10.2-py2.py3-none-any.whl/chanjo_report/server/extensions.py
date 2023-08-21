from alchy import make_declarative_base, QueryModel, ManagerMixin
from chanjo.store.models import BASE
from flask_sqlalchemy import SQLAlchemy
from threading import get_ident


class Alchy(SQLAlchemy, ManagerMixin):
    """Flask extension that integrates alchy with Flask-SQLAlchemy.
    Originally developed in Flask-Alchy (https://github.com/dgilland/flask-alchy).
    It has some changes here due to deprecated code in required libs (flask and flask_sqlalchemy)
    """

    def __init__(
        self, app=None, use_native_unicode=True, session_options=None, Model=None, metadata=None
    ):
        if session_options is None:
            session_options = {}

        session_options.setdefault("query_cls", QueryModel)
        session_options.setdefault("scopefunc", get_ident)

        self.Model = Model
        self.make_declarative_base(Model)

        super(Alchy, self).__init__(app, use_native_unicode, session_options, metadata=metadata)

        self.Query = session_options["query_cls"]

    def __getattr__(self, attr):
        """Delegate all other attributes to self.session"""
        return getattr(self.session, attr)


api = Alchy(Model=BASE)
