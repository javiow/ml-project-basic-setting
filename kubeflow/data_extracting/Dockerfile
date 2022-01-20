FROM kaggle/python
RUN pip install boto3 pandas joblib
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
COPY . /code/
ENTRYPOINT [ "python", "data_extracting.py" ]