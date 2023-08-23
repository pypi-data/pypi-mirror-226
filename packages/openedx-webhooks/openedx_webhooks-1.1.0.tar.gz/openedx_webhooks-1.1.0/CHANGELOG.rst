Change Log
##########

Version 1.1.0 (2023-08-22)
**********************************************

* Add grade changes signals
    * `COURSE_GRADE_CHANGED <https://github.com/openedx/edx-platform/blob/1d618055dc5a44b94a1da63ef4017a2015aad018/lms/djangoapps/grades/course_grade_factory.py#L201>`_
    * `COURSE_GRADE_NOW_PASSED <https://github.com/openedx/edx-platform/blob/1d618055dc5a44b94a1da63ef4017a2015aad018/lms/djangoapps/grades/course_grade_factory.py#L209C17-L209C40>`_
    * `COURSE_GRADE_NOW_FAILED <https://github.com/openedx/edx-platform/blob/1d618055dc5a44b94a1da63ef4017a2015aad018/lms/djangoapps/grades/course_grade_factory.py#L215C17-L215C40>`_


Version 1.0.1 (2023-08-15)
**********************************************

* Fix: remove non implemented filters

Version 1.0.0 (2023-08-15)
**********************************************

* Added webfilters:
    * CertificateCreationRequested,
    * CertificateRenderStarted,
    * CohortAssignmentRequested,
    * CohortChangeRequested,
    * CourseAboutRenderStarted,
    * CourseEnrollmentStarted,
    * CourseUnenrollmentStarted,
    * DashboardRenderStarted,
    * StudentLoginRequested,
    * StudentRegistrationRequested,

* Available webhooks:
    * SESSION_LOGIN_COMPLETED
    * STUDENT_REGISTRATION_COMPLETED
    * COURSE_ENROLLMENT_CREATED
    * COURSE_ENROLLMENT_CHANGED
    * COURSE_UNENROLLMENT_COMPLETED
    * CERTIFICATE_CREATED
    * CERTIFICATE_CHANGED
    * CERTIFICATE_REVOKED
    * COHORT_MEMBERSHIP_CHANGED
    * COURSE_DISCUSSIONS_CHANGED


Version 0.2.1 (2023-06-06)
**********************************************

* Renamed package to openedx_webhooks. Upload to PyPI.

Version 0.1.1 (2023-06-05)
**********************************************

* Improve documentation

0.1.0 – 2023-05-31
**********************************************

Added
=====

* First release on PyPI.
