from datetime import datetime

from airflow import DAG
from airflow.contrib.hooks.slack_webhook_hook import SlackWebhookHook
from airflow.contrib.operators.slack_webhook_operator import SlackWebhookOperator
from airflow.operators.python_operator import PythonOperator

import utils.slack_monkey_patch

utils.slack_monkey_patch.apply_monkey_patch_if_needed()

default_args = {
    'start_date': datetime(2019, 4, 1),
}


def slack_webhook_hook_demo():
    slack = SlackWebhookHook(
        http_conn_id='slack',
        message='Hello, world! (SlackWebhookHook)',
        username='SlackWebhookHook',
        icon_emoji=':cat:',
        link_names=True)
    slack.execute()


with DAG('slack_demo',
         default_args=default_args,
         schedule_interval='*/1 * * * *',
         catchup=False) as dag:
    first = SlackWebhookOperator(
        task_id='slack_webhook_operator_demo',
        http_conn_id='slack',
        message='*Hello, world!* (SlackWebhookOperator)\nhttps://airflow.apache.org/',
        username='SlackWebhookOperator',
        icon_emoji=':dog:',
        link_names=True,
        dag=dag)

    second = PythonOperator(
        task_id='slack_webhook_hook_demo',
        python_callable=slack_webhook_hook_demo,
        dag=dag)

    first >> second
