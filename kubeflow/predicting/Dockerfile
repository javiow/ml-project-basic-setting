FROM kaggle/python
RUN pip install pandas numpy joblib sklearn xgboost lightgbm pvlib
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
COPY . /code/
ENTRYPOINT [ "python", "predicting.py" ]