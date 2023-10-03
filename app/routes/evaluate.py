import os

import pandas as pd
from flask import Blueprint, render_template, g, request, send_file

from app.source.evaluate.custom_metrics import classification_metrics, regression_metrics
from app.source.preprocessing import preprocessing
from app.source import utils

import app.config as config

from app.source.utils import manage_context, update_status, get_status

evaluate_bp = Blueprint('evaluate', __name__, url_prefix='/evaluate')


@evaluate_bp.route('/<string:filename>/', methods=['GET', 'POST'])
def renderEvaluate(filename):
    manage_context(filename, g)

    file_root = os.path.join(config.UPLOAD_FOLDER, filename)
    file_path = os.path.join(file_root, 'versions')
    predictions_path = os.path.join(file_root, 'predictions')
    model_path = os.path.join(file_root, 'AutoGluon')

    split = get_status(filename, "split")

    from autogluon.tabular import TabularPredictor
    predictor = TabularPredictor.load(os.path.join(file_root, 'AutoGluon'))

    problem_type = predictor.problem_type
    eval_metric = predictor.eval_metric

    if problem_type in ['binary', 'multiclass']:
        extra_metrics = classification_metrics

    elif problem_type == 'regression':
        extra_metrics = regression_metrics
    else:
        extra_metrics = []

    if split:
        df_test = pd.read_parquet(os.path.join(file_root, 'interim', 'test.parquet'))
        leaderboard = predictor.leaderboard(df_test, extra_metrics=extra_metrics, silent=True)
    else:
        leaderboard = predictor.leaderboard(silent=True)

    feature_importance = pd.read_parquet(os.path.join(model_path, 'feature_importance', 'fs.parquet'))
    best_model = predictor.get_model_best()

    best_model_row = leaderboard[leaderboard['model'] == best_model]
    score_test = round(best_model_row['score_test'].values[0], 3) if split else "-"
    score_val = round(best_model_row['score_val'].values[0], 3)

    update_status(filename, {'train': True,
                             'best_model': best_model,
                             'train_metric': predictor.eval_metric,
                             'train_score': score_val if score_test == "-" else score_test
                             })

    original_columns = get_status(filename, "original_columns")

    if request.method == 'POST':

        file_path_history = os.path.join(file_path, 'history.parquet')
        file_path_prediction = os.path.join(predictions_path, 'prediction.csv')
        file_path_csv = os.path.join(file_root, 'raw', filename + '_test.csv')

        uploaded_file = request.files['file']
        uploaded_file.save(file_path_csv)

        df = pd.read_csv(file_path_csv, encoding='unicode_escape')
        history = pd.read_parquet(file_path_history)

        cols = request.form.get('col')

        if cols is not None:
            if not isinstance(cols, list):
                cols = [cols]
            result = df[cols]

        for index, row in history.iterrows():
            selected_function = preprocessing.name_funcs_dict[row['Tratamento']]
            df = selected_function(df, row['Coluna'].tolist(), *utils.fix_args_types(row['Args']))

        if predictor.label in df.columns:
            leaderboard = predictor.leaderboard(df, extra_metrics=extra_metrics, silent=True)
            best_model_row = leaderboard[leaderboard['model'] == best_model]
            score_test = round(best_model_row['score_test'].values[0], 3)

        pred = getattr(predictor, request.form.get('predict'))(df)

        if cols is None:
            result = pd.DataFrame(pred)
        else:
            result[predictor.label] = pred.values

        result.to_csv(file_path_prediction, index=False)
        return send_file(file_path_prediction, as_attachment=True)

    return render_template('platform/evaluate.html',
                           leaderboard_columns=leaderboard.columns.values,
                           leaderboard_row=list(leaderboard.values)[:1000],
                           fs_columns=feature_importance.columns.values,
                           fs_row=list(feature_importance.values),
                           best_model=best_model,
                           eval_metric=eval_metric,
                           score_test=score_test,
                           score_val=score_val,
                           original_columns=original_columns,
                           zip=zip, len=len, str=str, list=list)