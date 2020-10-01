import requests

import json

data = {
    "collection": "courses.courseWork",
    "eventType": "MODIFIED",
    "resourceId": {
        "courseId": "104950182954",
        "id": "178153010124",
    },
}

data = """{"message":{"attributes":{"registrationId":"3338188336727588864"},"data":"eyJjb2xsZWN0aW9uIjoiY291cnNlcy5jb3Vyc2VXb3JrIiwiZXZlbnRUeXBlIjoiTU9ESUZJRUQiLCJyZXNvdXJjZUlkIjp7ImNvdXJzZUlkIjoiMTA0OTUwMTgyOTU0IiwiaWQiOiIxNzY4MzI0NDU2NTEifX0=","messageId":"1592321181222643","message_id":"1592321181222643","publishTime":"2020-10-01T23:52:28.407Z","publish_time":"2020-10-01T23:52:28.407Z"},"subscription":"projects/csclub-281101/subscriptions/topersonalserver"}"""
data = json.loads(data)
r = requests.post(
    "http://localhost:50005/goog",
    json=data,
)

# r=requests.post("https://communication-bot.karmanyaah.malhotra.cc:42169/goog", json=data)
