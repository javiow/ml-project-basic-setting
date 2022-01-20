import ast
from sklearn.model_selection import train_test_split
from lightgbm import LGBMRegressor
from xgboost import XGBRegressor

class MLMODEL():
    def __init__(self, param, model):

        params = ast.literal_eval(param)

        if model == 'lightgbm':
            self.model = LGBMRegressor(**params)
        elif model == 'xgboost':
            self.model = XGBRegressor(**params)
        else:
            print('Set the right model name')
            return 0

    def train(self, input):

        model = self.model

        x_train, x_valid, y_train, y_valid = train_test_split(input, test_size = 0.3, random_state=1234)

        evals = [(x_train, y_train), (x_valid, y_valid)]
        model.fit(x_train, y_train, early_stopping_rounds=50, eval_metric='rmse', eval_set=evals, verbose=True)

        self.model = model

    def predict(self, input):

        model = self.model
        pred = model.predict(input)

        return pred