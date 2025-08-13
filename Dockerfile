FROM python:3.10-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

COPY requirements.txt /app/requirements.txt
RUN python -m pip install -U pip && pip install -r requirements.txt

COPY src /app/src
COPY templates /app/templates
COPY app.py /app/app.py

EXPOSE 8000

ENV MLFLOW_TRACKING_URI=file:///app/mlruns
CMD ["python", "app.py"]

