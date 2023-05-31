import os

import pandas as pd
from flask import Blueprint, render_template, request, redirect, url_for, Response

from contextlib import redirect_stderr

from sklearn.model_selection import train_test_split

import app.config as config

train_bp = Blueprint('train', __name__, url_prefix='/')


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


@train_bp.route('/<string:filename>/model', methods=['GET', 'POST'])
def renderTrain(filename):
    file_root = os.path.join(config.UPLOAD_FOLDER, filename)
    file_path = os.path.join(file_root, 'versions')
    file_path_parquet = os.path.join(file_path, filename + '.parquet')
    file_path_history = os.path.join(file_path, 'history.parquet')

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

                with open(os.path.join(config.UPLOAD_FOLDER, filename, "logs", "file"), 'w') as f:
                    with redirect_stderr(f):
                        from autogluon.tabular import TabularPredictor
                        predictor = TabularPredictor(label=label, path=os.path.join(file_root, 'AutoGluon')).fit(df_train, time_limit=time)  # Fit models for 120s
                leaderboard = predictor.leaderboard(df_test)

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