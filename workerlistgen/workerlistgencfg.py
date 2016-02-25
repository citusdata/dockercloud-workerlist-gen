import logging
import signal

import helper.init_helper as InitHelper
from docker import Client
from workerlistgen.config import *
from utils import fetch_remote_obj, save_to_file

docker = Client(base_url='unix://tmp/docker.sock')
logger = logging.getLogger("workerlistgen")


def run_workerlistgen(msg=None):
    workerlistgen = WorkerlistGen(msg)
    workerlistgen.update()


class WorkerlistGen(object):
    linked_names = []

    def __init__(self, msg=""):
        logger.info("==========BEGIN==========")
        if msg:
            logger.info(msg)

        self._initialize()

    def _initialize(self):
        if WORKERLISTGEN_CONTAINER_URI and WORKERLISTGEN_SERVICE_URI and API_AUTH:
            workerlistgen_container = fetch_remote_obj(WORKERLISTGEN_CONTAINER_URI)

            workerlistgen_names = InitHelper.get_link_names_from_workerlistgen(workerlistgen_container.linked_to_container)

            logger.info("Link names: %s", ", ".join(workerlistgen_names))

            WorkerlistGen.linked_names = workerlistgen_names
        else:
            raise RuntimeError('Docker Cloud environment variables not set')

    def update(self):
        if WORKERLISTGEN_SERVICE_URI and WORKERLISTGEN_CONTAINER_URI and API_AUTH:
            file_content = '# this file was auto-generated using workerlistgen\n'
            config_lines = InitHelper.get_config_lines(WorkerlistGen.linked_names)
            for config_line in config_lines:
                file_content += config_line
                file_content += '\n'

            save_to_file(CITUS_WORKERLIST_CONFIG_FILE, file_content)

            # find containers on this machine functioning as Citus master
            filters = dict()
            labels = []
            labels.append('com.docker.compose.project=' + CITUS_STACK_NAME)
            labels.append('com.docker.compose.service=' + CITUS_SERVICE_NAME)
            filters['label'] = labels

            citus_masters = docker.containers(filters=filters)

            for citus_master in citus_masters:
                logger.info("Sending container '%s' signal '%d'",
                            citus_master['Id'], signal.SIGHUP)
                docker.kill(citus_master['Id'], signal.SIGHUP)

            logger.info("===========END===========")
        else:
            raise RuntimeError('Docker Cloud environment variables not set')
