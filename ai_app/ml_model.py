import joblib
from pathlib import Path
from .models import Player, Team
from .goal_pipeline import GoalPredictionPipeline

# Trick: ánh xạ __main__.GoalPredictionPipeline về đúng class trong goal_pipeline
sys.modules["__main__"] = sys.modules[__name__]
sys.modules["__main__"].GoalPredictionPipeline = GoalPredictionPipeline

MODEL_PATH = Path(__file__).resolve().parent / "goal_prediction_pipeline.pkl"
_model = None

def _load_model():
    global _model
    if _model is None:
        _model = joblib.load(MODEL_PATH)
    return _model
    
def predict(data):
    """
    data is expected to be a dict with keys: player_id, opponent_id, home_team_id
    Example: {"player_id": 18, "opponent_id": 2, "home_team_id": 5}
    """

    # Look up DB entries
    try:
        player = Player.objects.get(id=data["player_id"])
        opponent = Team.objects.get(id=data["opponent_id"])
        home_team = Team.objects.get(id=data["home_team_id"])
    except (Player.DoesNotExist, Team.DoesNotExist) as e:
        raise ValueError(f"Invalid input IDs: {e}")

    # Load model and predict
    model = _load_model()
    result = [model.predict(player.name, opponent.name, home_team.name)]  # wrap in list for single sample
    try:
        return result.tolist()
    except Exception:
        return list(result)
