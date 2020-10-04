import secret
import re
import datetime


scopes = [
    "https://www.googleapis.com/auth/classroom.push-notifications",
    "https://www.googleapis.com/auth/classroom.coursework.students.readonly",  # for classes you teach
    "https://www.googleapis.com/auth/classroom.coursework.me.readonly",  ## for classes you don't teach
    "https://www.googleapis.com/auth/classroom.announcements.readonly",
    "https://www.googleapis.com/auth/classroom.courses.readonly",
    "https://www.googleapis.com/auth/classroom.courseworkmaterials.readonly",
    "https://www.googleapis.com/auth/classroom.topics.readonly",
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


class WrongUrlEnteredException(Exception):
    pass


ree = re.compile(r, re.IGNORECASE)


def clean_webhook_url(url):
    try:
        return ree.match(url.strip()).group(1, 2)
    except IndexError:
        raise WrongUrlEnteredException