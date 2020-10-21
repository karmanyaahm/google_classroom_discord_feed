from flask import Flask, request
import googleapiclient.errors
import webhook
from classroom import Classroom
from db import dbHelper, create
import json
from base64 import b64decode

app = Flask(__name__)
# with app.app_context():
#     create(app)
db = dbHelper(app)


@app.route("/goog", methods=["POST"])
def pubsub():
    data = request.json
    print(data)
    regid = data["message"]["attributes"]["registrationId"]
    print(data)
    data = json.loads(b64decode(data["message"]["data"]))

    if cons := db.find_connections_by_class_id(classId=data["resourceId"]["courseId"]):
        for con in cons:
            room = Classroom.from_user(con.user,db)
            to = con.get_webhook_url()
            try:
                d = room.get_courseWork(
                    data["resourceId"]["courseId"], data["resourceId"]["id"]
                )
            except googleapiclient.errors.HttpError:
                webhook.send_raw(
                    to, "Some update but error happened check classroom manually"
                )
                return "", 200
            webhook.received_stuff(to, d, status=data["eventType"])
    else:
        room.deregister_id(regid)
    ##allows for possible attack here TODO implement auth with pubsub

    return "", 200


# TODO: look at annoucements
# TODO: error handling

app.run(debug=False, port=50005)
