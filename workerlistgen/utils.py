import logging
import time

import dockercloud

from config import API_RETRY

logger = logging.getLogger("workerlistgen")


def fetch_remote_obj(uri):
    if not uri:
        return None

    while True:
        try:
            obj = dockercloud.Utils.fetch_by_resource_uri(uri)
            return obj
        except Exception as e:
            logger.error(e)
            time.sleep(API_RETRY)


def get_uuid_from_resource_uri(uri):
    terms = uri.strip("/").split("/")
    if len(terms) < 2:
        return ""
    return terms[-1]


def save_to_file(name, content):
    try:
        with open(name, 'w') as f:
            f.write(content)
            return True
    except Exception as e:
        logger.error("Cannot write to file(%s): %s" % (name, e))
        return False
