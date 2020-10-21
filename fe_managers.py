from classroom import Classroom
from db import Connection, User
import requests
from constants import *
import errors
from flask_login import current_user


def new_connection(uid, classId, webhookUrl, db):
    webhookId, webhookToken = clean_webhook_url(webhookUrl)

    regId, time = Classroom.from_uid(uid, db).register(classId)

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
    elif creds.refresh_token:
        db.add(user)
    else:
        requests.post(
            "https://oauth2.googleapis.com/revoke",
            params={"token": creds.token},
            headers={"content-type": "application/x-www-form-urlencoded"},
        )
        raise errors.LoginError
    return user

    ##TODO error handling


def modify_connection(classId, webhookUrl, db=None):
    webhookId, webhookToken = clean_webhook_url(webhookUrl)
    con = current_user.get_class(classId)
    con.webhookId = webhookId
    con.wehookToken = webhookToken
    db.commit_modification()


def modify_or_add_connection(uid, classId, webhook, db, classroom):
    if current_user.get_class(classId):
        modify_connection(classId, webhook, db)
    else:
        new_connection(uid, classId, webhook, db)


def delete_connection(classId, db, classroom):
    c = current_user.get_class(classId)
    assert c is not None
    classroom.deregister(c)
    db.delete(c)
