"""
Open edX signal events handler functions.
"""
import logging
from datetime import datetime

from attrs import asdict
from django.dispatch import receiver
# pylint: disable=import-error
from openedx.core.djangoapps.signals.signals import (
    COURSE_GRADE_CHANGED,
    COURSE_GRADE_NOW_FAILED,
    COURSE_GRADE_NOW_PASSED,
)

from .models import Webhook
from .utils import fix_dict_keys, send, serialize_course_key

logger = logging.getLogger(__name__)


def _process_event(event_name, data_type, data, **kwargs):
    """
    Process all events with user data.
    """
    logger.debug(f"Processing event: {event_name}")
    webhooks = Webhook.objects.filter(enabled=True, event=event_name)

    for webhook in webhooks:
        logger.info(f"{event_name} webhook triggered to {webhook.webhook_url}")

        if isinstance(data, dict):
            # Process events not coming from openedx_events
            payload = {
                data_type: data,
                'event_metadata': kwargs.get("metadata"),
            }
        else:
            # Process events coming from openedx_events
            payload = {
                data_type: asdict(data, value_serializer=serialize_course_key),
                'event_metadata': asdict(kwargs.get("metadata")),
            }

        send(webhook.webhook_url, payload, www_form_urlencoded=False)


def session_login_completed_receiver(user, **kwargs):
    """
    Handle SESSION_LOGIN_COMPLETED signal.

    Example of data sent:
        user_id:    	                4
        user_is_active:	                True
        user_pii_username:	            andres
        user_pii_email:	                andres@aulasneo.com
        user_pii_name:	                (empty)
        event_metadata_id:	            457f0c26-a1a5-11ed-afe6-0242ac140007
        event_metadata_event_type:	    org.openedx.learning.auth.session.login.completed.v1
        event_metadata_minorversion:	0
        event_metadata_source:	        openedx/lms/web
        event_metadata_sourcehost:	    8616aa50f067
        event_metadata_time:	        2023-01-31 20:24:32.598387
        event_metadata_sourcelib:   	(0, 8, 1)
    """
    _process_event("SESSION_LOGIN_COMPLETED", 'user', user, **kwargs)


def student_registration_completed_receiver(user, **kwargs):
    """
    Handle STUDENT_REGISTRATION_COMPLETED signal.
    """
    _process_event("STUDENT_REGISTRATION_COMPLETED", 'user', user, **kwargs)


def course_enrollment_created_receiver(enrollment, **kwargs):
    """
    Handle COURSE_ENROLLMENT_CREATED signal.

    Example of data sent:
        enrollment_user_id:	            4
        enrollment_user_is_active:	    True
        enrollment_user_pii_username:	andres
        enrollment_user_pii_email:	    andres@aulasneo.com
        enrollment_user_pii_name:	    (empty)
        enrollment_course_course_key:	course-v1:edX+DemoX+Demo_Course
        enrollment_course_display_name:	Demonstration Course
        enrollment_course_start:	    None
        enrollment_course_end;	        None
        enrollment_mode:	            honor
        enrollment_is_active:	        True
        enrollment_creation_date:	    2023-01-31 20:28:10.976084+00:00
        enrollment_created_by:	        None
        event_metadata_id:	            c8bee32c-a1a5-11ed-baf0-0242ac140007
        event_metadata_event_type:	    org.openedx.learning.course.enrollment.created.v1
        event_metadata_minorversio:	    0
        event_metadata_source:	        openedx/lms/web
        event_metadata_sourcehost:	    8616aa50f067
        event_metadata_time:	        2023-01-31 20:28:12.798285
        event_metadata_sourcelib:	    (0, 8, 1)
    """
    _process_event("COURSE_ENROLLMENT_CREATED", 'enrollment', enrollment, **kwargs)


def course_enrollment_changed_receiver(enrollment, **kwargs):
    """
    Handle COURSE_ENROLLMENT_CHANGED signal.
    """
    _process_event("COURSE_ENROLLMENT_CHANGED", 'enrollment', enrollment, **kwargs)


def course_unenrollment_completed_receiver(enrollment, **kwargs):
    """
    Handle COURSE_UNENROLLMENT_COMPLETED signal.
    """
    _process_event("COURSE_UNENROLLMENT_COMPLETED", 'enrollment', enrollment, **kwargs)


def certificate_created_receiver(certificate, **kwargs):
    """
    Handle CERTIFICATE_CREATED signal.
    """
    _process_event("CERTIFICATE_CREATED", 'certificate', certificate, **kwargs)


def certificate_changed_receiver(certificate, **kwargs):
    """
    Handle CERTIFICATE_CHANGED signal.
    """
    _process_event("CERTIFICATE_CHANGED", 'certificate', certificate, **kwargs)


def certificate_revoked_receiver(certificate, **kwargs):
    """
    Handle CERTIFICATE_REVOKED signal.
    """
    _process_event("CERTIFICATE_REVOKED", 'certificate', certificate, **kwargs)


def cohort_membership_changed_receiver(cohort, **kwargs):
    """
    Handle COHORT_MEMBERSHIP_CHANGED signal.
    """
    _process_event("COHORT_MEMBERSHIP_CHANGED", 'cohort', cohort, **kwargs)


def course_discussions_changed_receiver(configuration, **kwargs):
    """
    Handle COURSE_DISCUSSIONS_CHANGED signal.
    """
    _process_event("COURSE_DISCUSSIONS_CHANGED", 'configuration', configuration, **kwargs)
#
#
# def persistent_grade_summary_receiver(certificate, **kwargs):
#     """
#     Handle PERSISTENT_GRADE_SUMMARY_CHANGED signal.
#     """
#     _process_event("PERSISTENT_GRADE_SUMMARY_CHANGED", 'certificate', certificate, **kwargs)

# Events not part of openedx_events, but based on django signals


@receiver(COURSE_GRADE_CHANGED)
def course_grade_changed_receiver(sender, user, course_grade, course_key, deadline, **kwargs):
    """
    Handle COURSE_GRADE_CHANGED signal.
    """
    data = {
        "sender": sender,
        "user": fix_dict_keys(vars(user)),
        "course_grade": fix_dict_keys(vars(course_grade)),
        "course_key": fix_dict_keys(vars(course_key)),
        "deadline": deadline,
    }

    metadata = {
        "event_metadata_event_type": "openedx.core.djangoapps.signals.signals.COURSE_GRADE_CHANGED",
        "event_metadata_time": datetime.isoformat(datetime.now()),
    }

    _process_event("COURSE_GRADE_CHANGED", "course_grade_change",
                   data=data, metadata=metadata)


@receiver(COURSE_GRADE_NOW_PASSED)
def course_grade_now_passed(sender, user, course_id, **kwargs):
    """
    Handle COURSE_GRADE_NOW_PASSED signal.
    """
    data = {
        "sender": fix_dict_keys(vars(sender)),
        "user": fix_dict_keys(vars(user)),
        "course_id": course_id,
    }

    metadata = {
        "event_metadata_event_type": "openedx.core.djangoapps.signals.signals.COURSE_GRADE_NOW_PASSED",
        "event_metadata_time": datetime.isoformat(datetime.now()),
    }

    _process_event("COURSE_GRADE_NOW_PASSED", "course_grade_now_passed",
                   data=data, metadata=metadata)


@receiver(COURSE_GRADE_NOW_FAILED)
def course_grade_now_failed(sender, user, course_id, grade, **kwargs):
    """
    Handle COURSE_GRADE_NOW_FAILED signal.
    """
    data = {
        "sender": fix_dict_keys(vars(sender)),
        "user": fix_dict_keys(vars(user)),
        "course_id": course_id,
        "grade": fix_dict_keys(vars(grade)),
    }

    metadata = {
        "event_metadata_event_type": "openedx.core.djangoapps.signals.signals.COURSE_GRADE_NOW_FAILED",
        "event_metadata_time": datetime.isoformat(datetime.now()),
    }

    _process_event("COURSE_GRADE_NOW_FAILED", "course_grade_now_failed",
                   data=data, metadata=metadata)
