import os
import sys
from dataclasses import dataclass
from pathlib import Path

import pandas as pd
from sklearn.model_selection import train_test_split

from src.logger import logging
from src.exception import CustomException

# Optional dependencies used dynamically if available
try:
    import yaml  # type: ignore
except Exception:  # pragma: no cover - safe fallback if yaml isn't available
    yaml = None
try:
    import seaborn as sns  # type: ignore
except Exception:  # pragma: no cover
    sns = None


@dataclass
class DataIngestionConfig:
    raw_data_path:str=os.path.join("artifacts","raw.csv")
    train_data_path:str=os.path.join("artifacts","train.csv")
    test_data_path:str=os.path.join("artifacts","test.csv")

class DataIngestion:
    def __init__(self):
        self.ingestion_config=DataIngestionConfig()

    def initiate_data_ingestion(self):
        logging.info("data ingestion started")
        try:
            # Load configuration if present
            cfg = {}
            cfg_path = os.path.join("config", "config.yaml")
            if os.path.exists(cfg_path) and yaml is not None:
                try:
                    with open(cfg_path, "r") as f:
                        cfg = yaml.safe_load(f) or {}
                except Exception:
                    logging.info("config.yaml present but could not be parsed; proceeding with defaults")

            ingestion_params = (cfg.get("data_ingestion") or {}) if isinstance(cfg, dict) else {}
            source = (ingestion_params.get("source") or "seaborn").lower()
            dataset = ingestion_params.get("dataset") or "diamonds"
            url = ingestion_params.get("url")

            # Choose data source with robust defaults
            if url:
                data = pd.read_csv(url)
                logging.info("Loaded dataset from provided URL in config.yaml")
            elif source == "seaborn" and sns is not None:
                data = sns.load_dataset(dataset)
                logging.info(f"Loaded seaborn dataset: {dataset}")
            else:
                # Fallback to bundled artifacts if available
                fallback_raw = self.ingestion_config.raw_data_path
                if os.path.exists(fallback_raw):
                    data = pd.read_csv(fallback_raw)
                    logging.info("Loaded fallback artifacts/raw.csv")
                else:
                    raise CustomException(
                        f"No valid data source available. Provide config.data_ingestion.url or install seaborn.",
                        sys,
                    )

            os.makedirs(os.path.dirname(os.path.join(self.ingestion_config.raw_data_path)),exist_ok=True)
            data.to_csv(self.ingestion_config.raw_data_path,index=False)
            logging.info(" i have saved the raw dataset in artifact folder")
            
            logging.info("here i have performed train test split")
            
            test_size = float(ingestion_params.get("test_size", 0.25))
            random_state = ingestion_params.get("random_state")
            train_data,test_data=train_test_split(data,test_size=test_size, random_state=random_state)
            logging.info("train test split completed")
            
            train_data.to_csv(self.ingestion_config.train_data_path,index=False)
            test_data.to_csv(self.ingestion_config.test_data_path,index=False)
            
            logging.info("data ingestion part completed")
            
            return (
                 
                
                self.ingestion_config.train_data_path,
                self.ingestion_config.test_data_path
            )
        except Exception as e:
            logging.info("Data ingestion stopped")
            raise CustomException(e,sys)
        

if __name__=="__main__":
    obj=DataIngestion()

    obj.initiate_data_ingestion()