import warnings
import joblib
import argparse
import datetime as dt
warnings.filterwarnings("ignore")

import smtplib
from email.mime.text import MIMEText

from ml_model import MLMODEL


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    
    parser.add_argument('--preprocessed_data_path', type=str, help='input preprocessed data path')
    parser.add_argument('--param', type=str, help='input parameters')
    parser.add_argument('--model', type=str, help='input model name')
    parser.add_argument('--email_key', type=str, help='input email key')

    args = parser.parse_args()

    try:

        preprocessed_data = joblib.load(args.preprocessed_data_path)

        ml_model = MLMODEL(args.param, args.model)
        ml_model.train(preprocessed_data)

        nowtime = dt.datetime.now()
        nowtime = str(nowtime).split()[0][5:7]
        model_name = args.model + '_' + nowtime

        joblib.dump(ml_model, '/mnt/{}.pkl'.format(model_name))

    except Exception as error:

        nowtime = dt.datetime.now() + dt.timedelta(hours=9)

        s = smtplib.SMTP('smtp.gmail.com', 587)

        s.starttls()
        s.login('send_from@email.com', args.email_key)

        msg = MIMEText("""
            시각: {} 
            에러 내용: {}
        """.format(nowtime, str(error)))
        msg['Subject'] = 'BASIC-ML-PIPELINE: 모델 학습 및 저장 작업 중 에러가 발생했습니다.'

        s.sendmail('send_from@email.com', 'send_to@email', msg.as_string())
        s.quit()
