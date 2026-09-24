import pandas as pd
import numpy as np
import re


# ==========================================================
# REQUIRED COLUMNS
# ==========================================================

REQUIRED_COLUMNS = [
    "Date",
    "Product",
    "Store",
    "Sales",
    "Revenue",
    "Discount",
    "Holiday"
]


# ==========================================================
# NORMALIZE COLUMN NAME
# ==========================================================

def normalize_column_name(column):

    column = str(column)

    # Remove BOM
    column = column.replace("\ufeff", "")

    # Remove leading/trailing spaces
    column = column.strip()

    # Replace tabs/newlines with spaces
    column = re.sub(
        r"[\t\r\n]+",
        " ",
        column
    )

    # Remove multiple spaces
    column = re.sub(
        r"\s+",
        " ",
        column
    )

    return column


# ==========================================================
# LOAD DATA
# ==========================================================

def load_data(file_path):

    # ------------------------------------------------------
    # First attempt: automatic separator detection
    # ------------------------------------------------------

    try:

        df = pd.read_csv(
            file_path,
            sep=None,
            engine="python",
            encoding="utf-8-sig"
        )

    except Exception:

        df = pd.read_csv(
            file_path,
            encoding="utf-8-sig"
        )

    # ------------------------------------------------------
    # Normalize column names
    # ------------------------------------------------------

    df.columns = [
        normalize_column_name(column)
        for column in df.columns
    ]

    # ------------------------------------------------------
    # Map different possible names
    # ------------------------------------------------------

    column_mapping = {}

    for column in df.columns:

        clean = (
            column
            .strip()
            .lower()
            .replace("_", "")
            .replace("-", "")
            .replace(" ", "")
        )

        if clean == "date":
            column_mapping[column] = "Date"

        elif clean == "product":
            column_mapping[column] = "Product"

        elif clean == "store":
            column_mapping[column] = "Store"

        elif clean == "sales":
            column_mapping[column] = "Sales"

        elif clean == "revenue":
            column_mapping[column] = "Revenue"

        elif clean == "discount":
            column_mapping[column] = "Discount"

        elif clean == "holiday":
            column_mapping[column] = "Holiday"

    df = df.rename(
        columns=column_mapping
    )

    # ------------------------------------------------------
    # Check columns
    # ------------------------------------------------------

    missing_columns = [
        column
        for column in REQUIRED_COLUMNS
        if column not in df.columns
    ]

    # ------------------------------------------------------
    # If normal CSV parsing failed, try common separators
    # ------------------------------------------------------

    if missing_columns:

        separators = [
            ",",
            ";",
            "\t",
            "|"
        ]

        successful_df = None

        for separator in separators:

            try:

                test_df = pd.read_csv(
                    file_path,
                    sep=separator,
                    encoding="utf-8-sig"
                )

                test_df.columns = [
                    normalize_column_name(column)
                    for column in test_df.columns
                ]

                test_mapping = {}

                for column in test_df.columns:

                    clean = (
                        column
                        .strip()
                        .lower()
                        .replace("_", "")
                        .replace("-", "")
                        .replace(" ", "")
                    )

                    if clean == "date":
                        test_mapping[column] = "Date"

                    elif clean == "product":
                        test_mapping[column] = "Product"

                    elif clean == "store":
                        test_mapping[column] = "Store"

                    elif clean == "sales":
                        test_mapping[column] = "Sales"

                    elif clean == "revenue":
                        test_mapping[column] = "Revenue"

                    elif clean == "discount":
                        test_mapping[column] = "Discount"

                    elif clean == "holiday":
                        test_mapping[column] = "Holiday"

                test_df = test_df.rename(
                    columns=test_mapping
                )

                if all(
                    column in test_df.columns
                    for column in REQUIRED_COLUMNS
                ):

                    successful_df = test_df
                    break

            except Exception:
                continue

        if successful_df is not None:

            df = successful_df

        else:

            raise ValueError(
                "Could not detect the required CSV columns.\n\n"
                "Required columns:\n"
                + ", ".join(REQUIRED_COLUMNS)
                + "\n\n"
                "Columns detected:\n"
                + ", ".join(
                    str(column)
                    for column in df.columns
                )
            )

    # ------------------------------------------------------
    # Keep required columns
    # ------------------------------------------------------

    df = df[
        REQUIRED_COLUMNS
    ].copy()

    # ------------------------------------------------------
    # Convert Date
    # ------------------------------------------------------

    df["Date"] = pd.to_datetime(
        df["Date"],
        errors="coerce"
    )

    # ------------------------------------------------------
    # Convert numeric columns
    # ------------------------------------------------------

    numeric_columns = [
        "Sales",
        "Revenue",
        "Discount",
        "Holiday"
    ]

    for column in numeric_columns:

        df[column] = pd.to_numeric(
            df[column],
            errors="coerce"
        )

    # ------------------------------------------------------
    # Clean Product and Store
    # ------------------------------------------------------

    df["Product"] = (
        df["Product"]
        .astype(str)
        .str.strip()
    )

    df["Store"] = (
        df["Store"]
        .astype(str)
        .str.strip()
    )

    # ------------------------------------------------------
    # Remove invalid rows
    # ------------------------------------------------------

    df = df.dropna(
        subset=[
            "Date",
            "Sales"
        ]
    )

    # ------------------------------------------------------
    # Fill missing values
    # ------------------------------------------------------

    df["Revenue"] = (
        df["Revenue"]
        .fillna(0)
    )

    df["Discount"] = (
        df["Discount"]
        .fillna(0)
    )

    df["Holiday"] = (
        df["Holiday"]
        .fillna(0)
    )

    # ------------------------------------------------------
    # Clean numeric values
    # ------------------------------------------------------

    df["Sales"] = (
        df["Sales"]
        .clip(lower=0)
    )

    df["Revenue"] = (
        df["Revenue"]
        .clip(lower=0)
    )

    df["Discount"] = (
        df["Discount"]
        .clip(
            lower=0,
            upper=1
        )
    )

    df["Holiday"] = (
        df["Holiday"]
        .apply(
            lambda x: 1 if x >= 1 else 0
        )
    )

    # ------------------------------------------------------
    # Sort by date
    # ------------------------------------------------------

    df = (
        df
        .sort_values("Date")
        .reset_index(drop=True)
    )

    return df


# ==========================================================
# DAILY DATA
# ==========================================================

def prepare_daily_data(df):

    daily = (
        df.groupby("Date")
        .agg(
            Sales=("Sales", "sum"),
            Revenue=("Revenue", "sum"),
            Discount=("Discount", "mean"),
            Holiday=("Holiday", "max")
        )
        .reset_index()
    )

    return (
        daily
        .sort_values("Date")
        .reset_index(drop=True)
    )


# ==========================================================
# MONTHLY DATA
# ==========================================================

def prepare_monthly_data(df):

    temp = df.copy()

    temp["Month"] = (
        temp["Date"]
        .dt
        .to_period("M")
    )

    monthly = (
        temp.groupby("Month")
        .agg(
            Sales=("Sales", "sum"),
            Revenue=("Revenue", "sum"),
            Discount=("Discount", "mean"),
            Holiday=("Holiday", "sum")
        )
        .reset_index()
    )

    monthly["Date"] = (
        monthly["Month"]
        .dt
        .to_timestamp()
    )

    monthly = monthly.drop(
        columns=["Month"]
    )

    return (
        monthly
        .sort_values("Date")
        .reset_index(drop=True)
    )


# ==========================================================
# YEARLY DATA
# ==========================================================

def prepare_yearly_data(df):

    temp = df.copy()

    temp["Year"] = (
        temp["Date"]
        .dt
        .year
    )

    yearly = (
        temp.groupby("Year")
        .agg(
            Sales=("Sales", "sum"),
            Revenue=("Revenue", "sum"),
            Discount=("Discount", "mean"),
            Holiday=("Holiday", "sum")
        )
        .reset_index()
    )

    return yearly


# ==========================================================
# DATE FEATURES
# ==========================================================

def create_features(df):

    data = df.copy()

    data["Year"] = (
        data["Date"].dt.year
    )

    data["Month"] = (
        data["Date"].dt.month
    )

    data["Day"] = (
        data["Date"].dt.day
    )

    data["DayOfWeek"] = (
        data["Date"].dt.dayofweek
    )

    data["WeekOfYear"] = (
        data["Date"]
        .dt
        .isocalendar()
        .week
        .astype(int)
    )

    data["Quarter"] = (
        data["Date"].dt.quarter
    )

    data["IsWeekend"] = (
        data["DayOfWeek"]
        .isin([5, 6])
        .astype(int)
    )

    return data


# ==========================================================
# LAG FEATURES
# ==========================================================

def create_lag_features(
    df,
    target="Sales"
):

    data = df.copy()

    if target not in data.columns:

        raise ValueError(
            f"Target column '{target}' not found."
        )

    data = (
        data
        .sort_values("Date")
        .reset_index(drop=True)
    )

    data["Lag_1"] = (
        data[target].shift(1)
    )

    data["Lag_7"] = (
        data[target].shift(7)
    )

    data["Lag_14"] = (
        data[target].shift(14)
    )

    data["Lag_30"] = (
        data[target].shift(30)
    )

    data["Rolling_7"] = (
        data[target]
        .rolling(7)
        .mean()
    )

    data["Rolling_30"] = (
        data[target]
        .rolling(30)
        .mean()
    )

    data = data.dropna()

    return (
        data
        .reset_index(drop=True)
    )


# ==========================================================
# PRODUCT SUMMARY
# ==========================================================

def prepare_product_summary(df):

    summary = (
        df.groupby("Product")
        .agg(
            Sales=("Sales", "sum"),
            Revenue=("Revenue", "sum"),
            Average_Discount=(
                "Discount",
                "mean"
            ),
            Transactions=(
                "Sales",
                "count"
            )
        )
        .reset_index()
    )

    return (
        summary
        .sort_values(
            "Sales",
            ascending=False
        )
        .reset_index(drop=True)
    )


# ==========================================================
# STORE SUMMARY
# ==========================================================

def prepare_store_summary(df):

    summary = (
        df.groupby("Store")
        .agg(
            Sales=("Sales", "sum"),
            Revenue=("Revenue", "sum"),
            Average_Discount=(
                "Discount",
                "mean"
            ),
            Transactions=(
                "Sales",
                "count"
            )
        )
        .reset_index()
    )

    return (
        summary
        .sort_values(
            "Sales",
            ascending=False
        )
        .reset_index(drop=True)
    )


# ==========================================================
# HOLIDAY SUMMARY
# ==========================================================

def prepare_holiday_summary(df):

    summary = (
        df.groupby("Holiday")
        .agg(
            Sales=("Sales", "sum"),
            Revenue=("Revenue", "sum"),
            Average_Sales=(
                "Sales",
                "mean"
            ),
            Transactions=(
                "Sales",
                "count"
            )
        )
        .reset_index()
    )

    summary["Holiday_Type"] = (
        summary["Holiday"]
        .map({
            0: "Non-Holiday",
            1: "Holiday"
        })
    )

    return summary


# ==========================================================
# SALES STATISTICS
# ==========================================================

def calculate_sales_statistics(df):

    return {
        "Total Sales": df["Sales"].sum(),
        "Total Revenue": df["Revenue"].sum(),
        "Average Sales": df["Sales"].mean(),
        "Maximum Sales": df["Sales"].max(),
        "Minimum Sales": df["Sales"].min(),
        "Total Transactions": len(df)
    }


# ==========================================================
# FORECASTING DATA
# ==========================================================

def prepare_forecasting_data(df):

    daily = prepare_daily_data(df)

    if daily.empty:
        return daily

    full_dates = pd.date_range(
        start=daily["Date"].min(),
        end=daily["Date"].max(),
        freq="D"
    )

    daily = (
        daily
        .set_index("Date")
        .reindex(full_dates)
    )

    daily.index.name = "Date"

    daily["Sales"] = (
        daily["Sales"].fillna(0)
    )

    daily["Revenue"] = (
        daily["Revenue"].fillna(0)
    )

    daily["Discount"] = (
        daily["Discount"].fillna(0)
    )

    daily["Holiday"] = (
        daily["Holiday"].fillna(0)
    )

    daily = daily.reset_index()

    return daily