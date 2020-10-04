from sqlalchemy import Column, Integer, String, PickleType, DateTime, create_engine
from sqlalchemy.ext.declarative import declarative_base
from secret import sqlurl
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    uid = Column(String(255), primary_key=True)
    token = Column("token", PickleType(protocol=4))

    def is_authenticated(self):
        try:
            return self.token and self.token.valid
        except:
            return False

    def is_active(self):
        return True  ###TODO Look at this

    def is_anonymous(self):
        if uid:
            return False
        return True

    def get_id(self):
        return self.uid

    def __repr__(self):
        return "<User %r>" % self.uid


class Connection(db.Model):

    uid = Column(String(255))
    classId = Column(String(50), primary_key=True)
    webhookId = Column(String(50))
    webhookToken = Column(String(120))
    registration = Column(String(50))
    expire = Column(DateTime)

    def get_webhook_url(self):
        return (
            f"https://discordapp.com/api/webhooks/{self.webhookId}/{self.webhookToken}"
        )

    def __repr__(self):
        return "<Connection %r>" % self.classId


def create(app):
    app.config["SQLALCHEMY_DATABASE_URI"] = sqlurl
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)
    with app.app_context():
        db.create_all()


class dbHelper:
    Base = declarative_base()
    db = db

    def __init__(self, app):
        app.config["SQLALCHEMY_DATABASE_URI"] = sqlurl

        app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
        self.db.init_app(app)

    def add(self, o):
        session = self.db.session  ###!!!!!!!! maybe self.db here
        session.add(o)
        session.commit()

    def delete(self, o):
        session = self.db.session  ###!!!!!!!! maybe self.db here
        session.delete(o)
        session.commit()

    def commit_modification(self):
        self.db.session.commit()

    def find_connection_by_class_id(self, classId):
        return Connection.query.filter_by(classId=classId).first()

    def find_user_by_id(self, id):
        return User.query.filter_by(uid=id).first()
