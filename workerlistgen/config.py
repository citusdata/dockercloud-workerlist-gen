import os
import re

# envvar

WORKERLISTGEN_CONTAINER_URI = os.getenv("DOCKERCLOUD_CONTAINER_API_URI")
WORKERLISTGEN_SERVICE_URI = os.getenv("DOCKERCLOUD_SERVICE_API_URI")
API_AUTH = os.getenv("DOCKERCLOUD_AUTH")
DEBUG = os.getenv("DEBUG", True)
CITUS_CONFDIR = os.getenv("CITUS_CONFDIR")
CITUS_STACK_NAME = os.getenv("DOCKERCLOUD_STACK_NAME")
CITUS_SERVICE_NAME = os.getenv("CITUS_SERVICE_NAME")

# const
CITUS_WORKERLIST_CONFIG_FILE = CITUS_CONFDIR + "/pg_worker_list.conf"
API_RETRY = 10  # seconds
PID_FILE = "/tmp/dockercloud-workerlistgen.pid"
