from classroom import Classroom
from db import dbHelper
from flask import Flask
from datetime import datetime, timedelta
from sys import argv
from constants import parsetime

try:
    hrs_ahead = int(argv[1])
except IndexError:
    hrs_ahead = 6

hrs_behind = 2


app = Flask(__name__)
# with app.app_context():
#     create(app)
db = dbHelper(app)

now = datetime.utcnow()
time1 = now + timedelta(hours=hrs_ahead)
# time2 = now - timedelta(hours=hrs_behind)


with app.app_context():
    ls = db.find_connection_by_expire(end=time1)  # start=time2)

    for connection in ls:
        room = Classroom.from_uid(connection.uid, db)
        regId, expTime = room.register(courseId=connection.classId)
        connection.registration = regId
        connection.expire = parsetime(expTime)
        print(regId)

    db.commit_modification()