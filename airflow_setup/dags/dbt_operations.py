from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import datetime, timedelta
from airflow.operators.docker_operator import DockerOperator

default_args = {
    "owner": "airflow",
    "description": "Use of the DockerOperator",
    "depend_on_past": False,
    "start_date": datetime(2018, 1, 3),
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

with DAG(
    "dbt_dag", default_args=default_args, schedule_interval="5 * * * *", catchup=False,
) as dag:
    t1 = BashOperator(task_id="print_current_date", bash_command="date")

    t2 = DockerOperator(
        task_id="docker_command",
        image="dbt_docker:latest",
        api_version="auto",
        auto_remove=True,
        command="dbt debug",
        docker_url="unix://var/run/docker.sock",
        network_mode="bridge",
        # volumes=[
        #     "/home/airflow/dbt_files:/dbt",
        #     "/home/airflow/dbt_files/profiles.yml:/root/.dbt/profiles.yml",
        # ],
    )

    t3 = BashOperator(task_id="print_hello", bash_command='echo "hello world"')

    t1 >> t2 >> t3
