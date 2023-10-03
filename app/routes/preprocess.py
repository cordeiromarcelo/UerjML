import os

import pandas as pd
from flask import Blueprint, render_template, request, redirect, url_for, g

import app.config as config
from app.source import utils
from app.source.preprocessing import preprocessing

from app.source.utils import manage_context, update_status

preprocess_bp = Blueprint('preprocess', __name__, url_prefix='/preprocess')


@preprocess_bp.route('/<string:filename>/', methods=['GET', 'POST'])
def renderPreprocessing(filename):
    # file paths
    manage_context(filename, g)
    print(f"g.filename: {g.filename}")
    file_path = os.path.join(config.UPLOAD_FOLDER, filename, 'versions')
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
                print('args:', args)

                selected_function = preprocessing.name_funcs_dict[request.values['process']]
                df = selected_function(*args)

                # Save processed DF
                temporary_path_parquet = os.path.join(file_path, f'{filename}_temp.parquet')
                df.to_parquet(temporary_path_parquet)

                # Append applied function to history and save to parquet
                history = history.append(
                    {'Tratamento': selected_function.name,
                     'Coluna': request.form.getlist('col'),
                     'Args': [str(c) for c in args[2:]]
                     },
                    ignore_index=True)
                history.to_parquet(file_path_history)

                # Save applied function to history
                history_path_parquet = os.path.join(file_path, f'{filename}_{history.index[-1]}.parquet')

                # Keep track of old DF and update current df
                os.rename(file_path_parquet, history_path_parquet)
                os.rename(temporary_path_parquet, file_path_parquet)

                # Update status of preprocessings
                update_status(filename, {'preprocessing': len(history)})

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
            return redirect(url_for('train.renderTrain', filename=filename))

        if request.form.get('action') == "back":
            return redirect(url_for('upload.uploadFiles', filename=filename))

    else:
        df = pd.read_parquet(file_path_parquet)

    # describe information
    describe = df.describe(include='all').reset_index()

    # dtypes information
    dtypes = pd.DataFrame(df.dtypes).reset_index()
    dtypes.columns = ['coluna', 'tipo']

    # noinspection PyTypeChecker
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