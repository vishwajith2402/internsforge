print("==============================================")
print(" HOUSE PRICE AI - MODEL TRAINING")
print("==============================================")

import os
import warnings

warnings.filterwarnings("ignore")

import joblib
import numpy as np
import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score
)
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
from sklearn.tree import DecisionTreeRegressor


# ============================================================
# PATHS
# ============================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATA_FILE = os.path.join(
    BASE_DIR,
    "house_prices.csv"
)

MODEL_DIR = os.path.join(
    BASE_DIR,
    "models"
)

MODEL_FILE = os.path.join(
    MODEL_DIR,
    "best_model.pkl"
)

RESULT_FILE = os.path.join(
    BASE_DIR,
    "model_results.csv"
)

PREDICTION_FILE = os.path.join(
    BASE_DIR,
    "actual_vs_predicted.csv"
)

FEATURE_FILE = os.path.join(
    BASE_DIR,
    "feature_importance.csv"
)


# ============================================================
# CREATE MODEL DIRECTORY
# ============================================================

os.makedirs(
    MODEL_DIR,
    exist_ok=True
)


# ============================================================
# LOAD DATASET
# ============================================================

def load_dataset():

    print("\n[1/7] Loading dataset...")

    if not os.path.exists(DATA_FILE):

        raise FileNotFoundError(
            f"Dataset not found:\n{DATA_FILE}"
        )

    df = pd.read_csv(DATA_FILE)

    print(
        f"Dataset loaded successfully: "
        f"{df.shape[0]} rows, {df.shape[1]} columns"
    )

    return df


# ============================================================
# CLEAN DATA
# ============================================================

def clean_dataset(df):

    print("\n[2/7] Cleaning dataset...")

    df = df.copy()

    # Remove extra spaces from column names
    df.columns = (
        df.columns
        .astype(str)
        .str.strip()
    )

    required_columns = [
        "Area",
        "Bedrooms",
        "Bathrooms",
        "Location",
        "Property Age",
        "Price"
    ]

    missing_columns = [
        col
        for col in required_columns
        if col not in df.columns
    ]

    if missing_columns:

        raise ValueError(
            "Missing required columns: "
            + ", ".join(missing_columns)
        )

    # Numeric columns
    numeric_columns = [
        "Area",
        "Bedrooms",
        "Bathrooms",
        "Property Age",
        "Price"
    ]

    for col in numeric_columns:

        df[col] = pd.to_numeric(
            df[col],
            errors="coerce"
        )

    # Location
    df["Location"] = (
        df["Location"]
        .astype(str)
        .str.strip()
    )

    # Remove invalid values
    df = df.dropna(
        subset=required_columns
    )

    df = df[
        (df["Area"] > 0)
        & (df["Bedrooms"] > 0)
        & (df["Bathrooms"] > 0)
        & (df["Property Age"] >= 0)
        & (df["Price"] > 0)
    ]

    # Remove duplicate records
    df = df.drop_duplicates()

    print(
        f"Clean dataset: "
        f"{df.shape[0]} rows"
    )

    return df


# ============================================================
# BUILD PREPROCESSOR
# ============================================================

def create_preprocessor():

    numeric_features = [
        "Area",
        "Bedrooms",
        "Bathrooms",
        "Property Age"
    ]

    categorical_features = [
        "Location"
    ]

    preprocessor = ColumnTransformer(
        transformers=[

            (
                "numeric",
                "passthrough",
                numeric_features
            ),

            (
                "location",
                OneHotEncoder(
                    handle_unknown="ignore",
                    sparse_output=False
                ),
                categorical_features
            )
        ]
    )

    return preprocessor


# ============================================================
# TRAIN MODELS
# ============================================================

def train_models():

    # --------------------------------------------------------
    # LOAD
    # --------------------------------------------------------

    df = load_dataset()

    # --------------------------------------------------------
    # CLEAN
    # --------------------------------------------------------

    df = clean_dataset(df)

    # --------------------------------------------------------
    # FEATURES
    # --------------------------------------------------------

    print("\n[3/7] Preparing features...")

    feature_columns = [
        "Area",
        "Bedrooms",
        "Bathrooms",
        "Location",
        "Property Age"
    ]

    target_column = "Price"

    X = df[feature_columns]

    y = df[target_column]

    # --------------------------------------------------------
    # TRAIN TEST SPLIT
    # --------------------------------------------------------

    print("\n[4/7] Splitting dataset...")

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.20,
        random_state=42
    )

    print(
        f"Training records: {len(X_train)}"
    )

    print(
        f"Testing records: {len(X_test)}"
    )

    # --------------------------------------------------------
    # PREPROCESSOR
    # --------------------------------------------------------

    preprocessor = create_preprocessor()

    # --------------------------------------------------------
    # MODELS
    # --------------------------------------------------------

    models = {

        "Linear Regression":
            LinearRegression(),

        "Decision Tree":
            DecisionTreeRegressor(
                random_state=42,
                max_depth=12,
                min_samples_split=4
            ),

        "Random Forest":
            RandomForestRegressor(
                n_estimators=300,
                random_state=42,
                max_depth=15,
                min_samples_split=2,
                n_jobs=-1
            )
    }

    results = []

    trained_models = {}

    # --------------------------------------------------------
    # TRAIN
    # --------------------------------------------------------

    print("\n[5/7] Training models...")

    for model_name, model in models.items():

        print(
            f"\nTraining: {model_name}"
        )

        pipeline = Pipeline(
            steps=[
                (
                    "preprocessor",
                    preprocessor
                ),
                (
                    "model",
                    model
                )
            ]
        )

        pipeline.fit(
            X_train,
            y_train
        )

        predictions = pipeline.predict(
            X_test
        )

        mae = mean_absolute_error(
            y_test,
            predictions
        )

        mse = mean_squared_error(
            y_test,
            predictions
        )

        rmse = np.sqrt(mse)

        r2 = r2_score(
            y_test,
            predictions
        )

        print(
            f"MAE  : {mae:,.2f}"
        )

        print(
            f"MSE  : {mse:,.2f}"
        )

        print(
            f"RMSE : {rmse:,.2f}"
        )

        print(
            f"R2   : {r2:.4f}"
        )

        results.append(
            {
                "Model": model_name,
                "MAE": mae,
                "MSE": mse,
                "RMSE": rmse,
                "R2 Score": r2
            }
        )

        trained_models[
            model_name
        ] = pipeline

    # --------------------------------------------------------
    # RESULTS
    # --------------------------------------------------------

    print("\n[6/7] Selecting best model...")

    results_df = pd.DataFrame(
        results
    )

    results_df = results_df.sort_values(
        by="R2 Score",
        ascending=False
    ).reset_index(drop=True)

    results_df.to_csv(
        RESULT_FILE,
        index=False
    )

    best_model_name = results_df.iloc[0][
        "Model"
    ]

    best_model = trained_models[
        best_model_name
    ]

    print(
        f"\nBEST MODEL: {best_model_name}"
    )

    # --------------------------------------------------------
    # SAVE MODEL
    # --------------------------------------------------------

    joblib.dump(
        best_model,
        MODEL_FILE
    )

    # --------------------------------------------------------
    # ACTUAL VS PREDICTED
    # --------------------------------------------------------

    best_predictions = best_model.predict(
        X_test
    )

    prediction_output = pd.DataFrame(
        {
            "Actual Price": y_test.values,
            "Predicted Price": best_predictions
        }
    )

    prediction_output[
        "Absolute Error"
    ] = abs(
        prediction_output["Actual Price"]
        -
        prediction_output["Predicted Price"]
    )

    prediction_output.to_csv(
        PREDICTION_FILE,
        index=False
    )

    # --------------------------------------------------------
    # FEATURE IMPORTANCE
    # --------------------------------------------------------

    print(
        "\nGenerating feature importance..."
    )

    model_inside = best_model.named_steps[
        "model"
    ]

    preprocessor_inside = best_model.named_steps[
        "preprocessor"
    ]

    feature_names = (
        preprocessor_inside
        .get_feature_names_out()
    )

    importance_values = None

    if hasattr(
        model_inside,
        "feature_importances_"
    ):

        importance_values = (
            model_inside
            .feature_importances_
        )

    elif hasattr(
        model_inside,
        "coef_"
    ):

        importance_values = abs(
            model_inside.coef_
        )

    if importance_values is not None:

        feature_importance = pd.DataFrame(
            {
                "Feature": feature_names,
                "Importance": importance_values
            }
        )

        feature_importance[
            "Feature"
        ] = (
            feature_importance["Feature"]
            .str.replace(
                "numeric__",
                "",
                regex=False
            )
            .str.replace(
                "location__",
                "Location: ",
                regex=False
            )
        )

        feature_importance = (
            feature_importance
            .sort_values(
                "Importance",
                ascending=False
            )
            .reset_index(drop=True)
        )

        feature_importance.to_csv(
            FEATURE_FILE,
            index=False
        )

    # --------------------------------------------------------
    # FINISHED
    # --------------------------------------------------------

    print("\n==============================================")
    print(" TRAINING COMPLETED SUCCESSFULLY")
    print("==============================================")

    print(
        f"\nBest Model: {best_model_name}"
    )

    print(
        f"R2 Score: "
        f"{results_df.iloc[0]['R2 Score']:.4f}"
    )

    print("\nGenerated files:")

    print(
        f"✓ {MODEL_FILE}"
    )

    print(
        f"✓ {RESULT_FILE}"
    )

    print(
        f"✓ {PREDICTION_FILE}"
    )

    print(
        f"✓ {FEATURE_FILE}"
    )


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":

    try:

        train_models()

    except Exception as error:

        print("\n❌ TRAINING FAILED")
        print(
            f"\nError: {error}"
        )

        import traceback

        traceback.print_exc()