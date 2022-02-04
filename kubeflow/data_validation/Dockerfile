FROM kaggle/python
RUN pip install tensorflow_data_validation datetime joblib boto3 aiobotocore
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
COPY . /code/
ENTRYPOINT [ "python", "data_validation.py" ]