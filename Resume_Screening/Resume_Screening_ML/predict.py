import os
import joblib

from preprocessing import clean_text


MODEL_PATH = "models/resume_model.pkl"


def load_model():

    if not os.path.exists(MODEL_PATH):

        raise FileNotFoundError(
            "Trained model does not exist.\n"
            "Run: python train_model.py"
        )

    return joblib.load(MODEL_PATH)


def prepare_resume(
    resume_text,
    skills="",
    experience="",
    education=""
):

    combined = (
        str(resume_text) + " "
        + str(skills) + " "
        + str(experience) + " "
        + str(education)
    )

    return clean_text(combined)


def predict_resume(
    resume_text,
    skills="",
    experience="",
    education=""
):

    model = load_model()

    text = prepare_resume(
        resume_text,
        skills,
        experience,
        education
    )

    prediction = model.predict([text])

    return prediction[0]


def predict_with_confidence(
    resume_text,
    skills="",
    experience="",
    education=""
):

    model = load_model()

    text = prepare_resume(
        resume_text,
        skills,
        experience,
        education
    )

    prediction = model.predict([text])[0]

    confidence = None

    # Logistic Regression / Naive Bayes
    if hasattr(model, "predict_proba"):

        probabilities = model.predict_proba(
            [text]
        )[0]

        confidence = max(
            probabilities
        ) * 100

    # Linear SVM
    elif hasattr(model, "decision_function"):

        scores = model.decision_function(
            [text]
        )

        if len(scores.shape) == 1:

            confidence = 100 * (
                1 / (
                    1 + __import__(
                        "math"
                    ).exp(-abs(scores[0]))
                )
            )

        else:

            confidence = 100 * (
                abs(scores).max()
                / (abs(scores).sum() + 1e-9)
            )

    if confidence is not None:

        confidence = min(
            max(confidence, 0),
            100
        )

    return prediction, confidence


if __name__ == "__main__":

    try:

        result = predict_resume(
            "Python machine learning "
            "pandas numpy scikit learn "
            "data analysis predictive modeling",

            "Python, Machine Learning, Pandas, SQL",

            "2 years",

            "B.Tech Computer Science"
        )

        print(
            "Predicted Category:",
            result
        )

    except Exception as error:

        print(
            "Prediction Error:",
            error
        )