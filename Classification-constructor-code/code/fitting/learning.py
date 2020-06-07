import importlib
import re

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


def load_class(full_name):
    """
    Вспомогательная функция для класса обучения
    """
    class_data = full_name.split(".")
    module_path = ".".join(class_data[:-1])
    class_str = class_data[-1]
    module = importlib.import_module(module_path)
    return getattr(module, class_str)


ensambles = {
    'voting': 'sklearn.ensemble.VotingClassifier',
    'adaboost': 'sklearn.ensemble.AdaBoostClassifier',
    'bagging': 'sklearn.ensemble.BaggingClassifier',
    'gradientboosting': 'sklearn.ensemble.GradientBoostingClassifier',
    'stacking': 'sklearn.ensemble.StackingClassifier'
}

base_estimators = {
    'neural network': 'sklearn.neural_network.MLPClassifier',
    'logistic regression': 'sklearn.linear_model.LogisticRegression',
    'decision tree': 'sklearn.tree.DecisionTreeClassifier'
}


class Learning:
    """
    Класс обучения
    """
    def __init__(self):
        base_algorithms = []
        for el in all_params['base algorithms']:
            cls_name = base_estimators[re.match('(?P<name>\D+) #\d', el).group('name')]
            tmp_estim = load_class(cls_name)(**all_params['base algorithms'][el])
            base_algorithms.append((el, tmp_estim))
        type_ensamble = all_params['common params']['composition method']

        if type_ensamble == 'voting':
            self.ensamble = load_class(ensambles[type_ensamble])(estimators=base_algorithms, voting='soft')
        elif type_ensamble == 'stacking':
            self.ensamble = load_class(ensambles[type_ensamble])(estimators=base_algorithms,
                                                                 **all_params['composition method'][type_ensamble])
        else:
            if len(base_algorithms) != 1:
                raise Exception('base algorith is not suitable for composition')
            else:
                self.ensamble = load_class(ensambles[type_ensamble])(base_estimator=base_algorithms[0][1],
                                                                     **all_params['composition method'][type_ensamble])

    def fit(self, X, y):
        self.ensamble.fit(X, y)

    def predict(self, X):
        return self.ensamble.predict(X)

    def score(self, X, y, sample_weight=None):
        return self.ensamble.score(X, y, sample_weight=sample_weight)

    def predict_proba(self, X):
        return self.ensamble.predict_proba(X)
