import logging
import os
import signal
import sys

import dockercloud

from config import DEBUG, PID_FILE, WORKERLISTGEN_SERVICE_URI, WORKERLISTGEN_CONTAINER_URI, API_AUTH
from eventhandler import on_cloud_event, on_websocket_open, on_user_reload, on_websocket_close
from workerlistgen import __version__
from workerlistgencfg import run_workerlistgen
from utils import save_to_file

dockercloud.user_agent = "dockercloud-workerlistgen/%s" % __version__

logger = logging.getLogger("workerlistgen")


def create_pid_file():
    pid = str(os.getpid())
    save_to_file(PID_FILE, pid)
    return pid


def set_autoreload(workerlistgen_container_uri, workerlistgen_service_uri, api_auth):
    autoreload = False
    if workerlistgen_container_uri and workerlistgen_service_uri:
        if api_auth:
            msg = "dockercloud/workerlistgen %s has access to the cloud API - will reload list of backends" \
                  " in real-time" % __version__
            autoreload = True
        else:
            msg = "dockercloud/workerlistgen %s doesn't have access to the cloud API - you might want to" \
                  " give an API role to this service for automatic backend reconfiguration" % __version__
    else:
        msg = "dockercloud/workerlistgen %s is not running in Docker Cloud" % __version__

    if autoreload:
        logger.info(msg)
    else:
        raise RuntimeError(msg)

    return autoreload


def listen_remote_events():
    events = dockercloud.Events()
    events.on_open(on_websocket_open)
    events.on_close(on_websocket_close)
    events.on_message(on_cloud_event)
    events.run_forever()


def main():
    logging.basicConfig(stream=sys.stdout)
    logging.getLogger("workerlistgen").setLevel(logging.DEBUG if DEBUG else logging.INFO)

    signal.signal(signal.SIGUSR1, on_user_reload)
    signal.signal(signal.SIGTERM, sys.exit)

    autoreload = set_autoreload(WORKERLISTGEN_CONTAINER_URI, WORKERLISTGEN_SERVICE_URI, API_AUTH)

    pid = create_pid_file()
    logger.info("workerlistgen PID: %s" % pid)

    if autoreload:
        listen_remote_events()
    else:
        raise RuntimeError('Must run in autoreload mode')


if __name__ == "__main__":
    main()
