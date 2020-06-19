import pandas as pd
import pickle
from preprocessing.missing_values_imputing import miss_fit
from preprocessing.outliers_deleting import outliers_fit
from preprocessing.normalization import normalize
from preprocessing.feature_selection import feature_selection_fit
from sklearn.model_selection import train_test_split
from fitting.learning import Learning
from fitting.predicting import predict_test
from report.get_images import feature_description, getting_estimators, get_all_images
from report.create_doc import get_doc
import os
import warnings

warnings.filterwarnings('ignore')

train_path = os.path.join(os.path.dirname(__file__), '..', 'Input', 'train.csv')
test_path = os.path.join(os.path.dirname(__file__), '..', 'Input', 'test.csv')

train = pd.read_csv(train_path)
test = pd.read_csv(test_path)

numerics = ['int16', 'int32', 'int64', 'float16', 'float32', 'float64']
numeric_cols = list(
    train.drop('target', axis=1).select_dtypes(include=numerics).columns)  # должно быть на входе

all_params = {'name of model with time of create': 'model1(2020-01-07-16-38-31)',
              'deleting anomalies method': {'Elliptic': {'contamination': 0.1}},
              'feature selection method': {'RFE': {'n_features_to_select': 8, 'step': 1}},
              'base algorithms': {'neural network #1': {'activation': 'logistic',
                                                        'solver': 'lbfgs',
                                                        'learning_rate': 'constant',
                                                        'learning_rate_init': 0.05},
                                  'neural network #2': {'activation': 'tanh',
                                                        'solver': 'sgd',
                                                        'learning_rate': 'invscaling',
                                                        'learning_rate_init': 0.01},
                                  'logistic regression #1': {'solver': 'lbfgs', 'penalty': 'l2'},
                                  'logistic regression #2': {'solver': 'lbfgs', 'penalty': 'l2'},
                                  'decision tree #1': {'criterion': 'entropy', 'max_depth': 6, 'min_samples_split': 5,
                                                       'min_samples_leaf': 2}},
              'name of model': 'model1',
              'filling gaps method': 'LinearImputer',
              'composition method': 'voting',
              'test_ratio': 0.25,
              'common params': {'name of model': 'model1',
                                'filling gaps method': 'LinearImputer',
                                'deleting anomalies method': 'Elliptic',
                                'feature selection method': 'RFE',
                                'composition method': 'voting',
                                'neural network number': 2,
                                'decision tree number': 0,
                                'logistic regression number': 2,
                                'test_ratio': 0.25}}  # это заглушка

# заполняем пропуски
train_miss = miss_fit(train, all_params)

# удаляем выбросы
train_outliers = outliers_fit(train_miss, all_params,
                              numeric_cols)
train_outliers = train_outliers.reset_index(drop=True)

# нормализуем - пока только standard scaler, поэтому all_params не нужен
train_scaled_all = normalize(train_outliers, numeric_cols, test)

# отбираем признаки + сохраняем модель featire selector в App
train_selected, selected_cols = feature_selection_fit(train_scaled_all, all_params, numeric_cols)

# итого - train_selected - готовый к обучению датафрейм
# сплитим на трейн и тест
X_train, X_test, y_train, y_test = train_test_split(train_selected.drop(columns=['id', 'target']),
                                                    train_selected['target'], test_size=all_params['test_ratio'])

# обучаемся и можем посмотреть результат
qwe = Learning()
qwe.fit(X_train, y_train)
print(qwe.score(X_test, y_test))

# сохраняем обученную модель
pickle_path = os.path.join(os.path.dirname(__file__), '..', 'App/models/{}/composition.pickle'.format(all_params[
                                                                                                          'name of model with time of create']))
with open(pickle_path, 'wb') as f:
    pickle.dump(qwe, f)

# предсказание и сохранение результатов в файл
pred_test = predict_test(test, all_params, selected_cols, pickle_path)
pred_test_with_features = test.merge(pred_test, on='id')
pred_test_with_features.to_csv(os.path.join(os.path.dirname(__file__), '..', 'Output/{}/fin_test.csv'.format(
    all_params['name of model with time of create'])))

# получение промежуточного результата для графиков и отчета
feats_descr = feature_description(X_train, train)
estimators_pred, estimators_prob, y_true = getting_estimators(pickle_path, X_test, y_test)

# создание картинок
get_all_images(estimators_prob, y_true)

# создание отчета
get_doc(pickle_path, train_path, feats_descr, pred_test, estimators_pred, y_true)
