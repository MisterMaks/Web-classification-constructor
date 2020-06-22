import pandas as pd


def check_df(path, is_train=True):

    try:
        try:
            df = pd.read_csv(path)
        except Exception:
            return False, 'Проблемы с чтением csv-файла'

        if 'id' not in df.columns:
            return False, 'Нет поля id'
        if is_train:
            if 'target' not in df.columns:
                return False, 'Для train нет поля target'
            if df['target'].max() != 1:
                return False, 'В target есть значения больше единицы'
            if df['target'].min() != 0:
                return False, 'В target есть значения меньше нуля'
            if df['target'].nunique() != 2:
                return False, 'В target есть значения помимо нуля и единицы'
        numeric_types = ['int16', 'int32', 'int64', 'float16', 'float32', 'float64']
        for column in df.columns:
            if column != 'id' and df[column].dtype not in numeric_types:
                print(f'{column} не числовая колонка. Удалите ее или создайте категориальную(-ые) переменную(-ые)')
                return False
        return True, 'Файл загружен'
    except Exception:
        print('что-то пошло не так...')
        return False


# print(check_df('train.csv', is_train=True))
# print(check_df('test.csv', is_train=False))
