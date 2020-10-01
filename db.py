from sqlalchemy import Column, Integer, String, PickleType, create_engine
from sqlalchemy.ext.declarative import declarative_base

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    uid = Column(Integer, primary_key=True)
    token = Column("token", PickleType(protocol=4))

    def __repr__(self):
        return "<User %r>" % self.uid


class Connection(db.Model):

    uid = Column(Integer)
    classId = Column(String(50), primary_key=True)
    webhookId = Column(String(50))
    webhookToken = Column(String(120))
    def get_webhook_url(self):
        return f"https://discordapp.com/api/webhooks/{self.webhookId}/{self.webhookToken}"

    def __repr__(self):
        return "<Connection %r>" % self.classId


def create(app):
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///tmp.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)
    with app.app_context():
        db.create_all()


class dbHelper:
    Base = declarative_base()
    db = db

    def __init__(self, app):
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///tmp.db"

        app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
        self.db.init_app(app)

    def add(self, o):
        session = self.db.session  ###!!!!!!!! maybe self.db here
        session.add(o)
        session.commit()

    def find_connection_by_class_id(self, classId):
        return Connection.query.filter_by(classId=classId).first()

    def find_user_by_id(self, id):
        return User.query.filter_by(uid=id).first()
