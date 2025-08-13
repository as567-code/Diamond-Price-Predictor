import os
import sys
from urllib.parse import urlparse

import mlflow
import mlflow.sklearn
import numpy as np
from mlflow.models.signature import infer_signature
from sklearn.metrics import mean_absolute_error, r2_score, mean_squared_error

from src.logger import logging
from src.exception import CustomException
from src.utils.utils import load_object

class ModelEvaluation:
    def __init__(self):
        logging.info("evaluation started")

    def eval_metrics(self, actual, pred):
        rmse = np.sqrt(mean_squared_error(actual, pred))  # RMSE
        mae = mean_absolute_error(actual, pred)  # MAE
        r2 = r2_score(actual, pred)  # R2 value
        logging.info("evaluation metrics captured")
        return rmse, mae, r2

    def initiate_model_evaluation(self, train_array, test_array):
        try:
            X_test, y_test = test_array[:, :-1], test_array[:, -1]

            model_path = os.path.join("artifacts", "model.pkl")
            model = load_object(model_path)

            logging.info("model has been loaded")

            # Ensure a valid local tracking URI (prefer env, else local isolated dir)
            if os.environ.get("MLFLOW_TRACKING_URI"):
                mlflow.set_tracking_uri(os.environ["MLFLOW_TRACKING_URI"])
            else:
                local_uri = f"file://{os.path.abspath('mlruns_local')}"
                mlflow.set_tracking_uri(local_uri)
            tracking_url_type_store = urlparse(mlflow.get_tracking_uri()).scheme

            # Infer the input signature
            input_example = X_test[:5]  # Sample input example (you can adjust based on your data)
            signature = infer_signature(X_test, model.predict(X_test))  # Infer signature from data

            with mlflow.start_run():
                prediction = model.predict(X_test)
                rmse, mae, r2 = self.eval_metrics(y_test, prediction)

                mlflow.log_metric("rmse", rmse)
                mlflow.log_metric("r2", r2)
                mlflow.log_metric("mae", mae)

                # Model registry does not work with file store
                if tracking_url_type_store != "file":
                    # Register the model with signature and input example
                    mlflow.sklearn.log_model(
                        model, 
                        "model", 
                        registered_model_name="ml_model", 
                        input_example=input_example, 
                        signature=signature
                    )
                else:
                    mlflow.sklearn.log_model(
                        model, 
                        "model", 
                        input_example=input_example, 
                        signature=signature
                    )

        except Exception as e:
            raise CustomException(e, sys)
