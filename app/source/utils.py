from ast import literal_eval
import pickle
import os
from datetime import datetime

import app.config as config

def simplest_type(s):
    try:
        return literal_eval(s)
    except:
        return s


def fix_args_types(args_list):
    return [simplest_type(arg) for arg in args_list]


def manage_context(filename, g):

    last_modified = datetime.now()

    log_path = os.path.join(config.UPLOAD_FOLDER, filename, 'logs')
    with open(os.path.join(log_path, 'last_modified'), 'wb') as f:
        pickle.dump(last_modified, f)
    f.close()

    g.filename = filename


def update_status(filename, update_dict):

    log_path = os.path.join(config.UPLOAD_FOLDER, filename, 'logs')

    with open(os.path.join(log_path, 'status'), 'rb') as f:
        status = pickle.load(f)
    f.close()

    status.update(update_dict)

    with open(os.path.join(log_path, 'status'), 'wb') as f:
        pickle.dump(status, f)
    f.close()