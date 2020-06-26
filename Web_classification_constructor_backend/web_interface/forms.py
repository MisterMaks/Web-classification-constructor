from django import forms
from django.core.exceptions import ValidationError


def get_choices(choices):
    """Получение списка выбора в нужном формате"""
    return [(i, i) for i in choices]


def check_positive(value):
    """Проверка что число > 0"""
    if not (value > 0):
        raise ValidationError(f"{value} must be >0")


def check_zero_one(value):
    """Проверка что число между 0 и 1 не включая"""
    if not (1 > value > 0):
        raise ValidationError(f"{value} must be in (0, 1)")


def check_1_100(value):
    """Проверка что число между 1 и 100 включая"""
    if not (100 >= value >= 1):
        raise ValidationError(f"{value} must be in [1, 100]")


class Form1(forms.Form):
    """Форма для ввода общих параметров"""
    # field_1 = forms.IntegerField(required=False, help_text=" - Число")
    # field_2 = forms.CharField(required=False, initial="", help_text=" - Текст")
    # choices = [(1, 1), (2, 2), (3, 3)]
    # field_3 = forms.ChoiceField(choices=choices, required=False, initial="", help_text=" - Выбор")

    # name_of_model = forms.CharField(required=False, initial="", empty_value=None, label="Название модели")

    choices = get_choices(['HardRemoval', 'InsertMeanMode', 'LinearImputer'])
    filling_gaps_method = forms.ChoiceField(choices=choices, required=False, initial="",
                                            label="Метод заполнения пробелов")

    choices = get_choices(['ThreeSigma', 'Grubbs', 'IsolationForest', 'Elliptic', 'SVM'])
    deleting_anomalies_method = forms.ChoiceField(choices=choices, required=False, initial="",
                                                  label="Метод удаления аномалий")

    choices = get_choices(['VarianceThreshold', 'SelectKBest', 'SelectPercentile', 'SelectFpr', 'SelectFdr',
                           'SelectFwe', 'RFE'])
    feature_selection_method = forms.ChoiceField(choices=choices, required=False, initial="",
                                                 label="Метод отбора признаков")

    choices = get_choices(['voting', 'adaboost', 'stacking'])
    composition_method = forms.ChoiceField(choices=choices, required=False, initial="", label="Метод композиций")

    neural_network_number = forms.IntegerField(required=False, label="Количество нейронных сетей",
                                               min_value=0, max_value=5)

    decision_tree_number = forms.IntegerField(required=False, label="Количество решающих деревьев",
                                              min_value=0, max_value=5)

    logistic_regression_number = forms.IntegerField(required=False, label="Количество логистических регрессий",
                                                    min_value=0, max_value=5)

    test_ratio = forms.FloatField(required=False, validators=[check_zero_one])


class FillingGapsMethodInsertMeanMode(forms.Form):
    threshold = forms.IntegerField(required=False, label="Пороговое значение", validators=[check_positive])


class FillingGapsMethodHardRemoval(forms.Form):
    pass


class FillingGapsMethodLinearImputer(forms.Form):
    pass


class DeletingAnomaliesMethodThreeSigma(forms.Form):
    pass


class DeletingAnomaliesMethodGrubbs(forms.Form):
    alpha = forms.FloatField(required=False, validators=[check_zero_one])


# class DeletingAnomaliesMethodInterquartile(forms.Form):
#     low_quant = forms.FloatField(required=False, validators=[check_zero_one])
#     up_quant = forms.FloatField(required=False, validators=[check_zero_one])
#     coef = forms.FloatField(required=False, validators=[check_zero_one])


class DeletingAnomaliesMethodIsolationForest(forms.Form):
    n_estimators = forms.IntegerField(required=False, min_value=1, max_value=1000)
    contamination = forms.FloatField(required=False, min_value=0.01, max_value=0.5)


class DeletingAnomaliesMethodElliptic(forms.Form):
    contamination = forms.FloatField(required=False, min_value=0.01, max_value=0.5)


class DeletingAnomaliesMethodSVM(forms.Form):
    iters = forms.IntegerField(required=False, validators=[check_positive])


# class DeletingAnomaliesMethodApproximate(forms.Form):
#     deviation = forms.IntegerField(required=False)


# class DeletingAnomaliesMethodLocalFactor(forms.Form):
#     neigh = forms.IntegerField(required=False, validators=[check_positive])
#     contamination = forms.FloatField(required=False, validators=[check_zero_one])
#
#     choices = get_choices(['auto', 'ball_tree', 'kd_tree', 'brute'])
#     algorithm = forms.ChoiceField(choices=choices, required=False, initial="")


class FeatureSelectionMethodVarianceThreshold(forms.Form):
    threshold = forms.FloatField(required=False, min_value=0.01, max_value=1)


class FeatureSelectionMethodSelectKBest(forms.Form):
    k = forms.IntegerField(required=False, validators=[check_positive])


class FeatureSelectionMethodSelectPercentile(forms.Form):
    percentile = forms.IntegerField(required=False, validators=[check_1_100])


class FeatureSelectionMethodSelectFpr(forms.Form):
    alpha = forms.FloatField(required=False, validators=[check_zero_one])


class FeatureSelectionMethodSelectFdr(forms.Form):
    alpha = forms.FloatField(required=False, validators=[check_zero_one])


class FeatureSelectionMethodSelectFwe(forms.Form):
    alpha = forms.FloatField(required=False, validators=[check_zero_one])


# class FeatureSelectionMethodGenericUnivariateSelect(forms.Form):
#     choices = get_choices(['percentile', 'k_best', 'fpr', 'fdr', 'fwe'])
#     mode = forms.ChoiceField(choices=choices, required=False, initial="")
#
#     param = forms.FloatField(required=False, validators=[check_positive])


class FeatureSelectionMethodRFE(forms.Form):
    n_features_to_select = forms.IntegerField(required=False, validators=[check_positive])
    step = forms.IntegerField(required=False, validators=[check_positive])


# class FeatureSelectionMethodSelectFromModel(forms.Form):
#     choices = get_choices(['median', 'mean'])
#     threshold = forms.ChoiceField(choices=choices, required=False, initial="")
#
#     norm_order = forms.IntegerField(required=False, validators=[check_positive])
#     max_features = forms.IntegerField(required=False, validators=[check_positive])


class CompositionMethodVoting(forms.Form):
    pass


class CompositionMethodAdaboost(forms.Form):
    n_estimators = forms.IntegerField(required=False, min_value=1, max_value=100)
    learning_rate = forms.FloatField(required=False, min_value=0.01, max_value=1)

    choices = get_choices(['SAMME', 'SAMME.R'])
    algorithm = forms.ChoiceField(choices=choices, required=False, initial="")


class CompositionMethodStacking(forms.Form):
    choices = get_choices(['auto', 'predict_proba', 'decision_function', 'predict'])
    stack_method = forms.ChoiceField(choices=choices, required=False, initial="")

    cv = forms.IntegerField(required=False, min_value=2, max_value=10)


class NeuralNetwork(forms.Form):
    choices = get_choices(['identity', 'logistic', 'tanh', 'relu'])
    activation = forms.ChoiceField(choices=choices, required=False, initial="")

    choices = get_choices(['lbfgs', 'sgd', 'adam'])
    solver = forms.ChoiceField(choices=choices, required=False, initial="")

    choices = get_choices(['constant', 'invscaling', 'adaptive'])
    learning_rate = forms.ChoiceField(choices=choices, required=False, initial="")

    learning_rate_init = forms.FloatField(required=False, min_value=0.01, max_value=1)


class DecisionTree(forms.Form):
    choices = get_choices(['gini', 'entropy'])
    criterion = forms.ChoiceField(choices=choices, required=False, initial="")

    max_depth = forms.IntegerField(required=False, min_value=2, max_value=50)
    min_samples_split = forms.IntegerField(required=False, min_value=2)
    min_samples_leaf = forms.IntegerField(required=False, min_value=1)


class LogisticRegression(forms.Form):
    choices = get_choices(['newton-cg', 'lbfgs', 'liblinear', 'sag', 'saga'])
    solver = forms.ChoiceField(choices=choices, required=False, initial="")

    choices = get_choices(['l1', 'l2', 'elasticnet', 'none'])
    penalty = forms.ChoiceField(choices=choices, required=False, initial="")


class UploadFileForm(forms.Form):
    # title = forms.CharField(max_length=50)
    file_train = forms.FileField(required=False)
    file_test = forms.FileField(required=False)


class UploadModelFileForm(forms.Form):
    trained_model = forms.FileField(required=False)
    file_test = forms.FileField(required=False)
