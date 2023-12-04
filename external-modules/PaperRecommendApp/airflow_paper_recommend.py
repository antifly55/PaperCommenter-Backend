# append sys path to import core_paper_recommend
import sys
import configparser

properties = configparser.ConfigParser()
properties.read('config.ini')

CUSTOM_MODULE_PATH = properties['AIRFLOW']['PAPERRECOMMEND']

sys.path.append(CUSTOM_MODULE_PATH)


import airflow
from airflow import DAG
from airflow.operators.python import PythonOperator

# from core_paper_recommend import download_dataset, preprocess, train_model, inference_recommend_rating

def download_dataset():
    return

def preprocess():
    return

def train_model():
    return

def inference_recommend_rating():
    return

dag = DAG(
    dag_id="dag_paper_recommend_app",
    start_date=airflow.utils.dates.days_ago(3),
    schedule_interval="@daily"
)

operator_download_dataset = PythonOperator(
    task_id="download_dataset",
    python_callable=download_dataset,
    dag=dag
) ## argument: data_path

operator_preprocess = PythonOperator(
    task_id="preprocess",
    python_callable=preprocess,
    dag=dag
) ## argument: data_path

operator_dict_train_model = dict()

for features in [16, 32, 64, 128]:
    for lr in [0.1, 0.01, 0.001]:

        key = (features, lr)
        operator_dict_train_model[key] = []

        for start_epoch in range(0, 1000, 100):
            end_epoch = start_epoch + 100

            operator_current_train_model = PythonOperator(
                task_id=f"train_model_{features}_{lr}_{start_epoch}",
                python_callable=train_model,
                dag=dag
            ) ## argument: data_path, features, lr, start_epoch

            operator_dict_train_model[key].append(operator_current_train_model)

# define final pipeline
# operator_download_dataset >> operator_preprocess

# for features, lr in operator_dict_train_model.keys():
#     key = (features, lr)

