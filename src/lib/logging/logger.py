#!/usr/bin/env python

import logging,logging.handlers,os

def log(level,message):
    handler = logging.handlers.WatchedFileHandler(
        os.environ.get("LOGFILE", "/var/log/messages"))
    formatter = logging.Formatter(logging.BASIC_FORMAT)
    handler.setFormatter(formatter)

    root = logging.getLogger()
    root.setLevel(os.environ.get("LOGLEVEL", "INFO"))
    root.addHandler(handler)
    logging.exception("(" + str(level) + ") " + "ImageCapture - " + message)
    print("  => (" + str(level) + ") " + "ImageCapture - " + str(message))
    return
