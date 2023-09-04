from ast import literal_eval
import pickle
import os
from datetime import datetime

import app.config as config

import logging
from autogluon.common.utils import log_utils

def simplest_type(s):
    try:
        return literal_eval(s)
    except:
        return s


def fix_args_types(args_list):
    return [simplest_type(arg) for arg in args_list]


def manage_context(filename, g):
    g.filename = filename

    last_modified = datetime.now()

    log_path = os.path.join(config.UPLOAD_FOLDER, filename, 'logs')
    with open(os.path.join(log_path, 'last_modified'), 'wb') as f:
        pickle.dump(last_modified, f)
    f.close()

def get_status(filename, status_name):
    log_path = os.path.join(config.UPLOAD_FOLDER, filename, 'logs')
    with open(os.path.join(log_path, 'status'), 'rb') as f:
        status = pickle.load(f)
    f.close()

    return status.get(status_name)

def update_status(filename, update_dict):

    log_path = os.path.join(config.UPLOAD_FOLDER, filename, 'logs')

    with open(os.path.join(log_path, 'status'), 'rb') as f:
        status = pickle.load(f)
    f.close()

    status.update(update_dict)

    with open(os.path.join(log_path, 'status'), 'wb') as f:
        pickle.dump(status, f)
    f.close()

def logging_init(log_path):
    formatter = logging.Formatter(
        "{asctime}.{msecs:03.0f} {levelname:8} {message}",
        datefmt="%H:%M:%S",
        style="{",
    )

    file_handler = logging.FileHandler(log_path)
    file_handler.setFormatter(formatter)

    root_logger = logging.getLogger()
    root_logger.addHandler(file_handler)
    root_logger.setLevel(logging.INFO)
    log_utils._logger_ag.propagate = True

    return root_logger