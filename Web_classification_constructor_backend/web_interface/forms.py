from django import forms
from django.core.exceptions import ValidationError


def get_choices(choices):
    """Получение списка выбора в нужном формате"""
    return [(i, i) for i in choices]


def check_positive(value):
    """Проверка что число >= 0 или None"""
    if value < 0 or value is not None:
        raise ValidationError(f"{value} must be >=0 or None")


class Form1(forms.Form):
    """Форма для ввода общих параметров"""
    # field_1 = forms.IntegerField(required=False, help_text=" - Число")
    # field_2 = forms.CharField(required=False, initial="", help_text=" - Текст")
    # choices = [(1, 1), (2, 2), (3, 3)]
    # field_3 = forms.ChoiceField(choices=choices, required=False, initial="", help_text=" - Выбор")

    name_of_model = forms.CharField(required=False, initial="", empty_value=None, label="Название модели")

    choices = [(0, "Не использовать модель по-умолчанию"), (1, "Использовать модель по-умолчанию")]
    default = forms.ChoiceField(choices=choices, required=False, initial="", label="Модель по-умолчанию")

    choices = get_choices(['HardRemoval', 'InsertMeanMode', 'LinearImputer'])
    filling_gaps_method = forms.ChoiceField(choices=choices, required=False, initial="",
                                            label="Метод заполнения пробелов")

    choices = get_choices(['ThreeSigma', 'Grubbs', 'Interquartile', 'IsolationForest', 'Elliptic', 'SVM', 'Approximate',
                           'LocalFactor'])
    deleting_anomalies_method = forms.ChoiceField(choices=choices, required=False, initial="",
                                                  label="Метод удаления аномалий")

    choices = get_choices(['VarianceThreshold', 'SelectKBest', 'SelectPercentile', 'SelectFpr', 'SelectFdr',
                           'SelectFwe', 'GenericUnivariateSelect', 'RFE', 'SelectFromModel'])
    feature_selection_method = forms.ChoiceField(choices=choices, required=False, initial="",
                                                 label="Метод отбора признаков")

    choices = get_choices(['voting', 'adaboost', 'stacking'])
    composition_method = forms.ChoiceField(choices=choices, required=False, initial="", label="Метод композиций")

    neural_network_number = forms.IntegerField(required=False, label="Количество нейронных сетей",
                                               validators=[check_positive])

    decision_tree_number = forms.IntegerField(required=False, label="Количество решающих деревьев",
                                              validators=[check_positive])

    logistic_regression_number = forms.IntegerField(required=False, label="Количество логистических регрессий",
                                                    validators=[check_positive])

    test_ratio = forms.FloatField(required=False, validators=[check_positive])
