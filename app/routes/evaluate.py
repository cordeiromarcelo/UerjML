import os

import pandas as pd
from flask import Blueprint, render_template, request, redirect, url_for

from app.source.evaluate.custom_metrics import classification_metrics, regression_metrics
import config

evaluate_bp = Blueprint('evaluate', __name__, url_prefix='/')

@evaluate_bp.route('/<string:filename>/model/evaluate', methods=['GET', 'POST'])
def renderEvaluate(filename):
    file_root = os.path.join(config.UPLOAD_FOLDER, filename)
    file_path = os.path.join(file_root, 'versions')

    from autogluon.tabular import TabularPredictor
    predictor = TabularPredictor.load(os.path.join(file_root, 'AutoGluon'))
    df_test = pd.read_parquet(os.path.join(file_root, 'interim', 'test.parquet'))

    problem_type = predictor.problem_type

    if problem_type in ['binary', 'multiclass']:
        extra_metrics = classification_metrics

    elif problem_type == 'regression':
        extra_metrics = regression_metrics
    else:
        extra_metrics = []

    leaderboard = predictor.leaderboard(df_test,extra_metrics=extra_metrics, silent=False)

    return render_template('platform/evaluate.html',
                           leaderboard_columns=leaderboard.columns.values,
                           leaderboard_row=list(leaderboard.values.tolist())[:1000],
                           zip=zip, len=len, str=str, list=list)