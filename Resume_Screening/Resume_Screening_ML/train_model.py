import os
import joblib
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score
)

from preprocessing import load_data, prepare_text


DATASET = "data/resume_dataset.csv"
MODEL_FILE = "models/resume_model.pkl"
METRICS_FILE = "outputs/metrics.csv"


print("=" * 60)
print("RESUME SCREENING ML TRAINING")
print("=" * 60)

# ------------------------------------------------------------
# 1. CREATE FOLDERS
# ------------------------------------------------------------

print("\n[1] Creating folders...")

os.makedirs("models", exist_ok=True)
os.makedirs("outputs", exist_ok=True)

print("Folders ready.")


# ------------------------------------------------------------
# 2. LOAD DATASET
# ------------------------------------------------------------

print("\n[2] Loading dataset...")

df = load_data(DATASET)

print("Dataset loaded successfully.")
print("Rows:", len(df))
print("Columns:", df.columns.tolist())


# ------------------------------------------------------------
# 3. SHOW CATEGORIES
# ------------------------------------------------------------

print("\n[3] Job categories:")

print(
    df["Job Category"].value_counts()
)


# ------------------------------------------------------------
# 4. PREPARE TEXT
# ------------------------------------------------------------

print("\n[4] Preparing NLP text...")

X, y = prepare_text(df)

print("Text preprocessing complete.")
print("Documents:", len(X))


# ------------------------------------------------------------
# 5. TRAIN TEST SPLIT
# ------------------------------------------------------------

print("\n[5] Creating train/test split...")

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.30,
    random_state=42,
    stratify=y
)

print("Training samples:", len(X_train))
print("Testing samples:", len(X_test))


# ------------------------------------------------------------
# 6. CREATE MODEL
# ------------------------------------------------------------

print("\n[6] Creating TF-IDF + Logistic Regression model...")

model = Pipeline([
    (
        "tfidf",
        TfidfVectorizer(
            stop_words="english",
            ngram_range=(1, 2),
            max_features=5000,
            sublinear_tf=True
        )
    ),

    (
        "classifier",
        LogisticRegression(
            max_iter=3000,
            class_weight="balanced"
        )
    )
])

print("Model created.")


# ------------------------------------------------------------
# 7. TRAIN
# ------------------------------------------------------------

print("\n[7] Training model...")
print("Please wait...")

model.fit(
    X_train,
    y_train
)

print("MODEL TRAINING COMPLETE!")


# ------------------------------------------------------------
# 8. PREDICTION
# ------------------------------------------------------------

print("\n[8] Testing model...")

predictions = model.predict(
    X_test
)

print("Prediction complete.")


# ------------------------------------------------------------
# 9. METRICS
# ------------------------------------------------------------

accuracy = accuracy_score(
    y_test,
    predictions
)

precision = precision_score(
    y_test,
    predictions,
    average="weighted",
    zero_division=0
)

recall = recall_score(
    y_test,
    predictions,
    average="weighted",
    zero_division=0
)

f1 = f1_score(
    y_test,
    predictions,
    average="weighted",
    zero_division=0
)


print("\n" + "=" * 60)
print("MODEL PERFORMANCE")
print("=" * 60)

print(
    f"Accuracy  : {accuracy:.4f}"
)

print(
    f"Precision : {precision:.4f}"
)

print(
    f"Recall    : {recall:.4f}"
)

print(
    f"F1 Score  : {f1:.4f}"
)


# ------------------------------------------------------------
# 10. SAVE MODEL
# ------------------------------------------------------------

print("\n[9] Saving model...")

joblib.dump(
    model,
    MODEL_FILE
)

print(
    "Model saved:",
    MODEL_FILE
)


# ------------------------------------------------------------
# 11. SAVE METRICS
# ------------------------------------------------------------

metrics = pd.DataFrame([
    {
        "Model": "Logistic Regression",
        "Accuracy": accuracy,
        "Precision": precision,
        "Recall": recall,
        "F1 Score": f1
    }
])

metrics.to_csv(
    METRICS_FILE,
    index=False
)

print(
    "Metrics saved:",
    METRICS_FILE
)


# ------------------------------------------------------------
# 12. VERIFY MODEL
# ------------------------------------------------------------

print("\n[10] Verifying saved model...")

if os.path.exists(MODEL_FILE):

    size = os.path.getsize(
        MODEL_FILE
    )

    print(
        "SUCCESS: Model file exists."
    )

    print(
        "Model size:",
        size,
        "bytes"
    )

else:

    print(
        "ERROR: Model file was not created."
    )


print("\n" + "=" * 60)
print("TRAINING FINISHED SUCCESSFULLY")
print("=" * 60)