import warnings
import datetime as dt
warnings.filterwarnings('ignore')

import kfp
from kfp import dsl

KUBEFLOW_HOST = 'http://127.0.0.1:31380/pipeline'
EXPERIMENT_NAME = 'ml pipeline example'

# AWS 인증키
ACCESSKEY = 'myaccesskey'
SECRETKEY = 'mysecretkey'
BUCKET_NAME = 'myawsbucketname'
REGION_NAME = 'myawsregionname'

# 이메일 인증키
EMAIL_KEY = 'myemailkey'

# ML파이프라인
def ml_pipeline():

    params = {'n_estimators':99999, 'learning_rate':0.01}
    model = 'xgboost'
    data_path = {'train':'input/train/train_sample.csv', 'test':'input/test/test_sample.csv'}
    
    # 데이터 저장할 퍼시스턴트 볼륨 생성
    vop = kfp.dsl.VolumeOp(
        name = 'data pvc',
        resource_name = 'data-pvc',
        size = '5Gi',
        modes = dsl.VOLUME_MODE_RWM
    )

    # 모델 저장할 퍼시스턴트 볼륨 생성
    model_vop = kfp.dsl.VolumeOp(
        name = 'model pvc',
        resource_name = 'model-pvc',
        size = '5Gi',
        modes = dsl.VOLUME_MODE_RWM
    )

    # 데이터 추출 컴포넌트
    data_extracting = kfp.dsl.ContainerOp(
        name = 'extracting data',
        image = 'my/data-extracting:latest',
        pvolumes = {'/mnt':vop.volume},
        arguments = [
            '--BUCKET_NAME', BUCKET_NAME,
            '--ACCESSKEY', ACCESSKEY,
            '--SECRETKEY', SECRETKEY,
            '--REGION_NAME', REGION_NAME,
            '--train_data_path', data_path['train'],
            '--test_data_path', data_path['test'],
            '--email_key', EMAIL_KEY,
        ],
        file_outputs = {
            'train_data_output':'/mnt/train_data.pkl',
            'test_data_output':'/mnt/test_data.pkl',
        }
    )

    # 데이터 검증 컴포넌트
    data_validation = kfp.dsl.ContainerOp(
        name = 'data validation',
        image = 'my/data-validation:latest',
        pvolumes = {'/mnt':vop.volume},
        arguments = [
            '--BUCKET_NAME', BUCKET_NAME,
            '--ACCESSKEY', ACCESSKEY,
            '--SECRETKEY', SECRETKEY,
            '--REGION_NAME', REGION_NAME,
            '--train_data_path', dsl.InputArgumentPath(data_extracting.outputs['train_data_output']),
            '--test_data_path', dsl.InputArgumentPath(data_extracting.outputs['test_data_output']),
            '--email_key', EMAIL_KEY,
        ]
    )

    # 데이터 전처리 컴포넌트
    preprocessing = kfp.dsl.ContainerOp(
        name = 'preprocessing data',
        image = 'my/preprocessing:latest',
        arguments = [
            '--train_data_path', dsl.InputArgumentPath(data_extracting.outputs['train_data_output']),
            '--test_data_path', dsl.InputArgumentPath(data_extracting.outputs['test_data_output']),
            '--email_key', EMAIL_KEY
        ],
        file_outputs = {
            'preprocessed_train_output':'/mnt/preprocessed_train_data.pkl',
            'preprocessed_test_output':'/mnt/preprocessed_test_data.pkl'
        }
    )

    # 모델 이름 생성
    nowtime = dt.datetime.now()
    nowtime = str(nowtime).split()[0][5:7]
    model_name = model + '_' + nowtime

    # 모델 학습 및 저장 컴포넌트
    training = kfp.dsl.ContainerOp(
        name = 'training',
        image = 'my/training:latest',
        arguments = [
            '--preprocessed_data_path', dsl.InputArgumentPath(preprocessing.outputs['preprocessed_train_output']),
            '--param', params,
            '--model', model,
            '--email_key', EMAIL_KEY,
        ],
        pvolumes = {'/mnt':model_vop.volume},
        file_outputs = {
            'model_output':'/mnt/{}.pkl'.format(model_name)
        }
    )

    # 모델 예측값 저장 경로
    nowtime = dt.datetime.now()
    save_key = 'output/output_{}'.format(str(nowtime.year) + \
        ('0' + str(nowtime.month) if len(str(nowtime.month)) == 1 else str(nowtime.month)) + \
        ('0' + str(nowtime.day) if len(str(nowtime.day)) == 1 else str(nowtime.day)) + \
        '_' + ('0' + str(nowtime.hour) if len(str(nowtime.hour)) == 1 else str(nowtime.hour)) + \
            ('0' + str(nowtime.minute) if len(str(nowtime.minute)) == 1 else str(nowtime.minute)) + '.csv')

    # 모델 예측 컴포넌트
    predicting = kfp.dsl.ContainerOp(
        name = 'predicting',
        image = 'my/predicting:latest',
        arguments = [
            '--model', model,
            '--preprocessed_test_path', dsl.InputArgumentPath(preprocessing.outputs['preprocessed_test_output']),
            '--save_key', save_key,
            '--BUCKET_NAME', BUCKET_NAME,
            '--ACCESSKEY', ACCESSKEY,
            '--SECRETKEY', SECRETKEY,
            '--REGION_NAME', REGION_NAME,
            '--email_key', EMAIL_KEY,
        ],
        pvolumes = {'/mnt':model_vop.volume.after(training)}
    )

    # 실행 관계 설정
    data_validation.after(data_extracting)
    preprocessing.after(data_extracting)
    training.after(preprocessing)
    predicting.after(training)
    

if __name__ == '__main__':

    # 파이프라인 실행
    kfp.Client(host=KUBEFLOW_HOST).create_run_from_pipeline_func(
        ml_pipeline,
        arguments = {},
        experiment_name = EXPERIMENT_NAME
    )

