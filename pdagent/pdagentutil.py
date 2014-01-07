#
# Python utility module for sending events to PagerDuty Integration API.
#
# Copyright (c) 2013, PagerDuty, Inc. <info@pagerduty.com>
# All rights reserved.
#
# Uses the PagerDuty Integration API:
# http://developer.pagerduty.com/documentation/integration/events
#

import json

from pdqueue import PDQueue
from filelock import FileLock


def find_in_sys_path(file_path):
    import os
    import sys
    for directory in sys.path:
        abs_path = os.path.join(directory, file_path)
        if os.access(abs_path, os.R_OK):
            return abs_path
    return None


def queue_event(
        queue_config,
        event_type, service_key, incident_key, description, details
        ):

    event = _build_event_json_str(
        event_type, service_key, incident_key, description, details
        )
    PDQueue(
        queue_config=queue_config,
        lock_class=FileLock
    ).enqueue(service_key, event)


def resurrect_events(queue_config, service_key):
    from pdqueue import PDQueue

    PDQueue(
        queue_config=queue_config,
        lock_class=FileLock
    ).resurrect(service_key)


def get_status(queue_config, service_key):
    from pdqueue import PDQueue

    return PDQueue(
        queue_config=queue_config,
        lock_class=FileLock
    ).get_status(service_key)


def _build_event_json_str(
    event_type, service_key, incident_key, description, details
    ):
    d = {
        "service_key": service_key,
        "event_type": event_type,
        "details": details,
    }
    if incident_key is not None:
        d["incident_key"] = incident_key
    if description is not None:
        d["description"] = description

    return json.dumps(d)
