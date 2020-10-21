from __future__ import print_function
from googleapiclient.discovery import build
import googleapiclient.errors as gexcept
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import constants
import errors


# If modifying these scopes, delete the file token.pickle.
SCOPES = constants.scopes


def get_creds(uid, db):
    creds = db.find_user_by_id(uid).token
    # If there are no (valid) credentials available, let the user log in.
    if not creds.valid:
        if creds.refresh_token:
            creds.refresh(Request())
            db.find_user_by_id(uid).token = creds
            db.commit_modification()
        else:
            raise errors.LoginErrorold
    return creds


def creds_from_user(user, db):
    creds = user.token

    if not creds.valid:
        if creds.refresh_token:
            creds.refresh(Request())
            user.token = creds
            db.commit_modification()
        else:
            raise errors.CannotRefreshToken
    return creds


class Classroom:
    def __init__(self, service):
        self.service = service

    @classmethod
    def from_uid(clas, uid, db):
        return clas(build("classroom", "v1", credentials=get_creds(uid, db)))

    @classmethod
    def from_user(clas, user):
        return clas(build("classroom", "v1", credentials=creds_from_user(user, db)))

    def register(self, courseId):
        body = constants.registration_body(courseId)
        try:
            o = self.service.registrations().create(body=body).execute()
        except gexcept.HttpError as e:
            if int(e.resp["status"]) == 403:
                raise errors.ClassStudentException from e
            else:
                raise
        print(o)
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
        return self.service.courses().list(courseStates="ACTIVE").execute()["courses"]
