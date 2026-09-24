import os
import joblib
import pandas as pd

from sklearn.pipeline import Pipeline

from sklearn.linear_model import LogisticRegression

from sklearn.ensemble import (
    RandomForestClassifier,
    GradientBoostingClassifier
)

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score
)

from xgboost import XGBClassifier


def create_models(preprocessor):

    models = {

        "Logistic Regression": Pipeline(
            steps=[
                (
                    "preprocessor",
                    preprocessor
                ),
                (
                    "classifier",
                    LogisticRegression(
                        max_iter=2000,
                        class_weight="balanced",
                        random_state=42
                    )
                )
            ]
        ),

        "Random Forest": Pipeline(
            steps=[
                (
                    "preprocessor",
                    preprocessor
                ),
                (
                    "classifier",
                    RandomForestClassifier(
                        n_estimators=300,
                        max_depth=12,
                        min_samples_split=5,
                        class_weight="balanced",
                        random_state=42,
                        n_jobs=-1
                    )
                )
            ]
        ),

        "Gradient Boosting": Pipeline(
            steps=[
                (
                    "preprocessor",
                    preprocessor
                ),
                (
                    "classifier",
                    GradientBoostingClassifier(
                        n_estimators=200,
                        learning_rate=0.05,
                        max_depth=3,
                        random_state=42
                    )
                )
            ]
        ),

        "XGBoost": Pipeline(
            steps=[
                (
                    "preprocessor",
                    preprocessor
                ),
                (
                    "classifier",
                    XGBClassifier(
                        n_estimators=300,
                        max_depth=5,
                        learning_rate=0.05,
                        subsample=0.8,
                        colsample_bytree=0.8,
                        eval_metric="logloss",
                        random_state=42
                    )
                )
            ]
        )
    }

    return models


def train_models(
    models,
    X_train,
    y_train,
    X_test,
    y_test
):

    results = []

    trained_models = {}

    for name, model in models.items():

        print(
            f"\nTraining {name}..."
        )

        model.fit(
            X_train,
            y_train
        )

        predictions = model.predict(
            X_test
        )

        probabilities = model.predict_proba(
            X_test
        )[:, 1]

        accuracy = accuracy_score(
            y_test,
            predictions
        )

        precision = precision_score(
            y_test,
            predictions,
            zero_division=0
        )

        recall = recall_score(
            y_test,
            predictions,
            zero_division=0
        )

        f1 = f1_score(
            y_test,
            predictions,
            zero_division=0
        )

        roc_auc = roc_auc_score(
            y_test,
            probabilities
        )

        results.append({

            "Model": name,

            "Accuracy": accuracy,

            "Precision": precision,

            "Recall": recall,

            "F1 Score": f1,

            "ROC-AUC": roc_auc
        })

        trained_models[name] = model

        print(
            f"Accuracy : {accuracy:.4f}"
        )

        print(
            f"Precision: {precision:.4f}"
        )

        print(
            f"Recall   : {recall:.4f}"
        )

        print(
            f"F1 Score : {f1:.4f}"
        )

        print(
            f"ROC-AUC  : {roc_auc:.4f}"
        )

    results_df = pd.DataFrame(
        results
    )

    results_df = results_df.sort_values(
        by="ROC-AUC",
        ascending=False
    ).reset_index(
        drop=True
    )

    return (
        trained_models,
        results_df
    )


def save_best_model(
    trained_models,
    results_df,
    output_path="models/best_model.pkl"
):

    os.makedirs(
        os.path.dirname(output_path),
        exist_ok=True
    )

    best_model_name = (
        results_df.iloc[0]["Model"]
    )

    best_model = (
        trained_models[
            best_model_name
        ]
    )

    joblib.dump(
        best_model,
        output_path
    )

    print(
        f"\nBest model saved: {best_model_name}"
    )

    print(
        f"Location: {output_path}"
    )

    return best_model_name