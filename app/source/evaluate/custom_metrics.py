from autogluon.core.metrics import make_scorer
import sklearn.metrics as metrics

ag_accuracy_score = make_scorer(name='accuracy',
                                 score_func=metrics.accuracy_score,
                                 optimum=1,
                                 greater_is_better=True)

ag_precision_score = make_scorer(name='precision',
                                 score_func=metrics.precision_score,
                                 optimum=1,
                                 greater_is_better=True)

ag_recall_score = make_scorer(name='recall',
                                 score_func=metrics.recall_score,
                                 optimum=1,
                                 greater_is_better=True)

ag_f1_score = make_scorer(name='f1',
                                 score_func=metrics.f1_score,
                                 optimum=1,
                                 greater_is_better=True)

ag_roc_auc_score = make_scorer(name='roc_auc',
                                 score_func=metrics.roc_auc_score,
                                 optimum=1,
                                 greater_is_better=True,
                                 needs_threshold=True)


ag_mean_squared_error = make_scorer(name='mean_squared_error',
                                           score_func=metrics.mean_squared_error,
                                           optimum=0,
                                           greater_is_better=False)

ag_mean_absolute_error = make_scorer(name='mean_absolute_error',
                                           score_func=metrics.mean_absolute_error,
                                           optimum=0,
                                           greater_is_better=False)

ag_mean_absolute_percentage_error = make_scorer(name='mean_absolute_percentage_error',
                                           score_func=metrics.mean_absolute_percentage_error,
                                           optimum=0,
                                           greater_is_better=False)

classification_metrics = [ag_precision_score,
                          ag_recall_score,
                          ag_f1_score,
                          ag_roc_auc_score]

regression_metrics = [ag_mean_squared_error,
                      ag_mean_absolute_error,
                      ag_mean_absolute_percentage_error]