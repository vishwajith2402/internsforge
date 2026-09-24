import os
import joblib
import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline

from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
)

from xgboost import XGBClassifier

from preprocessing import (
    load_data,
    prepare_dataset,
    create_preprocessor,
    FEATURES,
    TARGET,
)


# =========================================================
# CONFIGURATION
# =========================================================

DATA_FILE = "loan_data.csv"
MODEL_DIR = "models"

TEST_SIZE = 0.20
RANDOM_STATE = 42


# =========================================================
# CREATE MODEL DIRECTORY
# =========================================================

os.makedirs(MODEL_DIR, exist_ok=True)


print()
print("=" * 65)
print("                 LOANAI ML TRAINING")
print("=" * 65)
print()


# =========================================================
# LOAD DATASET
# =========================================================

if not os.path.exists(DATA_FILE):

    raise FileNotFoundError(
        f"\nDataset not found: {DATA_FILE}\n"
        "Place loan_data.csv in the project folder."
    )


print("[1/7] Loading dataset...")

df = load_data(DATA_FILE)

print(f"      Original rows: {len(df)}")
print(f"      Original columns: {len(df.columns)}")

print()


# =========================================================
# CLEAN DATA
# =========================================================

print("[2/7] Cleaning dataset...")

df = prepare_dataset(df)

print(f"      Clean rows: {len(df)}")
print(f"      Columns: {list(df.columns)}")

if TARGET not in df.columns:

    raise ValueError(
        f"'{TARGET}' was not found in the dataset.\n"
        f"Available columns: {list(df.columns)}"
    )


# =========================================================
# CHECK TARGET
# =========================================================

print()
print("[3/7] Checking target distribution...")

print(
    df[TARGET]
    .value_counts()
    .sort_index()
)


# =========================================================
# PREPARE X AND Y
# =========================================================

X = df[FEATURES].copy()
y = df[TARGET].copy()


if len(df) < 10:

    raise ValueError(
        "Dataset is too small. Please provide at least 10 rows."
    )


# =========================================================
# TRAIN TEST SPLIT
# =========================================================

print()
print("[4/7] Splitting dataset...")

try:

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=TEST_SIZE,
        random_state=RANDOM_STATE,
        stratify=y,
    )

except ValueError:

    print(
        "      Stratified split unavailable; "
        "using normal split."
    )

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=TEST_SIZE,
        random_state=RANDOM_STATE,
    )


print(f"      Training rows: {len(X_train)}")
print(f"      Testing rows : {len(X_test)}")


# =========================================================
# MODELS
# =========================================================

models = {

    "Logistic Regression":
        LogisticRegression(
            max_iter=2000,
            random_state=RANDOM_STATE,
        ),

    "Decision Tree":
        DecisionTreeClassifier(
            max_depth=6,
            min_samples_split=4,
            random_state=RANDOM_STATE,
        ),

    "Random Forest":
        RandomForestClassifier(
            n_estimators=200,
            max_depth=10,
            min_samples_split=4,
            random_state=RANDOM_STATE,
            n_jobs=-1,
        ),

    "XGBoost":
        XGBClassifier(
            n_estimators=150,
            max_depth=4,
            learning_rate=0.05,
            subsample=0.9,
            colsample_bytree=0.9,
            objective="binary:logistic",
            eval_metric="logloss",
            random_state=RANDOM_STATE,
            n_jobs=2,
        ),
}


# =========================================================
# TRAINING
# =========================================================

print()
print("[5/7] Training models...")
print()

results = {}

best_model_name = None
best_f1 = -1


for model_name, model in models.items():

    print(f"      Training {model_name}...")

    preprocessor = create_preprocessor()

    pipeline = Pipeline(
        steps=[
            (
                "preprocessor",
                preprocessor,
            ),
            (
                "model",
                model,
            ),
        ]
    )

    pipeline.fit(
        X_train,
        y_train,
    )

    predictions = pipeline.predict(X_test)

    accuracy = accuracy_score(
        y_test,
        predictions,
    )

    precision = precision_score(
        y_test,
        predictions,
        zero_division=0,
    )

    recall = recall_score(
        y_test,
        predictions,
        zero_division=0,
    )

    f1 = f1_score(
        y_test,
        predictions,
        zero_division=0,
    )

    cm = confusion_matrix(
        y_test,
        predictions,
        labels=[0, 1],
    )

    results[model_name] = {

        "accuracy": float(accuracy),

        "precision": float(precision),

        "recall": float(recall),

        "f1": float(f1),

        "confusion_matrix": cm.tolist(),
    }

    # Save each model
    safe_name = (
        model_name
        .lower()
        .replace(" ", "_")
    )

    model_path = os.path.join(
        MODEL_DIR,
        f"{safe_name}.joblib",
    )

    joblib.dump(
        pipeline,
        model_path,
    )

    print(
        f"          Accuracy : {accuracy:.4f}"
    )

    print(
        f"          Precision: {precision:.4f}"
    )

    print(
        f"          Recall   : {recall:.4f}"
    )

    print(
        f"          F1 Score : {f1:.4f}"
    )

    print()

    if f1 > best_f1:

        best_f1 = f1
        best_model_name = model_name


# =========================================================
# SAVE MODEL RESULTS
# =========================================================

print("[6/7] Saving model results...")


results_path = os.path.join(
    MODEL_DIR,
    "model_results.joblib",
)

joblib.dump(
    results,
    results_path,
)


# =========================================================
# SAVE TEST PREDICTIONS
# =========================================================

test_output = X_test.copy()

test_output["Actual"] = y_test.values

test_output["Predicted"] = (
    models[best_model_name]
    if False
    else 0
)

# Re-load best model to generate prediction
best_safe_name = (
    best_model_name
    .lower()
    .replace(" ", "_")
)

best_model_path = os.path.join(
    MODEL_DIR,
    f"{best_safe_name}.joblib",
)

best_pipeline = joblib.load(
    best_model_path
)

test_output["Predicted"] = (
    best_pipeline.predict(X_test)
)

test_output["Actual"] = y_test.values


test_output.to_csv(
    os.path.join(
        MODEL_DIR,
        "test_predictions.csv",
    ),
    index=False,
)


# =========================================================
# SAVE CONFIGURATION
# =========================================================

config = {

    "features": FEATURES,

    "target": TARGET,

    "best_model": best_model_name,

    "random_state": RANDOM_STATE,
}

joblib.dump(
    config,
    os.path.join(
        MODEL_DIR,
        "config.joblib",
    ),
)


# =========================================================
# FINAL OUTPUT
# =========================================================

print()
print("[7/7] Training completed!")
print()

print("=" * 65)
print("                    MODEL RESULTS")
print("=" * 65)

for name, result in results.items():

    print()
    print(name)

    print(
        f"  Accuracy : {result['accuracy']:.4f}"
    )

    print(
        f"  Precision: {result['precision']:.4f}"
    )

    print(
        f"  Recall   : {result['recall']:.4f}"
    )

    print(
        f"  F1 Score : {result['f1']:.4f}"
    )


print()
print("=" * 65)
print(
    f"BEST MODEL: {best_model_name}"
)
print("=" * 65)

print()
print("Saved files:")

for file in os.listdir(MODEL_DIR):

    print(
        f"  ✓ {file}"
    )

print()
print("You can now run:")
print()
print("python -m streamlit run app.py")
print()