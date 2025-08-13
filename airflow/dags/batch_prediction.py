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
    dag_id="mlops_batch_prediction",
    default_args=default_args,
    start_date=datetime(2025, 1, 1),
    schedule_interval=None,
    catchup=False,
    tags=["mlops", "batch"],
):
    input_path = os.path.abspath("artifacts/test.csv")
    output_path = os.path.abspath("artifacts/predictions.csv")
    cmd = (
        "PYTHONPATH=src python - << 'PY'\n"
        "from src.pipeline.prediction_pipeline import PredictPipeline\n"
        "import pandas as pd\n"
        f"df = pd.read_csv(r'{input_path}')\n"
        "X = df.drop(columns=['price', 'id'], errors='ignore')\n"
        "preds = PredictPipeline().predict(X)\n"
        f"pd.DataFrame({{'prediction': preds}}).to_csv(r'{output_path}', index=False)\n"
        "print('Saved predictions to', r'" + output_path + "')\n"
        "PY"
    )
    batch_predict = BashOperator(
        task_id="batch_predict",
        bash_command=cmd,
        env={"MLFLOW_TRACKING_URI": f"file://{os.path.abspath('mlruns')}"},
    )
