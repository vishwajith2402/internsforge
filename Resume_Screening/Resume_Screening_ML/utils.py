import os


MODEL_PATH = "models/resume_model.pkl"
METRICS_PATH = "outputs/metrics.csv"


def create_directories():
    """Create required project directories."""

    os.makedirs(
        "data",
        exist_ok=True
    )

    os.makedirs(
        "models",
        exist_ok=True
    )

    os.makedirs(
        "outputs",
        exist_ok=True
    )


def model_exists():
    """Check whether the trained model exists."""

    return os.path.isfile(
        MODEL_PATH
    )


def metrics_exists():
    """Check whether evaluation metrics exist."""

    return os.path.isfile(
        METRICS_PATH
    )


def get_model_path():
    """Return the model path."""

    return MODEL_PATH


def get_metrics_path():
    """Return the metrics path."""

    return METRICS_PATH


if __name__ == "__main__":

    print("=" * 50)
    print("UTILS TEST")
    print("=" * 50)

    create_directories()

    print(
        "Model exists:",
        model_exists()
    )

    print(
        "Metrics exists:",
        metrics_exists()
    )

    print(
        "Model path:",
        get_model_path()
    )

    print(
        "Metrics path:",
        get_metrics_path()
    )

    print("\nUTILS TEST COMPLETE")