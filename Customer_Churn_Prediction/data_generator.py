import os
import random
import numpy as np
import pandas as pd


def generate_customer_data(
    number_of_customers=2000,
    output_path="data/customer_churn.csv"
):
    random.seed(42)
    np.random.seed(42)

    os.makedirs(
        os.path.dirname(output_path),
        exist_ok=True
    )

    customer_ids = [
        f"CUST{str(i).zfill(5)}"
        for i in range(1, number_of_customers + 1)
    ]

    gender = np.random.choice(
        ["Male", "Female"],
        number_of_customers
    )

    tenure = np.random.randint(
        1,
        73,
        number_of_customers
    )

    monthly_charges = np.round(
        np.random.uniform(
            20,
            120,
            number_of_customers
        ),
        2
    )

    contract_type = np.random.choice(
        [
            "Month-to-month",
            "One year",
            "Two year"
        ],
        number_of_customers,
        p=[0.55, 0.25, 0.20]
    )

    internet_service = np.random.choice(
        [
            "DSL",
            "Fiber optic",
            "No"
        ],
        number_of_customers,
        p=[0.35, 0.50, 0.15]
    )

    payment_method = np.random.choice(
        [
            "Electronic check",
            "Mailed check",
            "Bank transfer",
            "Credit card"
        ],
        number_of_customers,
        p=[0.35, 0.20, 0.25, 0.20]
    )

    total_charges = np.round(
        monthly_charges * tenure
        + np.random.normal(
            0,
            100,
            number_of_customers
        ),
        2
    )

    total_charges = np.maximum(
        total_charges,
        monthly_charges
    )

    # -----------------------------------------
    # CREATE CHURN PROBABILITY
    # -----------------------------------------

    churn_score = np.zeros(
        number_of_customers
    )

    # Contract effect
    churn_score += np.where(
        contract_type == "Month-to-month",
        0.30,
        0
    )

    churn_score += np.where(
        contract_type == "One year",
        -0.10,
        0
    )

    churn_score += np.where(
        contract_type == "Two year",
        -0.25,
        0
    )

    # Tenure effect
    churn_score += np.where(
        tenure < 12,
        0.25,
        0
    )

    churn_score += np.where(
        tenure > 48,
        -0.15,
        0
    )

    # Monthly charge effect
    churn_score += np.where(
        monthly_charges > 80,
        0.15,
        0
    )

    # Internet service effect
    churn_score += np.where(
        internet_service == "Fiber optic",
        0.10,
        0
    )

    # Payment method effect
    churn_score += np.where(
        payment_method == "Electronic check",
        0.12,
        0
    )

    churn_score += np.random.normal(
        0,
        0.10,
        number_of_customers
    )

    churn_probability = np.clip(
        churn_score,
        0.02,
        0.90
    )

    churn = np.where(
        np.random.random(
            number_of_customers
        ) < churn_probability,
        "Yes",
        "No"
    )

    data = pd.DataFrame({

        "Customer ID": customer_ids,

        "Gender": gender,

        "Tenure": tenure,

        "Monthly Charges": monthly_charges,

        "Total Charges": total_charges,

        "Contract Type": contract_type,

        "Internet Service": internet_service,

        "Payment Method": payment_method,

        "Churn": churn
    })

    # -----------------------------------------
    # ADD SOME MISSING VALUES
    # -----------------------------------------

    missing_indices = np.random.choice(
        number_of_customers,
        30,
        replace=False
    )

    data.loc[
        missing_indices[:10],
        "Total Charges"
    ] = np.nan

    data.loc[
        missing_indices[10:20],
        "Internet Service"
    ] = np.nan

    data.loc[
        missing_indices[20:],
        "Payment Method"
    ] = np.nan

    data.to_csv(
        output_path,
        index=False
    )

    print("=" * 50)
    print("CUSTOMER CHURN DATASET CREATED")
    print("=" * 50)
    print(f"File       : {output_path}")
    print(f"Customers  : {len(data)}")
    print(f"Columns    : {len(data.columns)}")
    print("=" * 50)

    print("\nChurn Distribution:")
    print(data["Churn"].value_counts())

    return data


if __name__ == "__main__":
    generate_customer_data()