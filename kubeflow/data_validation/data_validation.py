import pandas as pd
import boto3
import re
import argparse
import joblib
import datetime as dt
import tensorflow_data_validation as tfdv
from io import BytesIO

import smtplib
from email.mime.text import MIMEText
from s3fs.core import S3FileSystem

def get_stat(
    
    BUCKET_NAME:str, 
    ACCESSKEY:str, 
    SECRETKEY:str):
    
    train_key = "mykey"
    test_key = "mykey"
    
    s3 = S3FileSystem(key=ACCESSKEY, secret=SECRETKEY)
    
    train_stat_former = joblib.load(s3.open('{}/{}'.format(BUCKET_NAME, train_key)))
    test_stat_former = joblib.load(s3.open('{}/{}'.format(BUCKET_NAME, test_key)))
    
    print(train_stat_former)
    print(test_stat_former)
    
    return train_stat_former, test_stat_former

def data_validation(stat, schema, former_stat):
    
    anomalies = tfdv.validate_statistics(statistics=stat, schema=schema, previous_statistics=former_stat)

    if anomalies.anomaly_info == {}:
        pass
    else:
        
        pattern = re.compile(r"reason \{(.*?)\}")
        anomalies_text = re.sub("\n", "", str(anomalies.anomaly_info))
        error_msg = re.findall(pattern, anomalies_text)[0].strip()
        
        pattern = re.compile(r"path \{(.*?)\}")
        error_part = re.findall(pattern, anomalies_text)[0].strip()
        
        error = error_part + " " + error_msg
        
        nowtime = dt.datetime.now() + dt.timedelta(hours=9)

        s = smtplib.SMTP('smtp.gmail.com', 587)

        s.starttls()
        s.login('send_from@email.com', args.email_key)

        msg = MIMEText("""
            시각: {} 
            에러 내용: {}
        """.format(nowtime, str(error)))
        msg['Subject'] = 'BASIC-ML-PIPELINE: 데이터 검증 작업 중 특이사항이 발생했습니다.'

        s.sendmail('send_from@email.com', 'send_to@email', msg.as_string())
        s.quit()
        
def upload_stat(BUCKET_NAME, ACCESSKEY, SECRETKEY, REGION_NAME, data, save_key):
    
    s3 = boto3.client('s3',
        aws_access_key_id = ACCESSKEY,
        aws_secret_access_key = SECRETKEY,
        region_name = REGION_NAME)

    bytes_io = BytesIO()
    joblib.dump(data, bytes_io)
    s3.put_object(Bucket=BUCKET_NAME, Body=bytes_io.getvalue(), Key=save_key)


if __name__ == '__main__':

    parser = argparse.ArgumentParser()

    parser.add_argument('--BUCKET_NAME', type=str, help='input BUCKET_NAME')
    parser.add_argument('--ACCESSKEY', type=str, help='input ACCESSKEY')
    parser.add_argument('--SECRETKEY', type=str, help='input SECRETKEY')
    parser.add_argument('--REGION_NAME', type=str, help='input REGION_NAME')
    parser.add_argument('--train_data_path', type=str, help='input train data path')
    parser.add_argument('--test_data_path', type=str, help='input test data path')
    parser.add_argument('--email_key', type=str, help='input email key')

    args = parser.parse_args()

    try:

        train_stat_former, test_stat_former = get_stat(
            args.BUCKET_NAME, 
            args.ACCESSKEY, 
            args.SECRETKEY
        )
        
        train_data = joblib.load(args.train_data_path)
        train_stat = tfdv.generate_statistics_from_dataframe(train_data)
        train_schema = tfdv.infer_schema(train_stat)
        
        # Numeric Column Example
        tfdv.get_feature(train_schema, 'column').float_domain.name = 'column'
        tfdv.get_feature(train_schema, 'column').float_domain.min = 0.0
        tfdv.get_feature(train_schema, 'column').float_domain.max = 1.0
        
        # Categoric Column Example
        tfdv.get_feature(train_schema, 'column').skew_comparator.infinity_norm.threshold = 0.001

        test_data = joblib.load(args.test_data_path)
        test_stat = tfdv.generate_statistics_from_dataframe(test_data)
        test_schema = tfdv.infer_schema(test_stat)
        
        data_validation(stat=train_stat, schema=train_schema, former_sta=train_stat_former)
        data_validation(stat=test_stat, schema=test_schema, former_stat=test_stat_former)
        
        nowtime = dt.datetime.now() + dt.timedelta(hours=9)
        nowtime = str(nowtime.year) + \
            (('0'+str(nowtime.month)) if nowtime.month < 10 else str(nowtime.month)) + \
            (('0'+str(nowtime.day)) if nowtime.day < 10 else str(nowtime.day))
        
        upload_stat(args.BUCKET_NAME, 
                      args.ACCESSKEY, 
                      args.SECRETKEY, 
                      args.REGION_NAME, 
                      data=train_stat, 
                      save_key="save_key")
        
        upload_stat(args.BUCKET_NAME, 
                      args.ACCESSKEY, 
                      args.SECRETKEY, 
                      args.REGION_NAME, 
                      data=test_stat, 
                      save_key="save_key")
            

    except Exception as error:

        nowtime = dt.datetime.now() + dt.timedelta(hours=9)

        s = smtplib.SMTP('smtp.gmail.com', 587)

        s.starttls()
        s.login('send_from@email.com', args.email_key)

        msg = MIMEText("""
            시각: {} 
            에러 내용: {}
        """.format(nowtime, str(error)))
        msg['Subject'] = 'BASIC-ML-PIPELINE: 데이터 검증 작업 중 에러가 발생했습니다.'

        s.sendmail('send_from@email.com', 'send_to@email', msg.as_string())
        s.quit()