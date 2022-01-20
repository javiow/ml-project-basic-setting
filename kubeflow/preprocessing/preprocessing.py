import argparse
import joblib
import datetime as dt

import smtplib
from email.mime.text import MIMEText

from data_preprocessing import *

def data_preprocessing(train_data_path, test_data_path):

    train_data = joblib.load(train_data_path)
    test_data = joblib.load(test_data_path)
    print(train_data.head())

    preprocessed_train_data = sample_preprocessing(train_data)
    preprocessed_test_data = sample_preprocessing(test_data)
    print(preprocessed_train_data.head())

    print(test_data.head())
    print(preprocessed_test_data.head())
    joblib.dump(preprocessed_train_data, '/mnt/preprocessed_train_data.pkl')
    joblib.dump(preprocessed_test_data, '/mnt/preprocessed_test_data.pkl')
    

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--train_data_path', type=str, help='input train data')
    parser.add_argument('--test_data_path', type=str, help='input test data')
    parser.add_argument('--email_key', type=str, help='input email key')

    args = parser.parse_args()

    try:

        data_preprocessing(args.train_data_path, args.test_data_path)

    except Exception as error:

        nowtime = dt.datetime.now()

        s = smtplib.SMTP('smtp.gmail.com', 587)

        s.starttls()
        s.login('my_email@gmail.com', args.email_key)

        msg = MIMEText("""
            시각: {} 
            에러 내용: {}
        """.format(nowtime, str(error)))
        msg['Subject'] = 'BASIC-ML-PIPELINE: 데이터 전처리 작업 중 에러가 발생했습니다.'

        s.sendmail('my_email@gmail.com', msg.as_string())
        s.quit()
