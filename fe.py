import db
from constants import parsetime, clean_webhook_url
from flask import Flask, request, render_template, redirect, url_for
from classroom import Classroom
from db import dbHelper

app = Flask(__name__)
db = dbHelper(app)


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


def delete_connection(classId, db, classroom):
    con = db.find_connection_by_class_id(classId)
    classroom.deregister(con)
    db.delete(con)


def modify_or_add_connection():
    pass


def new_user():
    return


@app.route("/edit", methods=["GET", "POST"])
def edit_page():

    room = Classroom.from_uid(69, db)
    classes = [
        {
            "name": c["name"],
            "id": c["id"],
            "webhook": (
                a.get_webhook_url()
                if (a := db.find_connection_by_class_id(c["id"]))
                else ""
            ),
        }
        for c in room.get_courses()
    ]

    if request.method == "POST":
        # print(request.form)
        for c in classes:
            idd = c["id"]

            if request.form.get("delete-" + idd):
                delete_connection(classid=idd, db=db, classroom=room)

            if request.form["url-" + idd] != c["webhook"]:
                modify_or_add_connection(
                    classId=c["id"], webhook=request.form["url-" + idd]
                )

        return redirect(url_for(edit_page))

    return render_template("edit.html", classes=classes)


app.run(debug=True, port=4000)
