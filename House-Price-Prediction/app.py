import os
import joblib
import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="House Price AI",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# PATHS
# ============================================================

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

DATA_FILE = os.path.join(
    BASE_DIR,
    "house_prices.csv"
)

MODEL_FILE = os.path.join(
    BASE_DIR,
    "models",
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
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    .stApp {
        background-color: #070b14;
    }

    .block-container {
        max-width: 1400px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    section[data-testid="stSidebar"] {
        background-color: #0b1120;
        border-right: 1px solid #1e293b;
    }

    div[data-testid="stMetric"] {
        background-color: #0f172a;
        border: 1px solid #263449;
        border-radius: 14px;
        padding: 18px;
    }

    .stButton > button {
        width: 100%;
        min-height: 48px;
        border-radius: 10px;
        border: 0;
        font-weight: 700;
        color: white;
        background: linear-gradient(
            90deg,
            #6d28d9,
            #0891b2
        );
    }

    .stButton > button:hover {
        background: linear-gradient(
            90deg,
            #7c3aed,
            #06b6d4
        );
        color: white;
    }

    div[data-baseweb="select"] > div {
        background-color: #111827;
        border-radius: 10px;
    }

    .stNumberInput input {
        background-color: #111827;
        color: white;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# PRICE FORMATTERS
# ============================================================

def format_currency(value):

    try:
        value = float(value)
    except:
        return "₹0"

    return f"₹{value:,.0f}"


def format_price(value):

    try:
        value = float(value)
    except:
        return "₹0"

    if value >= 1_00_00_000:

        return (
            f"₹{value / 1_00_00_000:.2f} Crore"
        )

    if value >= 1_00_000:

        return (
            f"₹{value / 1_00_000:.2f} Lakh"
        )

    if value >= 1_000:

        return (
            f"₹{value / 1_000:.2f} Thousand"
        )

    return format_currency(value)


# ============================================================
# CHECK REQUIRED FILES
# ============================================================

if not os.path.exists(DATA_FILE):

    st.error(
        "❌ house_prices.csv not found."
    )

    st.stop()


if not os.path.exists(MODEL_FILE):

    st.error(
        "❌ Trained model not found."
    )

    st.info(
        "Run train_model.py first."
    )

    st.stop()


# ============================================================
# LOAD DATA
# ============================================================

try:

    df = pd.read_csv(
        DATA_FILE
    )

    df.columns = (
        df.columns
        .astype(str)
        .str.strip()
    )

except Exception as error:

    st.error(
        "❌ Could not load dataset."
    )

    st.exception(error)

    st.stop()


# ============================================================
# LOAD MODEL
# ============================================================

try:

    model = joblib.load(
        MODEL_FILE
    )

except Exception as error:

    st.error(
        "❌ Could not load model."
    )

    st.exception(error)

    st.stop()


# ============================================================
# LOAD TRAINING OUTPUTS
# ============================================================

results = None
prediction_df = None
feature_df = None


if os.path.exists(RESULT_FILE):

    try:

        results = pd.read_csv(
            RESULT_FILE
        )

    except:

        pass


if os.path.exists(PREDICTION_FILE):

    try:

        prediction_df = pd.read_csv(
            PREDICTION_FILE
        )

    except:

        pass


if os.path.exists(FEATURE_FILE):

    try:

        feature_df = pd.read_csv(
            FEATURE_FILE
        )

    except:

        pass


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.title("🏠 House Price AI")

    st.caption(
        "ML Internship Project"
    )

    st.divider()

    page = st.radio(
        "Navigation",
        [
            "🏠 Price Predictor",
            "📊 Dataset Analytics",
            "🤖 Model Performance",
            "🎯 Actual vs Predicted",
            "💡 Feature Importance",
            "📋 Dataset",
            "ℹ️ About"
        ]
    )

    st.divider()

    st.caption(
        "Python • Scikit-learn • Streamlit • Plotly"
    )


# ============================================================
# HEADER
# ============================================================

st.title(
    "🏠 House Price AI"
)

st.subheader(
    "Intelligent House Price Prediction & Analytics Platform"
)

st.caption(
    "Machine Learning based real-estate price estimation system"
)

st.divider()


# ============================================================
# PRICE PREDICTOR
# ============================================================

if page == "🏠 Price Predictor":

    st.header(
        "🏠 House Price Predictor"
    )

    st.write(
        "Enter property details to estimate the "
        "market value using Machine Learning."
    )

    st.divider()

    col1, col2 = st.columns(2)

    # --------------------------------------------------------
    # PROPERTY DETAILS
    # --------------------------------------------------------

    with col1:

        st.subheader(
            "📋 Property Details"
        )

        area = st.number_input(
            "📐 Area (sq ft)",
            min_value=100.0,
            max_value=100000.0,
            value=1500.0,
            step=50.0
        )

        bedrooms = st.number_input(
            "🛏 Bedrooms",
            min_value=1,
            max_value=20,
            value=3
        )

        bathrooms = st.number_input(
            "🚿 Bathrooms",
            min_value=1,
            max_value=20,
            value=2
        )

    # --------------------------------------------------------
    # LOCATION
    # --------------------------------------------------------

    with col2:

        st.subheader(
            "📍 Location Details"
        )

        if "Location" in df.columns:

            cities = sorted(
                df["Location"]
                .dropna()
                .astype(str)
                .str.strip()
                .unique()
                .tolist()
            )

        else:

            cities = [
                "Chennai",
                "Bangalore",
                "Hyderabad",
                "Mumbai",
                "Delhi"
            ]

        location = st.selectbox(
            "📍 Select City",
            cities
        )

        property_age = st.number_input(
            "🏗 Property Age (years)",
            min_value=0,
            max_value=200,
            value=5
        )

    st.write("")

    predict_button = st.button(
        "🔮 CALCULATE HOUSE PRICE"
    )

    # --------------------------------------------------------
    # PREDICTION
    # --------------------------------------------------------

    if predict_button:

        input_data = pd.DataFrame(
            {
                "Area": [area],
                "Bedrooms": [bedrooms],
                "Bathrooms": [bathrooms],
                "Location": [location],
                "Property Age": [property_age]
            }
        )

        try:

            prediction = model.predict(
                input_data
            )[0]

            prediction = max(
                float(prediction),
                0
            )

        except Exception as error:

            st.error(
                "❌ Prediction failed."
            )

            st.exception(error)

            st.stop()

        readable_price = format_price(
            prediction
        )

        exact_price = format_currency(
            prediction
        )

        price_per_sqft = (
            prediction / area
        )

        # ----------------------------------------------------
        # RESULT
        # ----------------------------------------------------

        st.divider()

        st.header(
            "💰 Estimated House Price"
        )

        # IMPORTANT:
        # Native Streamlit components.
        # No HTML.
        # No <div>.
        # No unsafe_allow_html.

        result_col1, result_col2, result_col3 = st.columns(
            [1, 1.5, 1]
        )

        with result_col1:

            st.metric(
                "Estimated Market Value",
                readable_price
            )

        with result_col2:

            st.metric(
                "Exact Predicted Price",
                exact_price
            )

        with result_col3:

            st.metric(
                "Price / sq ft",
                format_currency(
                    price_per_sqft
                )
            )

        st.success(
            f"🏠 Estimated value for a "
            f"{area:,.0f} sq ft property in "
            f"{location}: {readable_price}"
        )

        # ----------------------------------------------------
        # PROPERTY SUMMARY
        # ----------------------------------------------------

        st.divider()

        st.subheader(
            "📊 Property Summary"
        )

        c1, c2, c3, c4, c5 = st.columns(5)

        c1.metric(
            "Area",
            f"{area:,.0f} sq ft"
        )

        c2.metric(
            "Bedrooms",
            bedrooms
        )

        c3.metric(
            "Bathrooms",
            bathrooms
        )

        c4.metric(
            "City",
            location
        )

        c5.metric(
            "Property Age",
            f"{property_age} years"
        )

        # ----------------------------------------------------
        # DOWNLOAD
        # ----------------------------------------------------

        prediction_result = pd.DataFrame(
            {
                "Area": [area],
                "Bedrooms": [bedrooms],
                "Bathrooms": [bathrooms],
                "Location": [location],
                "Property Age": [property_age],
                "Predicted Price": [prediction],
                "Formatted Price": [readable_price],
                "Price Per Sq Ft": [price_per_sqft]
            }
        )

        st.download_button(
            "📥 Download Prediction",
            prediction_result.to_csv(
                index=False
            ),
            "house_price_prediction.csv",
            "text/csv"
        )


# ============================================================
# DATASET ANALYTICS
# ============================================================

elif page == "📊 Dataset Analytics":

    st.header(
        "📊 Dataset Analytics Dashboard"
    )

    st.write(
        "Explore the historical real-estate dataset."
    )

    st.divider()

    total_properties = len(df)

    total_cities = (
        df["Location"].nunique()
        if "Location" in df.columns
        else 0
    )

    average_price = (
        df["Price"].mean()
        if "Price" in df.columns
        else 0
    )

    median_price = (
        df["Price"].median()
        if "Price" in df.columns
        else 0
    )

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "🏠 Properties",
        f"{total_properties:,}"
    )

    c2.metric(
        "📍 Cities",
        total_cities
    )

    c3.metric(
        "💰 Average Price",
        format_price(
            average_price
        )
    )

    c4.metric(
        "📊 Median Price",
        format_price(
            median_price
        )
    )

    st.divider()

    # --------------------------------------------------------
    # PRICE DISTRIBUTION
    # --------------------------------------------------------

    if "Price" in df.columns:

        col1, col2 = st.columns(2)

        with col1:

            fig = px.histogram(
                df,
                x="Price",
                nbins=30,
                title="House Price Distribution"
            )

            fig.update_layout(
                template="plotly_dark"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        with col2:

            if "Location" in df.columns:

                city_prices = (
                    df.groupby(
                        "Location"
                    )["Price"]
                    .mean()
                    .reset_index()
                    .sort_values(
                        "Price",
                        ascending=False
                    )
                )

                fig = px.bar(
                    city_prices,
                    x="Location",
                    y="Price",
                    title="Average Price by City"
                )

                fig.update_layout(
                    template="plotly_dark"
                )

                st.plotly_chart(
                    fig,
                    use_container_width=True
                )

        # ----------------------------------------------------
        # AREA VS PRICE
        # ----------------------------------------------------

        if "Area" in df.columns:

            st.subheader(
                "📐 Area vs Price"
            )

            # NO trendline.
            # This avoids statsmodels completely.

            fig = px.scatter(
                df,
                x="Area",
                y="Price",
                color=(
                    "Location"
                    if "Location" in df.columns
                    else None
                ),
                title="Area vs House Price"
            )

            fig.update_layout(
                template="plotly_dark"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        # ----------------------------------------------------
        # BEDROOMS
        # ----------------------------------------------------

        if "Bedrooms" in df.columns:

            bedroom_prices = (
                df.groupby(
                    "Bedrooms"
                )["Price"]
                .mean()
                .reset_index()
            )

            fig = px.bar(
                bedroom_prices,
                x="Bedrooms",
                y="Price",
                title="Average Price by Bedrooms"
            )

            fig.update_layout(
                template="plotly_dark"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )


# ============================================================
# MODEL PERFORMANCE
# ============================================================

elif page == "🤖 Model Performance":

    st.header(
        "🤖 Model Performance"
    )

    if results is None:

        st.warning(
            "Model evaluation data is unavailable."
        )

        st.info(
            "Run train_model.py again."
        )

    else:

        st.dataframe(
            results,
            use_container_width=True,
            hide_index=True
        )

        if "R2 Score" in results.columns:

            best = (
                results
                .sort_values(
                    "R2 Score",
                    ascending=False
                )
                .iloc[0]
            )

            st.success(
                f"🏆 Best Model: {best['Model']} | "
                f"R² Score: {best['R2 Score']:.4f}"
            )

            fig = px.bar(
                results,
                x="Model",
                y="R2 Score",
                title="R² Score Comparison",
                text_auto=".3f"
            )

            fig.update_layout(
                template="plotly_dark"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        if "RMSE" in results.columns:

            fig = px.bar(
                results,
                x="Model",
                y="RMSE",
                title="RMSE Comparison",
                text_auto=".2f"
            )

            fig.update_layout(
                template="plotly_dark"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )


# ============================================================
# ACTUAL VS PREDICTED
# ============================================================

elif page == "🎯 Actual vs Predicted":

    st.header(
        "🎯 Actual vs Predicted Price"
    )

    if prediction_df is None:

        st.warning(
            "Actual vs Predicted data is unavailable."
        )

        st.info(
            "Run train_model.py again to generate it."
        )

    else:

        actual = prediction_df[
            "Actual Price"
        ]

        predicted = prediction_df[
            "Predicted Price"
        ]

        minimum = min(
            actual.min(),
            predicted.min()
        )

        maximum = max(
            actual.max(),
            predicted.max()
        )

        fig = px.scatter(
            prediction_df,
            x="Actual Price",
            y="Predicted Price",
            title="Actual vs Predicted House Prices"
        )

        fig.add_trace(
            go.Scatter(
                x=[
                    minimum,
                    maximum
                ],
                y=[
                    minimum,
                    maximum
                ],
                mode="lines",
                name="Perfect Prediction"
            )
        )

        fig.update_layout(
            template="plotly_dark",
            xaxis_title="Actual Price (₹)",
            yaxis_title="Predicted Price (₹)"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        st.info(
            "Points closer to the diagonal line "
            "represent more accurate predictions."
        )

        st.subheader(
            "Prediction Records"
        )

        st.dataframe(
            prediction_df,
            use_container_width=True,
            hide_index=True
        )


# ============================================================
# FEATURE IMPORTANCE
# ============================================================

elif page == "💡 Feature Importance":

    st.header(
        "💡 Feature Importance"
    )

    if feature_df is None:

        st.warning(
            "Feature importance data is unavailable."
        )

        st.info(
            "Run train_model.py again to generate it."
        )

    else:

        if (
            "Feature" in feature_df.columns
            and
            "Importance" in feature_df.columns
        ):

            feature_df = (
                feature_df
                .sort_values(
                    "Importance",
                    ascending=False
                )
            )

            fig = px.bar(
                feature_df,
                x="Importance",
                y="Feature",
                orientation="h",
                title="Feature Importance"
            )

            fig.update_layout(
                template="plotly_dark"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

            st.subheader(
                "Feature Importance Data"
            )

            st.dataframe(
                feature_df,
                use_container_width=True,
                hide_index=True
            )


# ============================================================
# DATASET
# ============================================================

elif page == "📋 Dataset":

    st.header(
        "📋 Dataset Explorer"
    )

    c1, c2 = st.columns(2)

    c1.metric(
        "Rows",
        f"{len(df):,}"
    )

    c2.metric(
        "Columns",
        len(df.columns)
    )

    st.divider()

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )

    st.divider()

    st.subheader(
        "📈 Statistical Summary"
    )

    st.dataframe(
        df.describe(
            include="all"
        ),
        use_container_width=True
    )


# ============================================================
# ABOUT
# ============================================================

elif page == "ℹ️ About":

    st.header(
        "ℹ️ About House Price AI"
    )

    st.write(
        "House Price AI is a supervised Machine Learning "
        "regression project developed for real-estate "
        "price estimation."
    )

    st.divider()

    col1, col2 = st.columns(2)

    with col1:

        st.subheader(
            "🎯 Objective"
        )

        st.write(
            "Predict the approximate market value of a "
            "house using historical property data."
        )

        st.subheader(
            "📥 Input Features"
        )

        st.write(
            """
            • Area  
            • Bedrooms  
            • Bathrooms  
            • Location  
            • Property Age
            """
        )

    with col2:

        st.subheader(
            "🤖 Algorithms"
        )

        st.write(
            """
            • Linear Regression  
            • Decision Tree Regressor  
            • Random Forest Regressor
            """
        )

        st.subheader(
            "📊 Evaluation Metrics"
        )

        st.write(
            """
            • MAE  
            • MSE  
            • RMSE  
            • R² Score
            """
        )

    st.divider()

    st.subheader(
        "🛠 Technology Stack"
    )

    st.write(
        "Python • Pandas • NumPy • Scikit-learn • "
        "Streamlit • Plotly • Joblib"
    )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "🏠 House Price AI • Machine Learning Internship Project"
)