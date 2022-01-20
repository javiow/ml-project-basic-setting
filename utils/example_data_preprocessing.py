import pandas as pd
from sklearn.preprocessing import StandardScaler

def sample_preprocessing(data):
    scaler = StandardScaler()
    return scaler.fit_transform(data)