from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import webhook

# If modifying these scopes, delete the file token.pickle.
SCOPES = [
    "https://www.googleapis.com/auth/classroom.push-notifications",
    "https://www.googleapis.com/auth/classroom.coursework.students.readonly",
    #    "https://www.googleapis.com/auth/classroom.announcements.readonly",
    "https://www.googleapis.com/auth/classroom.courses.readonly",
]


def get_creds(uid, db):
    creds = db.find_user_by_id(uid).token
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("token.pickle", "wb") as token:
            pickle.dump(creds, token)

    return creds


def get_service_raw(creds):
    return build("classroom", "v1", credentials=creds)


def get_service_from_request(r, db):
    con = db.find_connection_by_class_id(r["resourceId"]["courseId"])
    service = get_service_raw(get_creds(con.uid, db))
    return service


def return_details_from_request(r, db):
    service = get_service_from_request(r, db)
    o = (
        service.courses()
        .courseWork()
        .get(courseId=r["resourceId"]["courseId"], id=r["resourceId"]["id"])
        .execute()
    )
    return o


# a = {
#     "feed": {
#         "feedType": "COURSE_WORK_CHANGES",  # The type of feed.
#         "courseWorkChangesInfo": {  # Information about a `Feed` with a `feed_type` of `COURSE_WORK_CHANGES`. # Information about a `Feed` with a `feed_type` of `COURSE_WORK_CHANGES`.
#             "courseId": csclub_courseid,
#         },
#     },
#     "cloudPubsubTopic": {  # A reference to a Cloud Pub/Sub topic. # The Cloud Pub/Sub topic that notifications are to be sent to.
#         #
#         # To register for notifications, the owner of the topic must grant
#         # `classroom-notifications@system.gserviceaccount.com` the
#         #  `projects.topics.publish` permission.
#         "topicName": "projects/csclub-281101/topics/classroomdiscord",  # The `name` field of a Cloud Pub/Sub
#         # [Topic](https://cloud.google.com/pubsub/docs/reference/rest/v1/projects.topics#Topic).
#     },
# }


# o = service.registrations().create(body=a).execute()

# webhook.received_stuff(o, status="tmp")
# open("out.txt", "a").write("\n" + str(o) + "\n")
