#!/bin/bash

# Diamond Price Predictor MLOps Environment Setup
# Author: Diamond Price Predictor Team

log() {
    echo "[$(date)]: $1"
}

if [ -z "$1" ]; then
    log "Error: No environment name provided."
    log "Usage: ./init_setup.sh <env_name>"
    exit 1
fi

ENV_NAME="$1"
ENV_PATH="./envs/$ENV_NAME"

log "Setting up Gemstack MLOps environment: $ENV_NAME"

if [ -d "$ENV_PATH" ]; then
    log "Environment '$ENV_NAME' already exists. Activating..."
else
    log "Creating environment '$ENV_NAME' with Python 3.10..."
    conda create --prefix "$ENV_PATH" python=3.10 -y
fi

log "Activating conda environment..."
source activate "$ENV_PATH"

if [ -f requirements.txt ]; then
    log "Installing project dependencies..."
    pip install -r requirements.txt
else
    log "Warning: requirements.txt not found."
fi

log "Diamond Price Predictor environment setup complete!"
log "Run: PYTHONPATH=. python -m gemstack_mlops.pipeline.training_pipeline"