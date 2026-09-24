import matplotlib.pyplot as plt


def plot_churn_distribution(data):

    plt.figure(
        figsize=(8, 5)
    )

    churn_counts = (
        data["Churn"]
        .astype(str)
        .str.strip()
        .str.title()
        .value_counts()
    )

    plt.bar(
        churn_counts.index,
        churn_counts.values
    )

    plt.title(
        "Customer Churn Distribution",
        fontsize=15,
        fontweight="bold"
    )

    plt.xlabel(
        "Customer Status"
    )

    plt.ylabel(
        "Number of Customers"
    )

    plt.tight_layout()

    plt.show()


def plot_model_comparison(
    results_df
):

    plt.figure(
        figsize=(10, 5)
    )

    plt.bar(
        results_df["Model"],
        results_df["ROC-AUC"]
    )

    plt.title(
        "Model ROC-AUC Comparison",
        fontsize=15,
        fontweight="bold"
    )

    plt.xlabel(
        "Machine Learning Model"
    )

    plt.ylabel(
        "ROC-AUC Score"
    )

    plt.ylim(
        0,
        1
    )

    plt.xticks(
        rotation=20
    )

    plt.tight_layout()

    plt.show()


def plot_all_metrics(
    results_df
):

    metrics = [
        "Accuracy",
        "Precision",
        "Recall",
        "F1 Score",
        "ROC-AUC"
    ]

    for metric in metrics:

        plt.figure(
            figsize=(10, 5)
        )

        plt.bar(
            results_df["Model"],
            results_df[metric]
        )

        plt.title(
            f"Model {metric} Comparison",
            fontsize=15,
            fontweight="bold"
        )

        plt.xlabel(
            "Model"
        )

        plt.ylabel(
            metric
        )

        plt.ylim(
            0,
            1
        )

        plt.xticks(
            rotation=20
        )

        plt.tight_layout()

        plt.show()


def plot_feature_importance(
    feature_df,
    top_n=15
):

    if feature_df.empty:

        print(
            "No feature importance available."
        )

        return

    top_features = (
        feature_df
        .head(top_n)
        .sort_values(
            "Importance"
        )
    )

    plt.figure(
        figsize=(10, 7)
    )

    plt.barh(
        top_features["Feature"],
        top_features["Importance"]
    )

    plt.title(
        "Top Features Affecting Customer Churn",
        fontsize=15,
        fontweight="bold"
    )

    plt.xlabel(
        "Importance"
    )

    plt.ylabel(
        "Feature"
    )

    plt.tight_layout()

    plt.show()