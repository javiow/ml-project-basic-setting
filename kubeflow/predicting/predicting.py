import warnings
import argparse
import datetime as dt
import joblib
import boto3
import pandas as pd
from io import StringIO
warnings.filterwarnings("ignore")

import smtplib
from email.mime.text import MIMEText

from ml_model import MLMODEL

def upload_data(BUCKET_NAME, ACCESSKEY, SECRETKEY, REGION_NAME, pred_data, save_key):
    s3 = boto3.client('s3',
        aws_access_key_id = ACCESSKEY,
        aws_secret_access_key = SECRETKEY,
        region_name = REGION_NAME)

    string_io = StringIO()
    pred_data.to_csv(string_io, header=True, index=False)
    s3.put_object(Bucket=BUCKET_NAME, Body=string_io.getvalue(), Key=save_key)

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    
    parser.add_argument('--model', type=str, help='input model name')
    parser.add_argument('--preprocessed_test_path', type=str, help='input preprocessed test data')
    parser.add_argument('--save_key', type=str, help='input save path')
    parser.add_argument('--BUCKET_NAME', type=str, help='input BUCKET_NAME')
    parser.add_argument('--ACCESSKEY', type=str, help='input ACCESSKEY')
    parser.add_argument('--SECRETKEY', type=str, help='input SECRETKEY')
    parser.add_argument('--REGION_NAME', type=str, help='input REGION_NAME')
    parser.add_argument('--email_key', type=str, help='input email key')

    args = parser.parse_args()

    try:

        nowtime = dt.datetime.now() + dt.timedelta(hours=9)
        nowtime = str(nowtime).split()[0][5:7]
        model_name = args.model + '_' + nowtime

        preprocessed_test_data = joblib.load(args.preprocessed_test_path)

        MLMODEL = joblib.load('/mnt/' + model_name + '.pkl')

        pred = MLMODEL.predict(preprocessed_test_data)

        pred_df = pd.DataFrame({'index':preprocessed_test_data.index.to_list(), 'value':pred})
        upload_data(args.BUCKET_NAME, args.ACCESSKEY, args.SECRETKEY, args.REGION_NAME, pred_df, args.save_key)

    except Exception as error:

        nowtime = dt.datetime.now() + dt.timedelta(hours=9)

        s = smtplib.SMTP('smtp.gmail.com', 587)

        s.starttls()
        s.login('send_from@email.com', args.email_key)

        msg = MIMEText("""
            시각: {} 
            에러 내용: {}
        """.format(nowtime, str(error)))
        msg['Subject'] = 'BASIC-ML-PIPELINE: 모델 예측 작업 중 에러가 발생했습니다.'

        s.sendmail('send_from@email.com', 'send_to@email', msg.as_string())
        s.quit()