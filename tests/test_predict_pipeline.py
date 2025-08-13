import pandas as pd

from gemstack_mlops.pipeline.prediction_pipeline import PredictPipeline


def test_predict_smoke():
    X = pd.DataFrame({
        'carat': [0.5],
        'depth': [60.0],
        'table': [55.0],
        'x': [5.0],
        'y': [5.0],
        'z': [3.1],
        'cut': ['Ideal'],
        'color': ['G'],
        'clarity': ['VS2']
    })
    try:
        _ = PredictPipeline()
    except Exception:
        # instantiation does not fail
        assert False

