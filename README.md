# Gemstack MLOps

**Opinionated MLOps template with MLflow, DVC, Airflow, and Flask**

A production-ready template for machine learning projects featuring:
- 🔬 **MLflow** for experiment tracking and model registry
- 📊 **DVC** for data versioning and pipeline orchestration
- 🔄 **Airflow** for workflow orchestration
- 🌐 **Flask** for model serving with a web UI
- 🐳 **Docker** for containerization
- ✅ **GitHub Actions** for CI/CD

## Quick Start

1. **Install dependencies:**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Configure your data source** in `config/config.yaml`:
   ```yaml
   data_ingestion:
     source: seaborn  # or provide url
     dataset: diamonds
     test_size: 0.25
     random_state: 42
   ```

3. **Run the training pipeline:**
   ```bash
   MLFLOW_TRACKING_URI=file://$PWD/mlruns PYTHONPATH=. python -m gemstack_mlops.pipeline.training_pipeline
   ```

4. **Start the web app:**
   ```bash
   PYTHONPATH=. python app.py
   ```
   Open http://localhost:8000

## Architecture

```
gemstack_mlops/
├── components/           # ML pipeline components
│   ├── data_ingestion_component.py
│   ├── data_transformation_component.py
│   ├── data_validation_component.py
│   ├── model_trainer_component.py
│   └── model_evaluation_component.py
├── pipeline/            # Orchestration pipelines
│   ├── training_pipeline.py
│   └── prediction_pipeline.py
└── utils/              # Shared utilities
```

## Features

- **Config-driven**: Swap datasets via YAML config
- **Modular components**: Data ingestion, transformation, training, evaluation
- **Schema validation**: Automated data quality checks
- **Hyperparameter tuning**: Built-in RandomizedSearchCV
- **Experiment tracking**: MLflow integration with model signatures
- **Web interface**: Flask UI for predictions
- **Containerized**: Docker and docker-compose ready
- **CI/CD**: GitHub Actions workflow

## Usage

### Training
```bash
# Via DVC
dvc repro

# Direct execution
PYTHONPATH=. python -m gemstack_mlops.pipeline.training_pipeline
```

### Prediction
```bash
# Web UI
python app.py

# Programmatic
from gemstack_mlops.pipeline.prediction_pipeline import PredictPipeline
pipeline = PredictPipeline()
predictions = pipeline.predict(your_dataframe)
```

### Docker
```bash
docker-compose up --build
```

### Airflow
```bash
# Place DAGs in your Airflow environment
cp airflow/dags/* $AIRFLOW_HOME/dags/
```

## Development

Install development dependencies:
```bash
pip install -r requirements_dev.txt
pre-commit install
```

Run tests:
```bash
pytest
```

## License

MIT License - see LICENSE file for details.

---

**Built with ❤️ by Aditya Swaroop**