import logging
import json

import config
from workerlistgencfg import run_workerlistgen, WorkerlistGen
from utils import get_uuid_from_resource_uri

logger = logging.getLogger("workerlistgen")


def on_cloud_event(message):
    logger.debug(message)
    logger.debug(WorkerlistGen.linked_names)
    try:
        event = json.loads(message)
    except ValueError:
        logger.info("event is not a valid json message")
        return

    # When service scale up/down or container start/stop/terminate/redeploy, reload the service
    if event.get("state", "") not in ["In progress", "Pending", "Terminating", "Starting", "Scaling", "Stopping"] and \
                    event.get("type", "").lower() in ["container", "service"]:
        msg = "Event: %s %s is %s" % (
            event["type"], get_uuid_from_resource_uri(event.get("resource_uri", "")), event["state"].lower())
        run_workerlistgen(msg)

    # Add/remove services linked to workerlistgen
    if event.get("state", "") == "Success" and config.WORKERLISTGEN_SERVICE_URI in event.get("parents", []):
        run_workerlistgen("Event: New action is executed on the WorkerlistGen container")


def on_websocket_open():
    WorkerlistGen.linked_names = []
    run_workerlistgen("Websocket open")


def on_websocket_close():
    logger.info("Websocket close")


def on_user_reload(signum, frame):
    run_workerlistgen("User reload")
