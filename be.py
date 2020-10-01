from flask import Flask, request
import webhook
import quickstart
from db import dbHelper,create

app = Flask(__name__)
# with app.app_context():
#     create(app)
db = dbHelper(app)

@app.route("/goog", methods=["POST"])
def pubsub():
    data = request.json
    print(data)
    d = quickstart.return_details_from_request(data, db)
    webhook.received_stuff(d, status=data["eventType"])
    return "", 200


app.run(debug=False)