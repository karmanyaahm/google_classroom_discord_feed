from sqlalchemy import (
    Column,
    Integer,
    String,
    PickleType,
    DateTime,
    create_engine,
    ForeignKey,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from secret import sqlurl
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = "user"
    uid = Column(String(255), primary_key=True)
    token = Column("token", PickleType(protocol=4))
    connections = relationship("Connection", back_populates="user")

    def get_class(self,classId):
        for c in self.connections:
            if c.classId == classId:
                return c
        return None

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
    __tablename__ = "connection"
    uid = Column(String(255), ForeignKey("user.uid"))
    classId = Column(String(50), primary_key=True)
    webhookId = Column(String(50))
    webhookToken = Column(String(120))
    registration = Column(String(50))
    expire = Column(DateTime)
    user = relationship("User", back_populates="connections")
    __table_args__ = (UniqueConstraint(classId.name, webhookId.name),)

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

    def find_connections_by_class_id(self, classId):
        return Connection.query.filter_by(classId=classId).all()

    def find_user_by_id(self, id):
        return User.query.filter_by(uid=id).first()

    def find_connection_by_expire(self, end: datetime, start: datetime = None):
        if not start:
            return Connection.query.filter(Connection.expire <= end).all()
        return Connection.query.filter(
            Connection.expire >= start, Connection.expire <= end
        ).all()
