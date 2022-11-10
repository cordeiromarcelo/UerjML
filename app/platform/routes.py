from flask import Blueprint, render_template, request, redirect, url_for
import os
import io
import json
import config
import pandas as pd

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
    if request.method == 'GET':
        file_path = os.path.join(config.UPLOAD_FOLDER, filename)
        df = pd.read_csv(file_path, encoding='unicode_escape')
        return render_template("platform/table.html", column_names=df.columns.values,
                               row_data=list(df.values.tolist())[:10],
                               zip=zip, len=len)
    else:
        return redirect(url_for('platform.renderTableMap', filename=filename,
                                lat_col=request.values['lat'], long_col=request.values['long'],
                                peso_col=request.values['peso']))
