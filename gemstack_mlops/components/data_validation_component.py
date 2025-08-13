import os
import sys
from dataclasses import dataclass
from typing import List, Tuple

import pandas as pd

from src.logger import logging
from src.exception import CustomException


@dataclass
class DataValidationConfig:
    expected_columns: List[str]


class DataValidation:
    def __init__(self, config: DataValidationConfig):
        self.config = config

    def initiate_data_validation(self, train_path: str, test_path: str) -> Tuple[bool, str]:
        try:
            train_df = pd.read_csv(train_path, nrows=1)
            test_df = pd.read_csv(test_path, nrows=1)

            missing_train = [c for c in self.config.expected_columns if c not in train_df.columns]
            missing_test = [c for c in self.config.expected_columns if c not in test_df.columns]

            if missing_train or missing_test:
                message = f"Missing columns - train: {missing_train}, test: {missing_test}"
                logging.info(message)
                return False, message

            return True, "Schema validated"
        except Exception as e:
            raise CustomException(e, sys)