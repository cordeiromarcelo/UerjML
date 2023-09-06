import os
import shutil
import pickle

import pandas as pd
from flask import Blueprint, render_template, request, redirect, url_for, g

import app.config as config

upload_bp = Blueprint('upload', __name__, url_prefix='/upload')

@upload_bp.route('/')
def index():
    g.filename = ''
    saved_dfs = os.listdir(config.UPLOAD_FOLDER)
    return render_template('platform/upload.html', saved_dfs=saved_dfs)


@upload_bp.route("/", methods=['POST'])
def uploadFiles():
    # get the uploaded file
    uploaded_file = request.files['file']

    if uploaded_file.filename != '':

        filename = uploaded_file.filename.split('.')[0]
        root_path = os.path.join(config.UPLOAD_FOLDER, filename)
        file_path = os.path.join(root_path, 'versions')
        log_path = os.path.join(root_path, 'logs')
        file_path_history = os.path.join(file_path, 'history.parquet')

        if os.path.exists(root_path):
            shutil.rmtree(root_path)

        os.makedirs(root_path)
        for folder_name in ['versions', 'logs', 'raw', 'interim', 'predictions']:
            os.makedirs(os.path.join(root_path, folder_name))

        file_path_csv = os.path.join(root_path, 'raw', filename + '.csv')
        uploaded_file.save(file_path_csv)
        df = pd.read_csv(file_path_csv, encoding='unicode_escape')

        file_path_parquet = os.path.join(file_path, filename + '.parquet')
        df.to_parquet(file_path_parquet)

        history = pd.DataFrame()
        history.to_parquet(file_path_history)

        status = {'name': filename,
                  'original_columns': df.columns,
                  'preprocessing': 0,
                  'train': False,
                  'split': False,
                  'best_model': False,
                  'train_metric': False,
                  'train_score': False}

        with open(os.path.join(log_path, 'status'), 'wb') as f:
            pickle.dump(status, f)
        f.close()

    else:
        raise Exception('O arquivo não possui nome')

        # save the file
    return redirect(url_for('preprocess.renderPreprocessing', filename=filename))