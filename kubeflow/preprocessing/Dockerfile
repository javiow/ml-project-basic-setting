FROM kaggle/python
RUN pip install pandas numpy datetime scipy sklearn pvlib boto3 kfp joblib
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
COPY . /code/
ENTRYPOINT [ "python", "preprocessing.py" ]