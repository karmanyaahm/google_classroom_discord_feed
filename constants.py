import secret
import re
import datetime
from errors import WrongUrlEnteredException

scopes = [
    "https://www.googleapis.com/auth/classroom.push-notifications",
    "https://www.googleapis.com/auth/classroom.student-submissions.students.readonly",  # "https://www.googleapis.com/auth/classroom.coursework.students.readonly",
    "https://www.googleapis.com/auth/classroom.announcements.readonly",
    "https://www.googleapis.com/auth/classroom.courses.readonly",
    "https://www.googleapis.com/auth/classroom.courseworkmaterials.readonly",
    "openid",
]


def registration_body(courseId: str):
    return {  # An instruction to Classroom to send notifications from the `feed` to the
        # provided destination.
        "feed": {
            "feedType": "COURSE_WORK_CHANGES",  # The type of feed.
            "courseWorkChangesInfo": {  # Information about a `Feed` with a `feed_type` of `COURSE_WORK_CHANGES`. # Information about a `Feed` with a `feed_type` of `COURSE_WORK_CHANGES`.
                # This field must be specified if `feed_type` is `COURSE_WORK_CHANGES`.
                "courseId": courseId,  # The `course_id` of the course to subscribe to work changes for.
            },
        },
        "cloudPubsubTopic": {
            "topicName": secret.pubSubTopicName,  # The `name` field of a Cloud Pub/Sub
        },
    }


def parsetime(time):
    return datetime.datetime.strptime(time[:-5], "%Y-%m-%dT%H:%M:%S")


r = "https://discordapp.com/api/webhooks/(.*?)/(.*)"


ree = re.compile(r, re.IGNORECASE)


def clean_webhook_url(url):
    if url == "" or not url:
        raise WrongUrlEnteredException
    try:
        return ree.match(url.strip()).group(1, 2)
    except (IndexError, AttributeError):
        raise WrongUrlEnteredException