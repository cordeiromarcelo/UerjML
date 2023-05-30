import os
import shutil
import typing as t

import pandas as pd
from flask import Blueprint, render_template, request, redirect, url_for, Response
from jinja2 import Environment
from jinja2.utils import htmlsafe_json_dumps
from markupsafe import Markup

from sklearn.model_selection import train_test_split

import config
from app.source import utils
from app.source.preprocessing import preprocessing

platform = Blueprint('platform', __name__, url_prefix='/')


@platform.app_template_filter('new_tojson')
def new_tojson_filter(value: t.Any) -> Markup:
    env = Environment()
    dumps = env.policies["json.dumps_function"]
    kwargs = {'sort_keys': False}
    return htmlsafe_json_dumps(value, dumps=dumps, **kwargs)


@platform.route('/')
def index():

    saved_dfs = os.listdir(config.UPLOAD_FOLDER)
    return render_template('platform/index.html', saved_dfs=saved_dfs)


@platform.route("/", methods=['POST'])
def uploadFiles():
    # get the uploaded file
    uploaded_file = request.files['file']

    if uploaded_file.filename != '':

        filename = uploaded_file.filename.split('.')[0]
        file_path = os.path.join(config.UPLOAD_FOLDER, filename)
        file_path_history = os.path.join(file_path, 'history.parquet')

        if os.path.exists(file_path):
            shutil.rmtree(file_path)

        os.makedirs(file_path)

        file_path_csv = os.path.join(file_path, filename + '.csv')
        uploaded_file.save(file_path_csv)
        df = pd.read_csv(file_path_csv, encoding='unicode_escape')

        file_path_parquet = os.path.join(file_path, filename + '.parquet')
        df.to_parquet(file_path_parquet)

        history = pd.DataFrame()
        history.to_parquet(file_path_history)

    else:
        raise Exception('O arquivo não possui nome')

        # save the file
    return redirect(url_for('platform.renderPreprocessing', filename=filename))


@platform.route('/<string:filename>/', methods=['GET', 'POST'])
def renderPreprocessing(filename):

    # file paths
    file_path = os.path.join(config.UPLOAD_FOLDER, filename)
    file_path_parquet = os.path.join(file_path, filename + '.parquet')
    file_path_history = os.path.join(file_path, 'history.parquet')

    # read history logs
    history = pd.read_parquet(file_path_history)
    error_msg = "Erro: "

    print(preprocessing.func_args_dict)

    if request.method == 'POST':
        if request.form.get('action') == "apply":
            # get the actual file
            df = pd.read_parquet(file_path_parquet)

            try:
                # Get the selected function and apply
                extra_args = utils.fix_args_types(request.form.getlist('args'))
                args = [df, request.form.getlist('col')] + extra_args
                print(args)

                selected_function = preprocessing.name_funcs_dict[request.values['process']]
                df = selected_function(*args)

                # Append applied function to history and save to parquet
                history = history.append(
                    {'Tratamento': selected_function.name,
                     'Coluna': request.form.getlist('col')
                     },
                    ignore_index=True)
                history.to_parquet(file_path_history)

                # Save applied function to history
                history_path_parquet = os.path.join(file_path, f'{filename}_{history.index[-1]}.parquet')

                # Keep track of old DF
                os.rename(file_path_parquet, history_path_parquet)

                # Save processed DF
                df.to_parquet(file_path_parquet)
            except Exception as e:
                error_msg += str(e)

        if request.form.get('action') == "undo":
            try:
                history_path_parquet = os.path.join(file_path, f'{filename}_{history.index[-1]}.parquet')
                history = history[:-1]
                history.to_parquet(file_path_history)

                os.remove(file_path_parquet)
                os.rename(history_path_parquet, file_path_parquet)
            except IndexError:
                error_msg += "Nada para desfazer!"

            df = pd.read_parquet(file_path_parquet)

        if request.form.get('action') == "next":
            return redirect(url_for('platform.renderTrain', filename=filename))

        if request.form.get('action') == "back":
            return redirect(url_for('platform.uploadFiles', filename=filename))

    else:
        df = pd.read_parquet(file_path_parquet)

    # describe information
    describe = df.describe(include='all').reset_index()

    # dtypes information
    dtypes = pd.DataFrame(df.dtypes).reset_index()
    dtypes.columns = ['coluna', 'tipo']

    return render_template("platform/preprocessing.html", column_names=df.columns.values,
                           row_data=list(df.values.tolist())[:1000],
                           describe_columns=describe.columns.values,
                           describe_data=list(describe.values.tolist()),
                           dtypes_columns=dtypes.columns.values,
                           dtypes_data=list(dtypes.values.tolist()),
                           history_columns=history.columns.values,
                           history_data=list(history.values.tolist()),
                           funcs=preprocessing.category_funcs_dict,
                           options=preprocessing.funcs_options_dict,
                           options_descriptions=preprocessing.options_descriptions_dict,
                           funcs_args=preprocessing.func_args_dict,
                           help_texts=preprocessing.funcs_helps_dict,
                           error_msg=error_msg,
                           zip=zip, len=len, str=str, list=list)


# @platform.route('/<string:filename>/model/output')
# def content(run):
#     """
#     Render the content a url different from index
#     """
#     def inner():
#         # simulate a long process to watch
#         for i in range(500):
#             j = math.sqrt(i)
#             time.sleep(1)
#             # this value should be inserted into an HTML template
#             yield str(i) + '<br/>\n'
#     return Response(inner(), mimetype='text/html')


@platform.route('/<string:filename>/model', methods=['GET', 'POST'])
def renderTrain(filename):

    file_path = os.path.join(config.UPLOAD_FOLDER, filename)
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
                print('label:', label)
                print('time:', time)

                df_train, df_test = train_test_split(
                    df, test_size=0.33, random_state=42)

                import sys
                from io import StringIO
                import jinja2
                import logging

                logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

                old_stderr = sys.stderr
                sys.stderr = mystderr = StringIO()
                from autogluon.tabular import TabularPredictor
                predictor = TabularPredictor(label=label).fit(df_train, time_limit=time)  # Fit models for 120s
                sys.stderr = old_stderr
                leaderboard = predictor.leaderboard(df_test)

                print(mystderr.getvalue())
                return jinja2.Template("<div id='console'>my output = {{ console }}</div>").render(
                    console=mystderr.getvalue()
                )

            except Exception as e:
                error_msg += str(e)

        if request.form.get('action') == "back":
            return redirect(url_for('platform.renderPreprocessing', filename=filename))

    return render_template("platform/train.html", column_names=df.columns.values,
                           row_data=list(df.values.tolist())[:1000],
                           describe_columns=describe.columns.values,
                           describe_data=list(describe.values.tolist()),
                           dtypes_columns=dtypes.columns.values,
                           dtypes_data=list(dtypes.values.tolist()),
                           history_columns=history.columns.values,
                           history_data=list(history.values.tolist()),
                           error_msg=error_msg,
                           zip=zip, len=len, str=str, list=list)
