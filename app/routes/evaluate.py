import os

import pandas as pd
from flask import Blueprint, render_template, g

from app.source.evaluate.custom_metrics import classification_metrics, regression_metrics
import app.config as config

evaluate_bp = Blueprint('evaluate', __name__, url_prefix='/evaluate')

@evaluate_bp.route('/<string:filename>/', methods=['GET', 'POST'])
def renderEvaluate(filename):
    g.filename = filename
    file_root = os.path.join(config.UPLOAD_FOLDER, filename)
    file_path = os.path.join(file_root, 'versions')
    model_path = os.path.join(file_root, 'AutoGluon')

    from autogluon.tabular import TabularPredictor
    predictor = TabularPredictor.load(os.path.join(file_root, 'AutoGluon'))
    df_test = pd.read_parquet(os.path.join(file_root, 'interim', 'test.parquet'))

    problem_type = predictor.problem_type
    eval_metric = predictor.eval_metric

    if problem_type in ['binary', 'multiclass']:
        extra_metrics = classification_metrics

    elif problem_type == 'regression':
        extra_metrics = regression_metrics
    else:
        extra_metrics = []

    leaderboard = predictor.leaderboard(df_test,extra_metrics=extra_metrics, silent=True)
    feature_importance = pd.read_parquet(os.path.join(model_path, 'feature_importance', 'fs.parquet'))
    best_model = predictor.get_model_best()

    best_model_row = leaderboard[leaderboard['model'] == best_model]
    score_test = round(best_model_row['score_test'].values[0], 3)
    score_val = round(best_model_row['score_val'].values[0], 3)

    return render_template('platform/evaluate.html',
                           leaderboard_columns=leaderboard.columns.values,
                           leaderboard_row=list(leaderboard.values)[:1000],
                           fs_columns=feature_importance.columns.values,
                           fs_row=list(feature_importance.values),
                           best_model=best_model,
                           eval_metric=eval_metric,
                           score_test=score_test,
                           score_val=score_val,
                           zip=zip, len=len, str=str, list=list)