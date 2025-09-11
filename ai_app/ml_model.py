import joblib
from pathlib import Path

MODEL_PATH = Path(__file__).resolve().parent / "goal_prediction_pipeline.pkl"
_model = None

def _load_model():
    global _model
    if _model is None:
        _model = joblib.load(MODEL_PATH)
    return _model

def predict(data):
    model = _load_model()
    # if isinstance(data, dict):
    #     values = [data[k] for k in sorted(data.keys())]
    #     X = [values]
    # elif isinstance(data, list):
    #     if len(data) > 0 and isinstance(data[0], (list, tuple)):
    #         X = data
    #     else:
    #         X = [data]
    # else:
    #     X = [[data]]
    result = [model.predict(data)]
    try:
        return result.tolist()
    except Exception:
        return list(result)
