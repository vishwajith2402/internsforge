import numpy as np
import pandas as pd


def churn_summary(data):
    """
    Calculate overall customer churn statistics.
    """

    if "Churn" not in data.columns:
        return {}

    churn_values = (
        data["Churn"]
        .astype(str)
        .str.strip()
        .str.lower()
    )

    churned = (churn_values == "yes").sum()
    retained = (churn_values == "no").sum()

    total = churned + retained

    churn_percentage = (
        (churned / total) * 100
        if total > 0
        else 0
    )

    retention_percentage = (
        (retained / total) * 100
        if total > 0
        else 0
    )

    return {
        "total_customers": total,
        "churned_customers": churned,
        "retained_customers": retained,
        "churn_percentage": churn_percentage,
        "retention_percentage": retention_percentage
    }


def get_feature_importance(model):
    """
    Extract feature importance from the trained model.
    Works with tree models and Logistic Regression.
    """

    if model is None:
        return pd.DataFrame()

    try:

        preprocessor = model.named_steps[
            "preprocessor"
        ]

        classifier = model.named_steps[
            "classifier"
        ]

        feature_names = (
            preprocessor
            .get_feature_names_out()
        )

        # Tree-based models
        if hasattr(
            classifier,
            "feature_importances_"
        ):

            importance = (
                classifier
                .feature_importances_
            )

        # Logistic Regression
        elif hasattr(
            classifier,
            "coef_"
        ):

            importance = np.abs(
                classifier.coef_[0]
            )

        else:

            return pd.DataFrame()

        feature_df = pd.DataFrame({
            "Feature": feature_names,
            "Importance": importance
        })

        feature_df = feature_df.sort_values(
            by="Importance",
            ascending=False
        )

        feature_df = feature_df.reset_index(
            drop=True
        )

        return feature_df

    except Exception as error:

        print(
            f"Feature importance error: {error}"
        )

        return pd.DataFrame()


def get_top_features(
    feature_df,
    number_of_features=10
):
    """
    Return the most important features.
    """

    if feature_df.empty:
        return pd.DataFrame()

    return feature_df.head(
        number_of_features
    )


def customer_risk(probability):
    """
    Convert churn probability into a business risk category.
    """

    if probability >= 0.75:

        return "VERY HIGH RISK"

    elif probability >= 0.50:

        return "HIGH RISK"

    elif probability >= 0.30:

        return "MEDIUM RISK"

    else:

        return "LOW RISK"


def risk_color(risk):
    """
    Return a UI-friendly color based on risk.
    """

    colors = {
        "VERY HIGH RISK": "#EF4444",
        "HIGH RISK": "#F97316",
        "MEDIUM RISK": "#F59E0B",
        "LOW RISK": "#22C55E"
    }

    return colors.get(
        risk,
        "#94A3B8"
    )


def generate_business_recommendation(
    probability,
    customer_data
):
    """
    Generate a simple business recommendation
    based on predicted churn probability.
    """

    recommendations = []

    if probability >= 0.75:

        recommendations.append(
            "Immediate retention action recommended."
        )

        recommendations.append(
            "Consider a personalized retention offer."
        )

    elif probability >= 0.50:

        recommendations.append(
            "Customer should be monitored closely."
        )

        recommendations.append(
            "Consider loyalty incentives."
        )

    elif probability >= 0.30:

        recommendations.append(
            "Customer has moderate churn risk."
        )

        recommendations.append(
            "Monitor usage and satisfaction."
        )

    else:

        recommendations.append(
            "Customer currently has low churn risk."
        )

        recommendations.append(
            "Continue normal customer engagement."
        )

    # Contract recommendation
    contract = str(
        customer_data.get(
            "Contract Type",
            ""
        )
    ).lower()

    if "month" in contract:

        recommendations.append(
            "Consider encouraging a longer-term contract."
        )

    # Monthly charge recommendation
    try:

        monthly_charge = float(
            customer_data.get(
                "Monthly Charges",
                0
            )
        )

        if monthly_charge > 80:

            recommendations.append(
                "Consider reviewing pricing or offering a discount."
            )

    except (ValueError, TypeError):

        pass

    return recommendations