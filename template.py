import os
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO, format='[%(asctime)s]: %(message)s:')


list_of_files = [
    "gemstack_mlops/__init__.py",
    "gemstack_mlops/components/__init__.py",
    "gemstack_mlops/components/data_ingestion_component.py",
    "gemstack_mlops/components/data_transformation_component.py",
    "gemstack_mlops/components/data_validation_component.py",
    "gemstack_mlops/components/model_evaluation_component.py",
    "gemstack_mlops/components/model_trainer_component.py",
    "gemstack_mlops/utils/__init__.py",
    "gemstack_mlops/utils/common.py",
    "gemstack_mlops/utils/utils.py",
    "gemstack_mlops/config/__init__.py",
    "gemstack_mlops/logger/logger.py",
    "gemstack_mlops/exception/exception.py",
    "gemstack_mlops/exception/__init__.py",
    "gemstack_mlops/config/configuration.py",
    "gemstack_mlops/pipeline/__init__.py",
    "gemstack_mlops/pipeline/step_01_data_ingestion_pipeline.py",
    "gemstack_mlops/pipeline/step_02_data_validation_pipeline.py",
    "gemstack_mlops/pipeline/step_03_data_transformation_pipeline.py",
    "gemstack_mlops/pipeline/step_04_model_trainer_pipeline.py",
    "gemstack_mlops/pipeline/step_05_model_evaluation_pipeline.py",
    "gemstack_mlops/pipeline/step_06_prediction_pipeline.py",
    "gemstack_mlops/pipeline/prediction_pipeline.py",
    "gemstack_mlops/pipeline/training_pipeline.py",
    "gemstack_mlops/entity/__init__.py",
    "gemstack_mlops/entity/config_entity.py",
    "gemstack_mlops/constants/__init__.py",
    "data/data.txt",
    "config/config.yaml",
    "artifacts/info.txt",
    "test/__init__.py",
    "airflow/dags/batch_prediction.py",
    "airflow/dags/training_pipeline.py",
    "params.yaml",
    "schema.yaml",
    "main.py",
    "app.py",
    "start.sh",
    "dvc.yaml",
    "Dockerfile",
    "docker-compose.yaml",
    "tox.ini",
    "requirements.txt",
    "requirements_dev.txt",
    "setup.py",
    "setup.cfg",
    "research/trials.ipynb",
    "templates/index.html",
    "templates/form.html",
    "templates/result.html",
    "pyproject.toml",
    "init_setup.sh",
    ".github/workflows/.gitkeep"


]



for filepath in list_of_files:
    filepath = Path(filepath)

    filedir, filename = os.path.split(filepath)

    if filedir !="":
        os.makedirs(filedir, exist_ok=True)
        logging.info(f"Creating directory; {filedir} for the file: {filename}")

    if (not os.path.exists(filepath)) or (os.path.getsize(filepath) == 0):
        with open(filepath, "w") as f:
            pass
            logging.info(f"Creating empty file: {filepath}")


    else:
        logging.info(f"{filename} is already exists")