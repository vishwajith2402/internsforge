import re
import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer


# ============================================================
# REQUIRED DATASET COLUMNS
# ============================================================

REQUIRED_COLUMNS = [
    "Resume Text",
    "Skills",
    "Experience",
    "Education",
    "Job Category"
]


# ============================================================
# CLEAN TEXT
# ============================================================

def clean_text(text):

    if pd.isna(text):
        return ""

    text = str(text)

    # Lowercase
    text = text.lower()

    # Remove email
    text = re.sub(
        r"\S+@\S+",
        " ",
        text
    )

    # Remove URLs
    text = re.sub(
        r"http\S+|www\S+",
        " ",
        text
    )

    # Keep letters, numbers and spaces
    text = re.sub(
        r"[^a-z0-9\s]",
        " ",
        text
    )

    # Remove extra spaces
    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text.strip()


# ============================================================
# LOAD DATASET
# ============================================================

def load_data(file_path):

    print("Loading dataset:", file_path)

    df = pd.read_csv(
        file_path
    )

    print(
        "Dataset loaded:",
        len(df),
        "rows"
    )

    # Check required columns
    missing_columns = [
        column
        for column in REQUIRED_COLUMNS
        if column not in df.columns
    ]

    if missing_columns:

        raise ValueError(
            "Missing columns: "
            + ", ".join(missing_columns)
        )

    # Fill missing values
    for column in REQUIRED_COLUMNS:

        df[column] = (
            df[column]
            .fillna("")
            .astype(str)
        )

    # Remove empty categories
    df = df[
        df["Job Category"].str.strip() != ""
    ]

    df.reset_index(
        drop=True,
        inplace=True
    )

    return df


# ============================================================
# COMBINE RESUME INFORMATION
# ============================================================

def combine_resume_fields(df):

    combined = (
        df["Resume Text"] + " "
        + df["Skills"] + " "
        + df["Experience"] + " "
        + df["Education"]
    )

    combined = combined.apply(
        clean_text
    )

    return combined


# ============================================================
# PREPARE TEXT
# ============================================================

def prepare_text(df):

    X = combine_resume_fields(
        df
    )

    y = df["Job Category"]

    return X, y


# ============================================================
# TF-IDF VECTORIZER
# ============================================================

def create_vectorizer():

    vectorizer = TfidfVectorizer(
        stop_words="english",
        ngram_range=(1, 2),
        max_features=5000,
        sublinear_tf=True
    )

    return vectorizer


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    print("=" * 60)
    print("RESUME SCREENING - PREPROCESSING TEST")
    print("=" * 60)

    try:

        df = load_data(
            "data/resume_dataset.csv"
        )

        X, y = prepare_text(
            df
        )

        print(
            "\nDocuments:",
            len(X)
        )

        print(
            "Categories:",
            y.unique().tolist()
        )

        vectorizer = create_vectorizer()

        matrix = vectorizer.fit_transform(
            X
        )

        print(
            "TF-IDF shape:",
            matrix.shape
        )

        print(
            "\nPREPROCESSING SUCCESSFUL"
        )

    except Exception as error:

        print(
            "\nERROR:",
            error
        )