import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline


TARGET_COLUMN = "Churn"


def load_data(file_path):

    data = pd.read_csv(
        file_path
    )

    return data


def clean_data(data):

    data = data.copy()

    # Remove duplicate rows
    data = data.drop_duplicates()

    # Convert Total Charges
    if "Total Charges" in data.columns:

        data["Total Charges"] = pd.to_numeric(
            data["Total Charges"],
            errors="coerce"
        )

    # Convert target
    if TARGET_COLUMN in data.columns:

        data[TARGET_COLUMN] = (
            data[TARGET_COLUMN]
            .astype(str)
            .str.strip()
            .str.lower()
            .map({
                "yes": 1,
                "no": 0,
                "1": 1,
                "0": 0
            })
        )

    return data


def prepare_data(data):

    data = clean_data(data)

    if TARGET_COLUMN not in data.columns:

        raise ValueError(
            "Dataset must contain a 'Churn' column."
        )

    data = data.dropna(
        subset=[TARGET_COLUMN]
    )

    # Remove Customer ID
    columns_to_remove = [
        "Customer ID"
    ]

    for column in columns_to_remove:

        if column in data.columns:

            data = data.drop(
                columns=[column]
            )

    X = data.drop(
        columns=[TARGET_COLUMN]
    )

    y = data[TARGET_COLUMN].astype(int)

    numeric_columns = X.select_dtypes(
        include=["int64", "float64"]
    ).columns.tolist()

    categorical_columns = X.select_dtypes(
        include=["object", "category"]
    ).columns.tolist()

    # Numeric preprocessing
    numeric_pipeline = Pipeline(
        steps=[
            (
                "imputer",
                SimpleImputer(
                    strategy="median"
                )
            )
        ]
    )

    # Categorical preprocessing
    categorical_pipeline = Pipeline(
        steps=[
            (
                "imputer",
                SimpleImputer(
                    strategy="most_frequent"
                )
            ),
            (
                "encoder",
                OneHotEncoder(
                    handle_unknown="ignore",
                    sparse_output=False
                )
            )
        ]
    )

    preprocessor = ColumnTransformer(
        transformers=[
            (
                "numeric",
                numeric_pipeline,
                numeric_columns
            ),
            (
                "categorical",
                categorical_pipeline,
                categorical_columns
            )
        ]
    )

    X_train, X_test, y_train, y_test = train_test_split(

        X,
        y,

        test_size=0.20,

        random_state=42,

        stratify=y
    )

    return (
        X_train,
        X_test,
        y_train,
        y_test,
        preprocessor,
        numeric_columns,
        categorical_columns
    )