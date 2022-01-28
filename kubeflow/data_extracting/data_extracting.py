import pandas as pd
import boto3
import argparse
import joblib
import datetime as dt

import smtplib
from email.mime.text import MIMEText

def get_data(BUCKET_NAME:str, ACCESSKEY:str, SECRETKEY:str, REGION_NAME:str, train_data_path:str, test_data_path:str):

    s3 = boto3.client('s3',
        aws_access_key_id = ACCESSKEY,
        aws_secret_access_key = SECRETKEY,
        region_name = REGION_NAME)

    s3_object = s3.get_object(Bucket=BUCKET_NAME, Key=train_data_path)
    train_data = pd.read_csv(s3_object['Body'])
    joblib.dump(train_data, '/mnt/train_data.pkl')

    s3_object = s3.get_object(Bucket=BUCKET_NAME, Key=test_data_path)
    test_data = pd.read_csv(s3_object['Body'])
    joblib.dump(test_data, '/mnt/test_data.pkl')

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

        get_data(args.BUCKET_NAME, args.ACCESSKEY, args.SECRETKEY, args.REGION_NAME, args.train_data_path, args.test_data_path)

    except Exception as error:

        nowtime = dt.datetime.now()

        s = smtplib.SMTP('smtp.gmail.com', 587)

        s.starttls()
        s.login('send_from@email.com', args.email_key)

        msg = MIMEText("""
            시각: {} 
            에러 내용: {}
        """.format(nowtime, str(error)))
        msg['Subject'] = 'BASIC-ML-PIPELINE: 데이터 추출 작업 중 에러가 발생했습니다.'

        s.sendmail('send_from@email.com', 'send_to@email', msg.as_string())
        s.quit()