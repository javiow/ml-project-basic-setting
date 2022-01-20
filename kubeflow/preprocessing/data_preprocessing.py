from sklearn.preprocessing import MinMaxScaler

def sample_preprocessing(data):
    scaler = MinMaxScaler()
    return scaler.fit_transform(data)