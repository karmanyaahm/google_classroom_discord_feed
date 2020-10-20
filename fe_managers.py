from classroom import Classroom
from db import Connection, User
import requests
from constants import *


def new_connection(uid, classId, webhookUrl, db):
    regId, time = Classroom.from_uid(uid, db).register(classId)

    webhookId, webhookToken = clean_webhook_url(webhookUrl)
    con = Connection(
        uid=uid,
        classId=classId,
        webhookId=webhookId,
        webhookToken=webhookToken,
        registration=regId,
        expire=parsetime(time),
    )
    db.add(con)


def add_or_update_user(creds, db):
    url = "https://openidconnect.googleapis.com/v1/userinfo"
    head = {"Authorization": "Bearer " + creds.token}
    response = requests.get(url, headers=head)
    idd = response.json()["sub"]
    user = User(uid=idd, token=creds)
    if (a := db.find_user_by_id(idd)) :
        if creds.refresh_token:
            a.token = creds
            user = a
            db.commit_modification()
        ##or just log in
    else:
        db.add(user)
    return user

    ##TODO error handling


def modify_connection(classId, webhookUrl, db):
    webhookId, webhookToken = clean_webhook_url(webhookUrl)
    con = db.find_connection_by_class_id(classId)
    con.webhookId = webhookId
    con.wehookToken = webhookToken
    db.commit_modification()


def modify_or_add_connection(uid, classId, webhook, db,classroom):
    if a := db.find_connection_by_class_id(classId):
        modify_connection(classId, webhook, db)
    else:
        new_connection(uid, classId, webhook, db)


def delete_connection(classId, db, classroom):
    con = db.find_connection_by_class_id(classId)
    classroom.deregister(con)
    db.delete(con)
