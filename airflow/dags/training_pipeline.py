from datetime import datetime
import os

from airflow import DAG
from airflow.operators.bash import BashOperator

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "retries": 0,
}

with DAG(
    dag_id="mlops_training_pipeline",
    default_args=default_args,
    start_date=datetime(2025, 1, 1),
    schedule_interval=None,
    catchup=False,
    tags=["mlops", "training"],
):
    # ensure PYTHONPATH for package imports
    cmd = "PYTHONPATH=src python -m src.pipeline.training_pipeline"
    train = BashOperator(
        task_id="train_pipeline",
        bash_command=cmd,
        env={"MLFLOW_TRACKING_URI": f"file://{os.path.abspath('mlruns')}"},
    )
