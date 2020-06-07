"""
Файл содержит словари common_params и methods_params, описывающие все возможные общие и частные параметры

Словарь common_params построен по типу 'название общего параметра':{'type':<питонячий тип данных>, 'values': <конкретные
 варианты или None, если вариатнов бесконечно много>}
Словарь methods_params построен аналогично, но с большим возможным уровнем вложенности

На основе словаря common_params (и только на его основе) создавался первый конфиг-файл, который заполнял пользователь

Далее считывался  файл, который заполнил пользователь, парсился, и на основе того, что заполнил пользователь + на
основе словаря methods_params опять создавался второй файл, который опять должен был заполнить пользователь

Пользователь заполнял второй файл, он опять парсился и на его основе создавался питонячий словарь all_params, который
использовал впоследствии ВЕЗДЕ, то есть он должен быть глобальным объектом

Так как теперь мы будем работать с json-файлами, надо по новой делать следующие операции:
1) Создание первого шаблона (незаполненного конфиг-файла) для пользователя
2) Парсинг первого заполненного файла и создание шаблона второго
3) ПАрсинг второго заполненного и создание словаря all_params (желательно, чтоб all_params был той же структуры, что и
раньше, чтоб много не перелопачивать)

Возможно, для этого сгодятся отдельные куски из предыдущего варианта, но вставлять еод парсинга я не буду
"""

common_params = {
    'name of model': {'type': str,  # название модели - нужно, чтоб потом легко находить пиклы и картинки
                      'values': None
                      },
    'default': {'type': str,
                'values': ['0', '1']},
    # 1 - использовать модель по умолчанию, 0 - не использовать, пока просто для виду, реальной модели по умолчанию нет
    'filling gaps method': {'type': str,
                            'values': ['HardRemoval', 'InsertMeanMode', 'LinearImputer'],
                            },
    'deleting anomalies method': {'type': str,
                                  'values': ['ThreeSigma', 'Grubbs', 'Interquartile', 'IsolationForest', 'Elliptic',
                                             'SVM', 'Approximate', 'LocalFactor']
                                  },
    'feature selection method': {'type': str,
                                 'values': ['VarianceThreshold', 'SelectKBest', 'SelectPercentile', 'SelectFpr',
                                            'SelectFdr', 'SelectFwe', 'GenericUnivariateSelect', 'RFE',
                                            'SelectFromModel']
                                 },
    'composition method': {'type': str,
                           'values': ['voting', 'adaboost', 'stacking']
                           },
    'neural network number': {'type': int,
                              'values': None
                              },
    'decision tree number': {'type': int,
                             'values': None
                             },
    'logistic regression number': {'type': int,
                                   'values': None
                                   },
    'test_ratio': {'type': float,  # добавил параметр
                   'values': None
                   },
}

methods_params = {

    'filling gaps method': {
        'InsertMeanMode': {'threshold': {'type': int, 'values': None}},
        'HardRemoval': {},
        'LinearImputer': {}
    },

    'deleting anomalies method': {
        'ThreeSigma': {},
        'Grubbs': {'alpha': {'type': float, 'values': None}},
        'Interquartile': {'low_quant': {'type': float, 'values': None},
                          'up_quant': {'type': float, 'values': None},
                          'coef': {'type': float, 'values': None}},
        'IsolationForest': {'n_estimators': {'type': int, 'values': None},
                            'contamination': {'type': float, 'values': None}},
        'Elliptic': {'contamination': {'type': float, 'values': None}},
        'SVM': {'iters': {'type': int, 'values': None}},
        'Approximate': {'deviation': {'type': int, 'values': None}},
        'LocalFactor': {'neigh': {'type': int, 'values': None},
                        'contamination': {'type': float, 'values': None},
                        'algorithm': {'type': str, 'values': ['auto', 'ball_tree', 'kd_tree', 'brute']}}
    },

    'feature selection method': {
        'VarianceThreshold': {'threshold': {'type': float, 'values': None}},
        'SelectKBest': {'k': {'type': int, 'values': None}},
        'SelectPercentile': {'percentile': {'type': int, 'values': None}},
        'SelectFpr': {'alpha': {'type': float, 'values': None}},
        'SelectFdr': {'alpha': {'type': float, 'values': None}},
        'SelectFwe': {'alpha': {'type': float, 'values': None}},
        'GenericUnivariateSelect': {'mode': {'type': str, 'values': ['percentile', 'k_best', 'fpr', 'fdr', 'fwe']},
                                    'param': {'type': float, 'values': None}},
        'RFE': {'n_features_to_select': {'type': int, 'values': None},
                'step': {'type': int, 'values': None}},
        'SelectFromModel': {'threshold': {'type': str, 'values': ['median', 'mean']},
                            'norm_order': {'type': int, 'values': None},
                            'max_features': {'type': int, 'values': None}}
    },

    'composition method': {
        'voting': {},
        'adaboost': {
            'n_estimators': {'type': int, 'values': None},
            'learning_rate': {'type': float, 'values': None},
            'algorithm': {'type': str, 'values': ['SAMME', 'SAMME.R']}},
        'stacking': {
            'stack_method': {'type': str, 'values': ['auto', 'predict_proba', 'decision_function', 'predict']},
            'cv': {'type': int, 'values': None}}
    },

    'base algorithms': {
        'neural network': {
            'activation': {'type': str, 'values': ['identity', 'logistic', 'tanh', 'relu']},
            'solver': {'type': str, 'values': ['lbfgs', 'sgd', 'adam']},
            'learning_rate': {'type': str, 'values': ['constant', 'invscaling', 'adaptive']}},
        'decision tree': {
            'criterion': {'type': str, 'values': ['gini', 'entropy']},
            'max_depth': {'type': int, 'values': None}},
        'logistic regression': {
            'solver': {'type': str, 'values': ['newton-cg', 'lbfgs', 'liblinear', 'sag', 'saga']},
            # важно смотреть, сочетаются ли solver и penalty
            'penalty': {'type': str, 'values': ['l1', 'l2', 'elasticnet']}}
    }
}
