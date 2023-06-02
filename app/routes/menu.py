import os
import pickle

import pandas as pd
from flask import Blueprint, render_template, request, redirect, url_for, g

import app.config as config

menu_bp = Blueprint('main', __name__, url_prefix='/')


@menu_bp.route('/')
def menu():

    g.filename = ''

    saved_dfs = os.listdir(config.UPLOAD_FOLDER)
    dict_list = []
    for filename in saved_dfs:
        log_path = os.path.join(config.UPLOAD_FOLDER, filename, 'logs')
        with open(os.path.join(log_path, 'status'), 'rb') as f:
            status = pickle.load(f)
        f.close()

        with open(os.path.join(log_path, 'last_modified'), 'rb') as f:
            status.update({'last_updated': pickle.load(f).replace(microsecond=0)})
        f.close()

        translate_map = {'name': 'Nome',
                         'preprocessing': 'Preprocessamentos',
                         'train': 'Treino',
                         'best_model': 'Melhor Modelo',
                         'train_metric': 'Métrica de Treino',
                         'train_score': 'Score de Treino',
                         'last_updated': 'Aberto em',
                         }
        for old, new in translate_map.items():
            status[new] = status.pop(old)

        dict_list.append(status)

    print(dict_list)

    return render_template('platform/menu.html',
                           saved_dfs=saved_dfs,
                           dict_list=dict_list)