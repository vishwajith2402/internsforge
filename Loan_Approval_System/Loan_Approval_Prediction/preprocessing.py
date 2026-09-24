# ============================================================
# preprocessing.py
# Loan Approval Prediction System
# ============================================================

import re
import numpy as np
import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import (
    OneHotEncoder,
    StandardScaler
)


# ============================================================
# PROJECT CONFIGURATION
# ============================================================

TARGET = "LoanStatus"

FEATURES = [
    "Gender",
    "Married",
    "Education",
    "ApplicantIncome",
    "LoanAmount",
    "CreditHistory",
    "PropertyArea",
]

CATEGORICAL_FEATURES = [
    "Gender",
    "Married",
    "Education",
    "PropertyArea",
]

NUMERICAL_FEATURES = [
    "ApplicantIncome",
    "LoanAmount",
    "CreditHistory",
]


# ============================================================
# NORMALIZE COLUMN NAMES
# ============================================================

def normalize_column_name(column):

    original = str(column).strip()

    # Remove accidental markdown
    original = original.replace(
        "```csv",
        ""
    )

    original = original.replace(
        "```",
        ""
    )

    original = original.strip()

    # Convert to comparison key
    key = re.sub(
        r"[^a-z0-9]",
        "",
        original.lower()
    )

    mapping = {

        # Gender
        "gender":
            "Gender",

        # Married
        "married":
            "Married",

        "maritalstatus":
            "Married",

        # Education
        "education":
            "Education",

        # Income
        "applicantincome":
            "ApplicantIncome",

        "applicantincomeinr":
            "ApplicantIncome",

        "income":
            "ApplicantIncome",

        # Loan amount
        "loanamount":
            "LoanAmount",

        "loanamountinr":
            "LoanAmount",

        "loan":
            "LoanAmount",

        # Credit
        "credithistory":
            "CreditHistory",

        "credit":
            "CreditHistory",

        # Property
        "propertyarea":
            "PropertyArea",

        "property":
            "PropertyArea",

        # Target
        "loanstatus":
            "LoanStatus",

        "loanapproval":
            "LoanStatus",

        "approval":
            "LoanStatus",

        "status":
            "LoanStatus",

        # ID
        "loanid":
            "Loan_ID",

        "id":
            "Loan_ID",
    }

    return mapping.get(
        key,
        original
    )


# ============================================================
# CLEAN COLUMN NAMES
# ============================================================

def clean_columns(df):

    df = df.copy()

    # Remove completely empty columns
    df = df.dropna(
        axis=1,
        how="all"
    )

    df.columns = [
        normalize_column_name(column)
        for column in df.columns
    ]

    # Remove duplicate columns
    df = df.loc[
        :,
        ~df.columns.duplicated()
    ]

    return df


# ============================================================
# LOAD DATASET
# ============================================================

def load_data(file_path):

    df = pd.read_csv(
        file_path
    )

    df = clean_columns(
        df
    )

    # Remove ID
    if "Loan_ID" in df.columns:

        df = df.drop(
            columns=["Loan_ID"]
        )

    return df


# ============================================================
# CLEAN LOAN STATUS
# ============================================================

def clean_target(df):

    df = df.copy()

    if TARGET not in df.columns:

        raise ValueError(
            "LoanStatus column was not found.\n\n"
            f"Available columns: "
            f"{list(df.columns)}"
        )

    def convert_status(value):

        if pd.isna(value):
            return np.nan

        value = str(
            value
        ).strip().lower()

        approved_values = [
            "y",
            "yes",
            "approved",
            "approve",
            "1",
            "true",
        ]

        rejected_values = [
            "n",
            "no",
            "rejected",
            "reject",
            "0",
            "false",
        ]

        if value in approved_values:
            return 1

        if value in rejected_values:
            return 0

        return np.nan

    df[TARGET] = (
        df[TARGET]
        .apply(convert_status)
    )

    # Remove rows where target couldn't be understood
    df = df.dropna(
        subset=[TARGET]
    )

    df[TARGET] = (
        df[TARGET]
        .astype(int)
    )

    return df


# ============================================================
# CLEAN FEATURES
# ============================================================

def clean_features(df):

    df = df.copy()

    # Create missing expected columns
    # if they don't exist.
    for column in FEATURES:

        if column not in df.columns:

            df[column] = np.nan

    # Numeric columns
    for column in NUMERICAL_FEATURES:

        df[column] = pd.to_numeric(
            df[column],
            errors="coerce"
        )

    # Categorical columns
    for column in CATEGORICAL_FEATURES:

        df[column] = (
            df[column]
            .astype("string")
            .str.strip()
        )

        df[column] = (
            df[column]
            .replace(
                {
                    "":
                        np.nan,

                    "nan":
                        np.nan,

                    "None":
                        np.nan,

                    "null":
                        np.nan,
                }
            )
        )

    return df


# ============================================================
# COMPLETE DATASET PREPARATION
# ============================================================

def prepare_dataset(df):

    # Step 1
    df = clean_columns(
        df
    )

    # Step 2
    if TARGET in df.columns:

        df = clean_target(
            df
        )

    # Step 3
    df = clean_features(
        df
    )

    return df


# ============================================================
# CREATE ML PREPROCESSOR
# ============================================================

def create_preprocessor():

    # Numerical preprocessing
    numerical_pipeline = Pipeline(
        steps=[

            (
                "imputer",

                SimpleImputer(
                    strategy="median"
                )
            ),

            (
                "scaler",

                StandardScaler()
            ),
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
                    handle_unknown="ignore"
                )
            ),
        ]
    )

    preprocessor = ColumnTransformer(
        transformers=[

            (
                "numeric",

                numerical_pipeline,

                NUMERICAL_FEATURES
            ),

            (
                "categorical",

                categorical_pipeline,

                CATEGORICAL_FEATURES
            ),
        ]
    )

    return preprocessor


# ============================================================
# PREPARE PREDICTION INPUT
# ============================================================

def prepare_prediction_input(
    data
):

    if isinstance(
        data,
        dict
    ):

        df = pd.DataFrame(
            [data]
        )

    elif isinstance(
        data,
        pd.DataFrame
    ):

        df = data.copy()

    else:

        raise TypeError(
            "Prediction input must be "
            "a dictionary or DataFrame."
        )

    df = clean_columns(
        df
    )

    # Make sure all features exist
    for column in FEATURES:

        if column not in df.columns:

            df[column] = np.nan

    return df[
        FEATURES
    ]


# ============================================================
# DATASET VALIDATION
# ============================================================

def validate_dataset(df):

    errors = []

    # Check target
    if TARGET not in df.columns:

        errors.append(
            f"Missing target column: {TARGET}"
        )

    # Check features
    for feature in FEATURES:

        if feature not in df.columns:

            errors.append(
                f"Missing feature: {feature}"
            )

    if len(df) == 0:

        errors.append(
            "Dataset contains no rows."
        )

    return errors


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    print("=" * 60)
    print("LOAN AI - PREPROCESSING MODULE")
    print("=" * 60)

    print("\nTarget:")
    print(TARGET)

    print("\nFeatures:")

    for feature in FEATURES:
        print(
            f"  - {feature}"
        )

    print("\nCategorical features:")

    for feature in CATEGORICAL_FEATURES:
        print(
            f"  - {feature}"
        )

    print("\nNumerical features:")

    for feature in NUMERICAL_FEATURES:
        print(
            f"  - {feature}"
        )

    print(
        "\nPreprocessing module loaded successfully."
    )