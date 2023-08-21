# (C) Copyright 2021 Hewlett Packard Enterprise Development Company, L.P.

import logging
import os
import sys
import uuid

FORMAT_STRING = (
    "%(asctime)s : " + str(uuid.uuid4()) + " : %(process)d : %(thread)d \
: %(levelname)s : %(filename)s : %(funcName)s : %(lineno)d : %(message)s"
)

debug = os.getenv("DEBUG", True)
if debug:
    LOGGING_LEVEL = logging.DEBUG
else:
    LOGGING_LEVEL = logging.INFO

LOG = logging.getLogger()
LOG.setLevel(LOGGING_LEVEL)


handler = logging.StreamHandler(sys.stdout)
handler.setLevel(LOGGING_LEVEL)

formatter = logging.Formatter(FORMAT_STRING)
formatter.default_msec_format = "%s.%03d"
handler.setFormatter(formatter)
LOG.addHandler(handler)


def get_logger(name="root"):
    return logging.getLogger(name)
