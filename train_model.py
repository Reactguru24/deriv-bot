import joblib
from sklearn.linear_model import SGDClassifier
from config import MODEL_PATH

# Classes for prediction: 0 = DOWN, 1 = UP
CLASSES = [0, 1]

def initialize_model():
    """
    Load existing model from disk or create a new one if missing/corrupted.
    """
    try:
        model = joblib.load(MODEL_PATH)
        print("[MODEL] Loaded existing model.")
    except (EOFError, FileNotFoundError):
        print("[MODEL] Creating new model...")
        model = SGDClassifier(loss="log_loss")  # Use 'log_loss' for sklearn >=1.3
        # Initialize with dummy data to set classes
        model.partial_fit([[0, 0]], [0], classes=CLASSES)
        joblib.dump(model, MODEL_PATH)
        print(f"[MODEL] New model saved to {MODEL_PATH}")
    return model

def update_model(model, X_new, y_new):
    """
    Incrementally update the model with new data.

    Args:
        model: The SGDClassifier instance.
        X_new: List of feature vectors [[f1, f2, ...], ...].
        y_new: List of corresponding labels [0, 1, ...].
    """
    if not X_new or not y_new:
        print("[MODEL] No new data to update.")
        return model

    model.partial_fit(X_new, y_new, classes=CLASSES)
    joblib.dump(model, MODEL_PATH)
    print(f"[MODEL] Updated model with {len(X_new)} new samples and saved.")
    return model
