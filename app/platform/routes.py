from flask import Blueprint, render_template, request, redirect, url_for
import os
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
        file_path = os.path.join(config.UPLOAD_FOLDER, uploaded_file.filename)
        # set the file path
        uploaded_file.save(file_path)
        df = pd.read_csv(file_path, encoding='unicode_escape')

        filename = uploaded_file.filename.split('.')[0]
        df.to_parquet(os.path.join(config.UPLOAD_FOLDER, filename + '.parquet'))
    else:
        raise Exception('O arquivo não possui nome')

        # save the file
    return redirect(url_for('platform.renderTable', filename=filename))


@platform.route('/<string:filename>/', methods=['GET', 'POST'])
def renderTable(filename):

    filename = filename + '.parquet'
    # get the uploaded file
    file_path = os.path.join(config.UPLOAD_FOLDER, filename)
    df = pd.read_parquet(file_path)

    describe = df.describe().reset_index()

    dtypes = pd.DataFrame(df.dtypes).reset_index()
    dtypes.columns = ['coluna', 'tipo']

    if request.method == 'GET':
        return render_template("platform/table.html", column_names=df.columns.values,
                               row_data=list(df.values.tolist())[:1000],
                               describe_columns=describe.columns.values,
                               describe_data=list(describe.values.tolist()),
                               dtypes_columns=dtypes.columns.values,
                               dtypes_data=list(dtypes.values.tolist()),
                               funcs=preprocessing.category_funcs_dict,
                               options=preprocessing.funcs_options_dict,
                               options_descriptions=preprocessing.options_descriptions_dict,
                               zip=zip, len=len, str=str, list=list)
    else:

        selected_function = preprocessing.name_funcs_dict[request.values['process']]
        df = selected_function(df, request.form.getlist('col'), request.values['opt'])
        df.to_parquet(file_path)

        describe = df.describe().reset_index()

        dtypes = pd.DataFrame(df.dtypes).reset_index()
        dtypes.columns = ['coluna', 'tipo']

        return render_template("platform/table.html", column_names=df.columns.values,
                               row_data=list(df.values.tolist())[:1000],
                               describe_columns=describe.columns.values,
                               describe_data=list(describe.values.tolist()),
                               dtypes_columns=dtypes.columns.values,
                               dtypes_data=list(dtypes.values.tolist()),
                               funcs=preprocessing.category_funcs_dict,
                               options=preprocessing.funcs_options_dict,
                               options_descriptions=preprocessing.options_descriptions_dict,
                               zip=zip, len=len, str=str, list=list)

        # return redirect(url_for('platform.renderTableMap', filename=filename,
        #                         lat_col=request.values['lat'], long_col=request.values['long'],
        #                         peso_col=request.values['peso']))
