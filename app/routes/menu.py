import os
import pickle

from datetime import datetime
import humanize

from flask import Blueprint, render_template, g

import app.config as config

menu_bp = Blueprint('menu', __name__, url_prefix='/')

os.makedirs(config.UPLOAD_FOLDER, exist_ok=True)
saved_dfs = os.listdir(config.UPLOAD_FOLDER)

@menu_bp.route('/')
def menu():

    g.filename = ''

    dict_list = []
    for filename in saved_dfs:
        log_path = os.path.join(config.UPLOAD_FOLDER, filename, 'logs')
        with open(os.path.join(log_path, 'status'), 'rb') as f:
            status = pickle.load(f)
        f.close()

        with open(os.path.join(log_path, 'last_modified'), 'rb') as f:
            status.update({'last_updated': pickle.load(f).replace(microsecond=0)})
        f.close()

        timedelta = datetime.now() - status.get('last_updated')
        _t = humanize.i18n.activate("pt_BR")
        status['natural_timedelta'] = humanize.naturaltime(timedelta)

        dict_list.append(status)

    dict_list = sorted(dict_list, key=lambda d: d['last_updated'], reverse=True)

    print(dict_list)

    return render_template('platform/menu.html',
                           saved_dfs=saved_dfs,
                           dict_list=dict_list[0:5])


@menu_bp.route('/open')
def open_project():

    g.filename = ''

    dict_list = []
    for filename in saved_dfs:
        log_path = os.path.join(config.UPLOAD_FOLDER, filename, 'logs')
        with open(os.path.join(log_path, 'status'), 'rb') as f:
            status = pickle.load(f)
        f.close()

        with open(os.path.join(log_path, 'last_modified'), 'rb') as f:
            status.update({'last_updated': pickle.load(f).replace(microsecond=0)})
        f.close()

        timedelta = datetime.now() - status.get('last_updated')
        _t = humanize.i18n.activate("pt_BR")
        status['natural_timedelta'] = humanize.naturaltime(timedelta)

        dict_list.append(status)

    print(dict_list)

    return render_template('platform/open.html',
                           saved_dfs=saved_dfs,
                           dict_list=dict_list)