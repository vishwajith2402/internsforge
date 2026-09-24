import os
import joblib
import pandas as pd


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_DIR = os.path.join(BASE_DIR, "models")


MODEL_FILES = {
    "Logistic Regression": "logistic_regression.joblib",
    "Decision Tree": "decision_tree.joblib",
    "Random Forest": "random_forest.joblib",
    "XGBoost": "xgboost.joblib",
}


def load_model(model_name):
    """Load one trained model."""

    if model_name not in MODEL_FILES:
        raise ValueError(
            f"Unknown model: {model_name}"
        )

    model_path = os.path.join(
        MODEL_DIR,
        MODEL_FILES[model_name]
    )

    if not os.path.exists(model_path):
        raise FileNotFoundError(
            f"Model not found:\n{model_path}\n\n"
            "Run train_models.py first."
        )

    return joblib.load(model_path)


def load_all_models():
    """Load all available models."""

    models = {}

    for name in MODEL_FILES:

        try:
            models[name] = load_model(name)

        except Exception as error:
            print(
                f"Could not load {name}: {error}"
            )

    return models


def load_model_results():
    """Load model evaluation results."""

    results_path = os.path.join(
        MODEL_DIR,
        "model_results.joblib"
    )

    if not os.path.exists(results_path):
        return {}

    try:
        return joblib.load(results_path)

    except Exception as error:
        print(
            f"Could not load model results: {error}"
        )
        return {}


def prepare_input(
    gender,
    married,
    education,
    applicant_income,
    loan_amount,
    credit_history,
    property_area
):
    """Create DataFrame from applicant input."""

    return pd.DataFrame({
        "Gender": [gender],
        "Married": [married],
        "Education": [education],
        "ApplicantIncome": [applicant_income],
        "LoanAmount": [loan_amount],
        "CreditHistory": [credit_history],
        "PropertyArea": [property_area],
    })


def predict_loan(
    gender,
    married,
    education,
    applicant_income,
    loan_amount,
    credit_history,
    property_area,
    model_name="Random Forest"
):
    """Predict loan approval."""

    model = load_model(model_name)

    input_df = prepare_input(
        gender,
        married,
        education,
        applicant_income,
        loan_amount,
        credit_history,
        property_area
    )

    prediction = model.predict(input_df)[0]

    if int(prediction) == 1:
        status = "Approved"
    else:
        status = "Rejected"

    probability = 0.0

    if hasattr(model, "predict_proba"):

        probabilities = model.predict_proba(
            input_df
        )[0]

        probability = float(
            probabilities[1] * 100
        )

    return {
        "prediction": int(prediction),
        "status": status,
        "probability": probability,
        "model": model_name,
    }


def predict_from_dictionary(
    applicant_data,
    model_name="Random Forest"
):
    """Prediction helper for dictionary input."""

    model = load_model(model_name)

    input_df = pd.DataFrame([applicant_data])

    prediction = model.predict(input_df)[0]

    probability = 0.0

    if hasattr(model, "predict_proba"):

        probabilities = model.predict_proba(
            input_df
        )[0]

        probability = float(
            probabilities[1] * 100
        )

    status = (
        "Approved"
        if int(prediction) == 1
        else "Rejected"
    )

    return {
        "prediction": int(prediction),
        "status": status,
        "probability": probability,
        "model": model_name,
    }


def get_available_models():

    available = []

    for name, filename in MODEL_FILES.items():

        path = os.path.join(
            MODEL_DIR,
            filename
        )

        if os.path.exists(path):
            available.append(name)

    return available


def get_best_model():

    results = load_model_results()

    if not results:
        return "Random Forest"

    best_model = "Random Forest"
    best_score = -1

    for name, metrics in results.items():

        if not isinstance(metrics, dict):
            continue

        score = metrics.get(
            "f1",
            metrics.get(
                "F1 Score",
                metrics.get(
                    "accuracy",
                    metrics.get(
                        "Accuracy",
                        0
                    )
                )
            )
        )

        if score > best_score:
            best_score = score
            best_model = name

    return best_model


def get_model_status():

    status = {}

    for name, filename in MODEL_FILES.items():

        path = os.path.join(
            MODEL_DIR,
            filename
        )

        status[name] = os.path.exists(path)

    return status


if __name__ == "__main__":

    print("=" * 60)
    print("LOAN AI - PREDICTION MODULE")
    print("=" * 60)

    print("\nLoaded file:")
    print(__file__)

    print("\nAvailable models:")

    for name, available in get_model_status().items():

        print(
            f"  {name}: "
            f"{'OK' if available else 'MISSING'}"
        )

    print("\nPrediction module loaded successfully.")