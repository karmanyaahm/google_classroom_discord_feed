from __future__ import print_function
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import constants


# If modifying these scopes, delete the file token.pickle.
SCOPES = constants.scopes


def get_creds(uid, db):
    creds = db.find_user_by_id(uid).token
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
            db.find_user_by_id(uid).token = creds
            db.commit_modification()
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        # with open("token.pickle", "wb") as token:
        #     pickle.dump(creds, token)
        ## TODO: replace

    return creds


def return_details_from_request(r, db):
    room = Classroom.from_classId(r["resourceId"]["courseId"], db)
    return room.get_courseWork(
        courseId=r["resourceId"]["courseId"], thingId=r["resourceId"]["id"]
    )


class Classroom:
    def __init__(self, service):
        self.service = service

    @classmethod
    def from_uid(clas, uid, db):
        return clas(build("classroom", "v1", credentials=get_creds(uid, db)))

    @classmethod
    def from_classId(clas, courseId, db):
        uid = db.find_connection_by_class_id(courseId).uid
        return clas.from_uid(uid, db)

    def register(self, courseId):
        body = constants.registration_body(courseId)
        o = self.service.registrations().create(body=body).execute()
        return o["registrationId"], o["expiryTime"]

    def deregister(self, con):
        self.service.registrations().delete(registrationId=con.registration).execute()

    def deregister_id(self, id):
        self.service.registrations().delete(registrationId=id).execute()

    def get_courseWork(self, courseId, thingId):
        return (
            self.service.courses()
            .courseWork()
            .get(courseId=courseId, id=thingId)
            .execute()
        )

    def get_courses(self):
        return self.service.courses().list(courseStates='ACTIVE').execute()["courses"]
