import requests


data = {
    "collection": "courses.courseWork",
    "eventType": "MODIFIED",
    "resourceId": {
        "courseId": "104950182954",
        "id": "178153010124",
    },
}


#r=requests.post("http://localhost:5000/goog", json=data)
r=requests.post("http://communication-bot.karmanyaah.malhotra.cc:42169/goog", json=data)
