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
        # save the file
    return redirect(url_for('platform.renderTable', filename=uploaded_file.filename))


@platform.route('/<string:filename>/', methods=['GET', 'POST'])
def renderTable(filename):
    # get the uploaded file
    file_path = os.path.join(config.UPLOAD_FOLDER, filename)
    df = pd.read_csv(file_path, encoding='unicode_escape')
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
                               funcs=preprocessing.funcs,
                               options=preprocessing.options,
                               options_descriptions=preprocessing.options_descriptions,
                               zip=zip, len=len, str=str, list=list)
    else:
        print(request.values['col'])
        print(request.values['process'])
        print(request.values['opt'])

        return render_template("platform/table.html", column_names=df.columns.values,
                               row_data=list(df.values.tolist())[:1000],
                               describe_columns=describe.columns.values,
                               describe_data=list(describe.values.tolist()),
                               dtypes_columns=dtypes.columns.values,
                               dtypes_data=list(dtypes.values.tolist()),
                               funcs=preprocessing.funcs,
                               options=preprocessing.options,
                               options_descriptions=preprocessing.options_descriptions,
                               zip=zip, len=len, str=str, list=list)
        # return redirect(url_for('platform.renderTableMap', filename=filename,
        #                         lat_col=request.values['lat'], long_col=request.values['long'],
        #                         peso_col=request.values['peso']))
