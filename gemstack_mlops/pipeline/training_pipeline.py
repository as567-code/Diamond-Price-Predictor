import os
import sys

from gemstack_mlops.logger import logging
from gemstack_mlops.exception import CustomException
from gemstack_mlops.components.data_ingestion_component import DataIngestion
from gemstack_mlops.components.data_transformation_component import DataTransformation
from gemstack_mlops.components.model_trainer_component import ModelTrainer
from gemstack_mlops.components.model_evaluation_component import ModelEvaluation
from gemstack_mlops.components.data_validation_component import (
    DataValidation,
    DataValidationConfig,
)


obj=DataIngestion()
train_data_path,test_data_path=obj.initiate_data_ingestion()

# Simple schema validation before proceeding
expected_columns = [
    'carat', 'depth', 'table', 'x', 'y', 'z', 'cut', 'color', 'clarity', 'price'
]
validator = DataValidation(config=DataValidationConfig(expected_columns=expected_columns))
ok, msg = validator.initiate_data_validation(train_data_path, test_data_path)
if not ok:
    raise CustomException(f"Data validation failed: {msg}", sys)

data_transformation=DataTransformation()

train_arr,test_arr=data_transformation.initialize_data_transformation(train_data_path,test_data_path)


model_trainer_obj=ModelTrainer()
model_trainer_obj.initate_model_training(train_arr,test_arr)

model_eval_obj = ModelEvaluation()
model_eval_obj.initiate_model_evaluation(train_arr,test_arr)