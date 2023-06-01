import os

import pandas as pd
from flask import Blueprint, render_template, request, redirect, url_for, Response, g

from autogluon.tabular import TabularPredictor
from autogluon.common.utils import log_utils
import logging

from sklearn.model_selection import train_test_split

import app.config as config

train_bp = Blueprint('train', __name__, url_prefix='/train')


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


@train_bp.route('/<string:filename>/train_log')
def content(filename):
    """
    Render the content an url different from index
    """
    def inner():
        with open(os.path.join(config.UPLOAD_FOLDER, filename, "logs", "file"), "r") as file:
            # this value should be inserted into an HTML template
            yield '<br>'.join(file.readlines())

    return Response(inner(), mimetype='text/html')


@train_bp.route('/<string:filename>/', methods=['GET', 'POST'])
def renderTrain(filename):
    g.filename = filename
    file_root = os.path.join(config.UPLOAD_FOLDER, filename)
    file_path = os.path.join(file_root, 'versions')
    file_path_parquet = os.path.join(file_path, filename + '.parquet')
    file_path_history = os.path.join(file_path, 'history.parquet')
    model_path = os.path.join(file_root, 'AutoGluon')

    # read history logs
    history = pd.read_parquet(file_path_history)
    error_msg = "Erro: "

    df = pd.read_parquet(file_path_parquet)

    # describe information
    describe = df.describe(include='all').reset_index()

    # dtypes information
    dtypes = pd.DataFrame(df.dtypes).reset_index()
    dtypes.columns = ['coluna', 'tipo']

    if request.method == 'POST':
        if request.form.get('action') == "apply":
            try:
                # Get the selected function and apply
                label = request.values['col']
                time = int(request.values['process'])

                df_train, df_test = train_test_split(
                    df, test_size=0.33, random_state=42)

                df_train.to_parquet(os.path.join(file_root, 'interim', 'train.parquet'))
                df_test.to_parquet(os.path.join(file_root, 'interim', 'test.parquet'))

                log_path = os.path.join(config.UPLOAD_FOLDER, filename, "logs", "file")
                if os.path.exists(log_path):
                    os.remove(log_path)

                root_logger = logging_init(log_path)
                predictor = TabularPredictor(label=label, path=model_path).fit(df_train, time_limit=time)

                print("Calculating Feature Importance")
                fs_path = os.path.join(model_path, 'feature_importance')

                if not os.path.exists(fs_path):
                    os.makedirs(fs_path)

                feature_importance = predictor.feature_importance(df_test)
                feature_importance.reset_index().to_parquet(os.path.join(fs_path, 'fs.parquet'))

                root_logger.setLevel(0)

                return redirect(url_for('evaluate.renderEvaluate', filename=filename))

            except Exception as e:
                error_msg += str(e)

        if request.form.get('action') == "back":
            return redirect(url_for('preprocess.renderPreprocessing', filename=filename))

    # noinspection PyTypeChecker
    return render_template("platform/train.html", column_names=df.columns.values,
                           row_data=list(df.values.tolist())[:1000],
                           describe_columns=describe.columns.values,
                           describe_data=list(describe.values.tolist()),
                           dtypes_columns=dtypes.columns.values,
                           dtypes_data=list(dtypes.values.tolist()),
                           history_columns=history.columns.values,
                           history_data=list(history.values.tolist()),
                           error_msg=error_msg,
                           filename=filename,
                           zip=zip, len=len, str=str, list=list)