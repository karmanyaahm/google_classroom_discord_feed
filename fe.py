import db
from constants import parsetime, clean_webhook_url, scopes
from flask import Flask, request, render_template, redirect, url_for
from classroom import Classroom
from db import dbHelper, Connection
from fe_managers import *
from secret import secret_key
from flask_login import (
    LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user,
)
import google.oauth2.credentials
import google_auth_oauthlib.flow
import os
from werkzeug.middleware.proxy_fix import ProxyFix


os.environ["OAUTHLIB_RELAX_TOKEN_SCOPE"] = "true"


app = Flask(__name__)

app.secret_key = secret_key
app = ProxyFix(app, x_for=1, x_host=1)

db = dbHelper(app)


login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(u):
    return db.find_user_by_id(u)  # should return none if none


@app.route("/")
def root():
    return render_template("index.html")

def httpsit(st):
    return redirect("https://" + st.split("://")[1])

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect('/')



@app.route("/login")
def login():
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        "credentials_new.json", scopes=scopes
    )
    flow.redirect_uri = request.base_url+ "/callback"
    authorization_url, state = flow.authorization_url(
        access_type="offline",
    )
    return redirect(authorization_url)

    ##TODO security: implement state for csrf etc


@app.route("/login/callback")
def callback():
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        "credentials_new.json", scopes=scopes
    )
    flow.redirect_uri = httpsit(request.base_url)

    authorization_response = httpsit(request.url)
    flow.fetch_token(authorization_response=authorization_response)

    credentials = flow.credentials

    user = add_or_update_user(credentials, db)
    login_user(user)
    return redirect( "/edit")


@app.route("/edit", methods=["GET", "POST"])
@login_required
def edit_page():
    uid = current_user.uid
    room = Classroom.from_uid(uid, db)
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
                delete_connection(classId=idd, db=db, classroom=room)

            if request.form["url-" + idd] != c["webhook"]:
                modify_or_add_connection(
                    uid=uid, classId=c["id"], webhook=request.form["url-" + idd], db=db
                )

        return redirect( "/edit")

    return render_template("edit.html", classes=classes)


if __name__ == "__main__":
    app.run(
        debug=True,
        port=50004,
    )
