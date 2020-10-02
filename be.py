from flask import Flask, request
import googleapiclient.errors
import webhook
import quickstart
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
    data = json.loads(b64decode(data["message"]["data"]))
    to = db.find_connection_by_class_id(
        classId=data["resourceId"]["courseId"]
    ).get_webhook_url()

    try:
        d = quickstart.return_details_from_request(data, db)
    except googleapiclient.errors.HttpError:
        webhook.send_raw(to, "Some update but 404 happened check classroom manually")
        return "", 200
    webhook.received_stuff(to, d, status=data["eventType"])
    return "", 200


# TODO: acknowledge annoucnments even if not post them
# TODO: look at announments
# TODO: error handling

app.run(debug=False, port=50005)
