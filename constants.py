import secret


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
