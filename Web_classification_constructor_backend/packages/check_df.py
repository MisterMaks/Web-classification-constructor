import pandas as pd


def check_df(path, is_train=True):

    try:
        try:
            df = pd.read_csv(path)
        except Exception:
            # print('Проблемы с чтением csv-файла')
            return False

        if 'id' not in df.columns:
            print('нет поля id')
            return False
        if is_train:
            if 'target' not in df.columns:
                print('для train нет поля target')
                return False
            if df['target'].nunique() != 2:
                print('not 2 marks')
                return False
            if df['target'].max() != 1:
                print('pos value is not 1')
                return False
            if df['target'].min() != 0:
                print('neg value is not 0')
                return False
        numeric_types = ['int16', 'int32', 'int64', 'float16', 'float32', 'float64']
        for column in df.columns:
            if column != 'id' and df[column].dtype not in numeric_types:
                print(f'{column} is not numeric column')
                return False
        return True
    except Exception:
        print('что-то пошло не так...')
        return False


# print(check_df('train.csv', is_train=True))
# print(check_df('test.csv', is_train=False))
