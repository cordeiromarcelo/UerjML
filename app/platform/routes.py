from flask import Blueprint, render_template, request, redirect, url_for
import os
import shutil
import io
import json
import config
import pandas as pd
from app.source import preprocessing

platform = Blueprint('platform', __name__, url_prefix='/')


@platform.route('/')
def index():
    return render_template('platform/index.html')


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
    return redirect(url_for('platform.renderTable', filename=filename))


@platform.route('/<string:filename>/', methods=['GET', 'POST'])
def renderTable(filename):

    # file paths
    file_path = os.path.join(config.UPLOAD_FOLDER, filename)
    file_path_parquet = os.path.join(file_path, filename + '.parquet')
    file_path_history = os.path.join(file_path, 'history.parquet')

    # read history logs
    history = pd.read_parquet(file_path_history)
    error_msg = "Erro: "

    if request.method == 'POST':
        if request.form.get('action') == "apply":
            # get the actual file
            df = pd.read_parquet(file_path_parquet)

            try:
                # Get the selected function and apply
                selected_function = preprocessing.name_funcs_dict[request.values['process']]
                df = selected_function(df, request.form.getlist('col'), request.values['opt'])

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

    else:
        df = pd.read_parquet(file_path_parquet)

    # describe information
    describe = df.describe().reset_index()

    # dtypes information
    dtypes = pd.DataFrame(df.dtypes).reset_index()
    dtypes.columns = ['coluna', 'tipo']

    return render_template("platform/table.html", column_names=df.columns.values,
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
                           help_texts=preprocessing.funcs_helps_dict,
                           error_msg=error_msg,
                           zip=zip, len=len, str=str, list=list)

    # return redirect(url_for('platform.renderTableMap', filename=filename,
    #                         lat_col=request.values['lat'], long_col=request.values['long'],
    #                         peso_col=request.values['peso']))
