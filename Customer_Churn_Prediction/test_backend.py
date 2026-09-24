from preprocessing import (
    load_data,
    prepare_data
)

from models import (
    create_models,
    train_models,
    save_best_model
)

from analysis import (
    churn_summary,
    get_feature_importance,
    get_top_features
)

from visualization import (
    plot_churn_distribution,
    plot_model_comparison,
    plot_feature_importance
)


DATA_PATH = "data/customer_churn.csv"


print("=" * 60)
print("CUSTOMER CHURN ML BACKEND TEST")
print("=" * 60)


# ---------------------------------------------------------
# LOAD DATA
# ---------------------------------------------------------

print("\n[1] Loading dataset...")

data = load_data(
    DATA_PATH
)

print(
    f"Dataset shape: {data.shape}"
)


# ---------------------------------------------------------
# CHURN ANALYSIS
# ---------------------------------------------------------

print("\n[2] Churn analysis...")

summary = churn_summary(
    data
)

print(
    f"Total customers : {summary['total_customers']}"
)

print(
    f"Churned         : {summary['churned_customers']}"
)

print(
    f"Retained        : {summary['retained_customers']}"
)

print(
    f"Churn rate      : "
    f"{summary['churn_percentage']:.2f}%"
)

print(
    f"Retention rate  : "
    f"{summary['retention_percentage']:.2f}%"
)


# ---------------------------------------------------------
# PREPROCESSING
# ---------------------------------------------------------

print("\n[3] Preparing data...")

(
    X_train,
    X_test,
    y_train,
    y_test,
    preprocessor,
    numeric_columns,
    categorical_columns
) = prepare_data(
    data
)

print(
    f"Training samples : {len(X_train)}"
)

print(
    f"Testing samples  : {len(X_test)}"
)

print(
    f"Numeric features : {numeric_columns}"
)

print(
    f"Categorical      : {categorical_columns}"
)


# ---------------------------------------------------------
# TRAIN MODELS
# ---------------------------------------------------------

print("\n[4] Training models...")

models = create_models(
    preprocessor
)

(
    trained_models,
    results_df
) = train_models(
    models,
    X_train,
    y_train,
    X_test,
    y_test
)


# ---------------------------------------------------------
# MODEL RESULTS
# ---------------------------------------------------------

print("\n[5] MODEL COMPARISON")
print("-" * 60)

print(
    results_df.to_string(
        index=False
    )
)


# ---------------------------------------------------------
# SAVE BEST MODEL
# ---------------------------------------------------------

print("\n[6] Saving best model...")

best_model_name = save_best_model(
    trained_models,
    results_df
)

print(
    f"Best model: {best_model_name}"
)


# ---------------------------------------------------------
# FEATURE IMPORTANCE
# ---------------------------------------------------------

print("\n[7] Feature importance...")

best_model = trained_models[
    best_model_name
]

feature_df = get_feature_importance(
    best_model
)

print(
    feature_df.head(15).to_string(
        index=False
    )
)


# ---------------------------------------------------------
# SAVE OUTPUTS
# ---------------------------------------------------------

print("\n[8] Saving analysis outputs...")

results_df.to_csv(
    "outputs/model_comparison.csv",
    index=False
)

feature_df.to_csv(
    "outputs/feature_importance.csv",
    index=False
)


# ---------------------------------------------------------
# COMPLETE
# ---------------------------------------------------------

print("\n" + "=" * 60)
print("BACKEND TEST COMPLETED SUCCESSFULLY")
print("=" * 60)

print(
    "\nGenerated files:"
)

print(
    " - models/best_model.pkl"
)

print(
    " - outputs/model_comparison.csv"
)

print(
    " - outputs/feature_importance.csv"
)