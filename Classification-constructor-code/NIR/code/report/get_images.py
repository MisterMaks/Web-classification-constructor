import numpy as np
import pickle
from sklearn.metrics import *
import matplotlib.pyplot as plt
import pandas as pd

all_params = {'name of model with time of create': 'model1(2020-01-07-16-38-31)',
              'deleting anomalies method': {'Elliptic': {'contamination': 0.1}},
              'feature selection method': {'RFE': {'n_features_to_select': 8, 'step': 1}},
              'base algorithms': {'neural network #1': {'activation': 'logistic',
                                                        'solver': 'lbfgs',
                                                        'learning_rate': 'constant'},
                                  'neural network #2': {'activation': 'tanh',
                                                        'solver': 'sgd',
                                                        'learning_rate': 'invscaling'},
                                  'logistic regression #1': {'solver': 'lbfgs', 'penalty': 'l2'},
                                  'logistic regression #2': {'solver': 'lbfgs', 'penalty': 'l2'}},
              'name of model': 'model1',
              'default': '0',
              'filling gaps method': 'LinearImputer',
              'composition method': 'voting',
              'test_ratio': 0.25,
              'common params': {'name of model': 'model1',
                                'default': '0',
                                'filling gaps method': 'LinearImputer',
                                'deleting anomalies method': 'Elliptic',
                                'feature selection method': 'RFE',
                                'composition method': 'voting',
                                'neural network number': 2,
                                'decision tree number': 0,
                                'logistic regression number': 2,
                                'test_ratio': 0.25}}  # это заглушка


def getting_estimators(pickle_path, X_test, y_test):
    """
    Функция для получения важных данных по отдельным базовым алгоритмам
    :param pickle_path:
    :param X_test:
    :param y_test:
    :return:
    """
    with open(pickle_path, 'rb') as f:
        model = pickle.load(f)

    # предсказания на каждом базовом алгоритме
    estimators_pred = {}
    estimators_prob = {}

    if all_params['common params']['composition method'] in ['voting', 'stacking']:
        for name, mod in zip(model.ensamble.estimators, model.ensamble.estimators_):
            y_prob = mod.predict_proba(X_test)[:, 1]
            y_pred = np.array([1 if x > 0.5 else 0 for x in y_prob])
            estimators_pred[name[0]] = y_pred
            estimators_prob[name[0]] = y_prob
    else:
        for mod in model.ensamble.estimators_:
            y_prob = mod.predict_proba(X_test)[:, 1]
            y_pred = np.array([1 if x > 0.5 else 0 for x in y_prob])

    # предсказание на финальном алгоритме
    y_prob = model.predict_proba(X_test)[:, 1]
    y_pred = np.array([1 if x > 0.5 else 0 for x in y_prob])
    estimators_pred['final_model'] = y_pred
    estimators_prob['final_model'] = y_prob

    # истинные ответы
    y_true = y_test

    return estimators_pred, estimators_prob, y_true


def feature_description(df, train):
    """
    КАкая-то вспомогательная функция
    :param df:
    :param train:
    :return:
    """
    features = df.columns
    feature_descr = [['#', 'Feature name', 'Mean', 'Median', 'Std', 'Variation']]
    for i, f in enumerate(features):
        nulls = df[f].isna().sum() / train.shape[0]
        mean = df[f].mean()
        median = df[f].median()
        std = df[f].std()
        r = df[f].max() - train[f].min()
        feature_descr.append([i, f, round(mean, 2), round(median, 2), round(std, 2), round(r, 2)])
    return np.array(feature_descr)


def create_plot(arr, xlabel, ylabel, title, img_save_path, diag=False, dpi=200, font_size=15, linewidth=2,
                figsize=(10, 8)):
    """
    Вспомогательная функция для построения графиков
    """
    plt.figure(figsize=figsize)
    if diag:
        plt.plot([0, 1], [0, 1], linestyle='dashed')

    plt.grid()
    plt.xlabel(xlabel, size=font_size)
    plt.ylabel(ylabel, size=font_size)
    plt.title(title, size=font_size)

    for x, y, name in arr:
        plt.plot(x, y, linewidth=linewidth, label=name)

    plt.legend()
    plt.savefig(img_save_path, dpi=dpi)


def create_hist(ones, zeros, name):
    """
  Вспомогательная функция для построения гистограммы
  """
    plt.figure(figsize=(10, 8))
    plt.title(f'Score distribution: {name}', size=15)
    plt.hist(ones, bins=50, alpha=0.5, label='класс 1')
    plt.hist(zeros, bins=50, alpha=0.5, label='класс 0')
    plt.xlabel('Score', size=15)
    plt.ylabel('Число набрюдений', size=15)
    plt.legend()
    plt.savefig('/home/alexey/NIR/App/images/{}/Distribution_graph {}.png'.format(all_params['name of model with time of create'], name),
                dpi=200)


def get_all_images(estimators_prob, y_true):
    """
    Главная функция для создания и сохранения всех картинок куда надо
    :param estimators_prob: словарь вероятностей для БА
    :param y_true: реальные данные валидационной выборки
    :return:
    """
    for key, value in estimators_prob.items():
        fpr, tpr, thr = roc_curve(y_true, value)
        create_plot([(fpr, tpr, key)], 'False Positive Rate', 'True Positive Rate', 'ROC curve',
                    '/home/alexey/NIR/App/images/{}/ROC_curve {}.png'.format(all_params['name of model with time of create'], key),
                    diag=True)
    arr = []
    for key, value in estimators_prob.items():
        fpr, tpr, thr = roc_curve(y_true, value)
        arr.append((fpr, tpr, key))
    create_plot(arr, 'False Positive Rate', 'True Positive Rate', 'ROC curve',
                '/home/alexey/NIR/App/images/{}/ROC_curve.png'.format(all_params['name of model with time of create']), diag=True)

    for key, value in estimators_prob.items():
        precision, recall, thr = precision_recall_curve(y_true, value)
        create_plot([(recall, precision, key)], 'Recall', 'Precision', 'PR curve',
                    '/home/alexey/NIR/App/images/{}/PR_curve {}.png'.format(all_params['name of model with time of create'], key))

    arr = []
    for key, value in estimators_prob.items():
        precision, recall, thr = precision_recall_curve(y_true, value)
        arr.append((recall, precision, key))
    create_plot(arr, 'Recall', 'Precision', 'PR curve',
                '/home/alexey/NIR/App/images/{}/PR_curve.png'.format(all_params['name of model with time of create']))

    for key, value in estimators_prob.items():
        ones = [x[1] for x in zip(y_true, value) if x[0] == 1]
        zeros = [x[1] for x in zip(y_true, value) if x[0] == 0]
        create_hist(ones, zeros, key)

    y_prob = estimators_prob['final_model']

    pred_min, pred_max = min(y_prob), max(y_prob)
    step = (pred_max - pred_min) / 100
    step_range = np.arange(pred_min, pred_max, step)
    predictions = []

    for threshold in step_range:
        preds_binary = np.where(y_prob > threshold, 1, 0)
        prc = round(precision_score(y_true, preds_binary), 3)
        rec = round(recall_score(y_true, preds_binary), 3)
        f1 = round(f1_score(y_true, preds_binary), 3)
        predictions.append([threshold, prc, rec, f1])

    results = pd.DataFrame(predictions, columns=['threshold', 'precision', 'recall', 'f1'])
    ax = results[['precision', 'recall', 'f1']].plot(figsize=(12, 10),
                                                     grid=True,
                                                     title='Precision & Recall by percentile',
                                                     fontsize=14)
    fig = ax.get_figure()
    fig.savefig('/home/alexey/NIR/App/images/{}/PR_by_prc.png'.format(all_params['name of model with time of create']), dpi=200)
