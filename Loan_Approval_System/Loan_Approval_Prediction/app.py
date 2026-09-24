import os
import pandas as pd
import numpy as np
import streamlit as st

from prediction import (
    predict_loan,
    get_available_models,
    load_model_results,
    get_best_model,
)

from preprocessing import (
    load_data,
    prepare_dataset,
    FEATURES,
    TARGET,
)


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="LoanAI | Loan Approval",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded",
)


# =========================================================
# LUXURY UI CSS
# =========================================================

st.markdown(
    """
<style>

@import url(
    'https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap'
);

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {

    background:
        radial-gradient(
            circle at 85% 5%,
            rgba(81, 45, 168, 0.20),
            transparent 28%
        ),
        radial-gradient(
            circle at 10% 20%,
            rgba(0, 188, 212, 0.10),
            transparent 25%
        ),
        linear-gradient(
            135deg,
            #050817 0%,
            #080b1d 48%,
            #0b1026 100%
        );

    color: #f8fafc;
}


/* Remove default top padding */

.block-container {
    padding-top: 1.2rem;
    padding-bottom: 3rem;
    max-width: 1500px;
}


/* Sidebar */

[data-testid="stSidebar"] {

    background:
        linear-gradient(
            180deg,
            #070b1c 0%,
            #0b1028 50%,
            #0a0920 100%
        );

    border-right:
        1px solid rgba(100, 120, 255, 0.20);
}


[data-testid="stSidebar"] * {
    color: #e5e7eb;
}


/* Sidebar logo */

.logo-box {

    padding: 10px 5px 25px 5px;
}

.logo-title {

    font-size: 28px;
    font-weight: 800;

    background:
        linear-gradient(
            90deg,
            #22d3ee,
            #8b5cf6,
            #a78bfa
        );

    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.logo-subtitle {

    color: #94a3b8;
    font-size: 12px;
    margin-top: -5px;
}


/* Sidebar section */

.sidebar-label {

    color: #64748b;
    font-size: 11px;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    font-weight: 700;
    margin: 20px 0 8px 0;
}


/* Header */

.top-header {

    display: flex;
    justify-content: space-between;
    align-items: center;

    margin-bottom: 18px;
}

.welcome {

    color: #94a3b8;
    font-size: 13px;
}

.welcome strong {

    color: #f8fafc;
    font-size: 17px;
}


/* Hero */

.hero {

    position: relative;
    overflow: hidden;

    border-radius: 24px;

    padding: 34px 36px;

    min-height: 250px;

    background:
        radial-gradient(
            circle at 78% 45%,
            rgba(124, 58, 237, 0.42),
            transparent 25%
        ),
        radial-gradient(
            circle at 95% 10%,
            rgba(34, 211, 238, 0.22),
            transparent 24%
        ),
        linear-gradient(
            135deg,
            #0b1735,
            #11152e 55%,
            #18123d
        );

    border:
        1px solid rgba(
            34,
            211,
            238,
            0.45
        );

    box-shadow:
        0 20px 70px
        rgba(0,0,0,0.30);
}


.hero:after {

    content: "";

    position: absolute;

    width: 420px;
    height: 420px;

    right: -160px;
    top: -160px;

    border-radius: 50%;

    background:
        radial-gradient(
            circle,
            rgba(34,211,238,0.18),
            transparent 65%
        );
}


.hero-content {

    position: relative;
    z-index: 2;

    max-width: 650px;
}


.hero-title {

    font-size: 42px;
    line-height: 1.08;
    font-weight: 800;

    margin-bottom: 14px;

    background:
        linear-gradient(
            90deg,
            #ffffff,
            #7dd3fc,
            #a78bfa
        );

    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}


.hero-text {

    color: #b7c4dd;
    font-size: 15px;
    line-height: 1.7;

    max-width: 650px;
}


.badges {

    display: flex;
    gap: 10px;
    flex-wrap: wrap;

    margin-top: 25px;
}


.badge {

    padding: 9px 14px;

    border-radius: 999px;

    background:
        rgba(15, 23, 42, 0.75);

    border:
        1px solid rgba(
            148,
            163,
            184,
            0.18
        );

    color: #dbeafe;

    font-size: 12px;
}


/* Metric cards */

.metric-card {

    min-height: 170px;

    padding: 22px;

    border-radius: 18px;

    background:
        linear-gradient(
            145deg,
            rgba(15, 23, 42, 0.96),
            rgba(12, 18, 39, 0.96)
        );

    border:
        1px solid rgba(
            99,
            102,
            241,
            0.35
        );

    box-shadow:
        0 15px 40px
        rgba(0,0,0,0.22);

    transition: 0.25s ease;
}


.metric-card:hover {

    transform: translateY(-3px);

    border-color:
        rgba(34,211,238,0.55);

    box-shadow:
        0 18px 45px
        rgba(34,211,238,0.08);
}


.metric-icon {

    font-size: 26px;
    margin-bottom: 12px;
}


.metric-label {

    color: #94a3b8;

    font-size: 11px;

    letter-spacing: 1px;

    font-weight: 700;
}


.metric-value {

    font-size: 31px;

    font-weight: 800;

    margin-top: 6px;

    color: #f8fafc;
}


.metric-info {

    color: #64748b;

    font-size: 11px;

    margin-top: 7px;
}


/* Section */

.section-title {

    font-size: 20px;
    font-weight: 800;

    color: #f8fafc;

    margin-top: 28px;
    margin-bottom: 4px;
}


.section-subtitle {

    color: #64748b;

    font-size: 12px;

    margin-bottom: 14px;
}


/* Cards */

.glass-card {

    padding: 22px;

    border-radius: 18px;

    background:
        rgba(15, 23, 42, 0.78);

    border:
        1px solid rgba(
            100,
            116,
            139,
            0.18
        );

    backdrop-filter: blur(14px);
}


/* Prediction result */

.approved {

    border:
        1px solid
        rgba(34,211,238,0.45);

    background:
        linear-gradient(
            135deg,
            rgba(6,78,59,0.40),
            rgba(8,47,73,0.50)
        );
}


.rejected {

    border:
        1px solid
        rgba(244,63,94,0.45);

    background:
        linear-gradient(
            135deg,
            rgba(76,5,25,0.42),
            rgba(30,20,50,0.60)
        );
}


.result-title {

    font-size: 28px;
    font-weight: 800;
}


.result-probability {

    font-size: 38px;
    font-weight: 800;

    background:
        linear-gradient(
            90deg,
            #22d3ee,
            #8b5cf6
        );

    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}


/* Inputs */

.stTextInput input,
.stNumberInput input,
.stSelectbox div[data-baseweb="select"] {

    background-color:
        #101a35 !important;

    color: #f8fafc !important;

    border-color:
        rgba(99,102,241,0.35) !important;
}


/* Buttons */

.stButton > button {

    width: 100%;

    border: none;

    border-radius: 12px;

    padding: 12px 20px;

    font-weight: 800;

    color: white;

    background:
        linear-gradient(
            90deg,
            #7c3aed,
            #06b6d4
        );

    box-shadow:
        0 10px 30px
        rgba(124,58,237,0.25);

    transition: 0.2s ease;
}


.stButton > button:hover {

    transform: translateY(-2px);

    box-shadow:
        0 15px 35px
        rgba(6,182,212,0.25);
}


/* Dataframe */

[data-testid="stDataFrame"] {

    border-radius: 14px;
    overflow: hidden;
}


/* Hide Streamlit branding */

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

header {
    background: transparent !important;
}

</style>
""",
    unsafe_allow_html=True,
)


# =========================================================
# HELPER FUNCTIONS
# =========================================================

def metric_card(
    icon,
    label,
    value,
    info,
    accent="#22d3ee",
):

    return f"""
    <div class="metric-card">

        <div class="metric-icon">
            {icon}
        </div>

        <div class="metric-label">
            {label}
        </div>

        <div
            class="metric-value"
            style="color:{accent};"
        >
            {value}
        </div>

        <div class="metric-info">
            {info}
        </div>

    </div>
    """


def find_dataset():

    possible_files = [
        "loan_data.csv",
        "loan_dataset.csv",
        "loan.csv",
        "LoanApprovalPrediction.csv",
    ]

    for file in possible_files:

        if os.path.exists(file):
            return file

    return None


def get_status_counts(df):

    if TARGET not in df.columns:
        return 0, 0

    values = (
        df[TARGET]
        .astype(str)
        .str.strip()
        .str.lower()
    )

    approved = values.isin(
        ["y", "yes", "approved", "1", "true"]
    ).sum()

    rejected = values.isin(
        ["n", "no", "rejected", "0", "false"]
    ).sum()

    return int(approved), int(rejected)


# =========================================================
# LOAD DATASET
# =========================================================

dataset_file = find_dataset()

df = None

if dataset_file:

    try:

        df = load_data(dataset_file)

        df = prepare_dataset(df)

    except Exception as error:

        st.error(
            f"Could not load dataset: {error}"
        )


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.markdown(
        """
        <div class="logo-box">

            <div class="logo-title">
                🏦 LoanAI
            </div>

            <div class="logo-subtitle">
                Smart Loan Decisions
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="sidebar-label">Navigation</div>',
        unsafe_allow_html=True,
    )

    page = st.radio(
        "Go to",
        [
            "Dashboard",
            "Dataset Analysis",
            "Model Comparison",
            "Loan Prediction",
            "About",
        ],
        label_visibility="collapsed",
    )

    st.markdown("---")

    st.markdown(
        """
        <div class="glass-card">

            <div style="
                color:#22d3ee;
                font-weight:800;
                font-size:12px;
            ">
                AI LOAN INTELLIGENCE
            </div>

            <br>

            <div style="
                color:#94a3b8;
                font-size:12px;
                line-height:1.7;
            ">
                Analyze applications, compare
                machine learning models, and
                generate instant loan predictions.
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )


# =========================================================
# HEADER
# =========================================================

st.markdown(
    """
    <div class="top-header">

        <div class="welcome">
            ☀️ &nbsp;
            <strong>Welcome back, Vishwajith 👋</strong>
            <br>
            <span>
                Loan Approval Prediction System
            </span>
        </div>

    </div>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# HERO
# =========================================================

st.markdown(
    """
    <div class="hero">

        <div class="hero-content">

            <div class="hero-title">
                Predict Loan Approval
                <br>
                with the Power of AI
            </div>

            <div class="hero-text">
                Analyze applicant details, compare
                powerful machine learning models,
                and make smarter lending decisions
                using data-driven insights.
            </div>

            <div class="badges">

                <div class="badge">
                    ⚙️ 4 ML Algorithms
                </div>

                <div class="badge">
                    🛡️ Classification
                </div>

                <div class="badge">
                    📊 Data Driven Insights
                </div>

                <div class="badge">
                    ✨ Easy To Use
                </div>

            </div>

        </div>

    </div>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# DASHBOARD
# =========================================================

if page == "Dashboard":

    if df is None:

        st.warning(
            "loan_data.csv was not found. "
            "Place it in the project folder."
        )

    else:

        total = len(df)

        approved, rejected = get_status_counts(
            df
        )

        approval_rate = (
            approved / total * 100
            if total > 0
            else 0
        )

        st.markdown(
            '<div class="section-title">Project Dashboard</div>',
            unsafe_allow_html=True,
        )

        st.markdown(
            '<div class="section-subtitle">'
            'Real-time overview of your loan dataset'
            '</div>',
            unsafe_allow_html=True,
        )

        # Metrics
        c1, c2, c3, c4 = st.columns(4)

        with c1:
            st.markdown(
                metric_card(
                    "👥",
                    "TOTAL APPLICATIONS",
                    total,
                    "Dataset records",
                ),
                unsafe_allow_html=True,
            )

        with c2:
            st.markdown(
                metric_card(
                    "✓",
                    "APPROVED APPLICATIONS",
                    approved,
                    "Successful applications",
                    "#22d3ee",
                ),
                unsafe_allow_html=True,
            )

        with c3:
            st.markdown(
                metric_card(
                    "✕",
                    "REJECTED APPLICATIONS",
                    rejected,
                    "Rejected applications",
                    "#fb7185",
                ),
                unsafe_allow_html=True,
            )

        with c4:
            st.markdown(
                metric_card(
                    "%",
                    "APPROVAL RATE",
                    f"{approval_rate:.1f}%",
                    "Overall dataset rate",
                    "#a78bfa",
                ),
                unsafe_allow_html=True,
            )

        # Charts
        st.markdown(
            '<div class="section-title">'
            'Application Intelligence'
            '</div>',
            unsafe_allow_html=True,
        )

        chart_col1, chart_col2 = st.columns(2)

        with chart_col1:

            st.markdown(
                '<div class="section-subtitle">'
                'Approved vs rejected applications'
                '</div>',
                unsafe_allow_html=True,
            )

            chart_df = pd.DataFrame(
                {
                    "Status": [
                        "Approved",
                        "Rejected",
                    ],
                    "Applications": [
                        approved,
                        rejected,
                    ],
                }
            )

            st.bar_chart(
                chart_df.set_index("Status")
            )

        with chart_col2:

            st.markdown(
                '<div class="section-subtitle">'
                'Relationship between income and loan amount'
                '</div>',
                unsafe_allow_html=True,
            )

            if (
                "ApplicantIncome" in df.columns
                and
                "LoanAmount" in df.columns
            ):

                chart_data = df[
                    [
                        "ApplicantIncome",
                        "LoanAmount",
                    ]
                ].copy()

                chart_data = chart_data.apply(
                    pd.to_numeric,
                    errors="coerce",
                ).dropna()

                if len(chart_data) > 0:

                    st.scatter_chart(
                        chart_data,
                        x="ApplicantIncome",
                        y="LoanAmount",
                    )

                else:

                    st.info(
                        "No numeric income/loan data available."
                    )

            else:

                st.info(
                    "Income/Loan Amount columns not found."
                )

        # Recent applications
        st.markdown(
            '<div class="section-title">'
            'Recent Loan Applications'
            '</div>',
            unsafe_allow_html=True,
        )

        st.markdown(
            '<div class="section-subtitle">'
            'Latest records from the loan dataset'
            '</div>',
            unsafe_allow_html=True,
        )

        display_df = df.copy()

        if TARGET in display_df.columns:

            display_df["LoanStatus"] = (
                display_df[TARGET]
                .map({
                    1: "Approved",
                    0: "Rejected",
                })
                .fillna(
                    display_df[TARGET]
                )
            )

        st.dataframe(
            display_df.tail(10),
            use_container_width=True,
            hide_index=True,
        )


# =========================================================
# DATASET ANALYSIS
# =========================================================

elif page == "Dataset Analysis":

    st.markdown(
        '<div class="section-title">'
        'Dataset Analysis'
        '</div>',
        unsafe_allow_html=True,
    )

    if df is None:

        st.error(
            "Dataset not available."
        )

    else:

        c1, c2, c3 = st.columns(3)

        with c1:
            st.metric(
                "Rows",
                len(df),
            )

        with c2:
            st.metric(
                "Columns",
                len(df.columns),
            )

        with c3:
            st.metric(
                "Missing Values",
                int(df.isna().sum().sum()),
            )

        st.markdown(
            '<div class="section-title">'
            'Dataset Preview'
            '</div>',
            unsafe_allow_html=True,
        )

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True,
        )

        st.markdown(
            '<div class="section-title">'
            'Numerical Statistics'
            '</div>',
            unsafe_allow_html=True,
        )

        numeric_df = df.select_dtypes(
            include=np.number
        )

        if not numeric_df.empty:

            st.dataframe(
                numeric_df.describe().round(2),
                use_container_width=True,
            )

        else:

            st.info(
                "No numerical columns found."
            )

        st.markdown(
            '<div class="section-title">'
            'Missing Value Analysis'
            '</div>',
            unsafe_allow_html=True,
        )

        missing = (
            df.isna()
            .sum()
            .reset_index()
        )

        missing.columns = [
            "Column",
            "Missing Values",
        ]

        st.dataframe(
            missing,
            use_container_width=True,
            hide_index=True,
        )


# =========================================================
# MODEL COMPARISON
# =========================================================

elif page == "Model Comparison":

    st.markdown(
        '<div class="section-title">'
        'Model Comparison'
        '</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="section-subtitle">'
        'Compare the four classification algorithms'
        '</div>',
        unsafe_allow_html=True,
    )

    results = load_model_results()

    if not results:

        st.warning(
            "No trained models found."
        )

        st.info(
            "Run: python train_models.py"
        )

    else:

        rows = []

        for model_name, metrics in results.items():

            rows.append(
                {
                    "Model": model_name,

                    "Accuracy":
                        round(
                            metrics["accuracy"] * 100,
                            2,
                        ),

                    "Precision":
                        round(
                            metrics["precision"] * 100,
                            2,
                        ),

                    "Recall":
                        round(
                            metrics["recall"] * 100,
                            2,
                        ),

                    "F1 Score":
                        round(
                            metrics["f1"] * 100,
                            2,
                        ),
                }
            )

        results_df = pd.DataFrame(rows)

        best_model = get_best_model()

        st.success(
            f"🏆 Best Model: {best_model}"
        )

        st.dataframe(
            results_df,
            use_container_width=True,
            hide_index=True,
        )

        st.markdown(
            '<div class="section-title">'
            'Performance Visualization'
            '</div>',
            unsafe_allow_html=True,
        )

        plot_df = results_df.set_index(
            "Model"
        )

        st.bar_chart(
            plot_df[
                [
                    "Accuracy",
                    "Precision",
                    "Recall",
                    "F1 Score",
                ]
            ]
        )

        # Confusion matrices
        st.markdown(
            '<div class="section-title">'
            'Confusion Matrices'
            '</div>',
            unsafe_allow_html=True,
        )

        for model_name, metrics in results.items():

            cm = np.array(
                metrics["confusion_matrix"]
            )

            cm_df = pd.DataFrame(
                cm,
                index=[
                    "Actual Rejected",
                    "Actual Approved",
                ],
                columns=[
                    "Predicted Rejected",
                    "Predicted Approved",
                ],
            )

            st.markdown(
                f"**{model_name}**"
            )

            st.dataframe(
                cm_df,
                use_container_width=True,
            )


# =========================================================
# LOAN PREDICTION
# =========================================================

elif page == "Loan Prediction":

    st.markdown(
        '<div class="section-title">'
        'Quick Loan Prediction'
        '</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="section-subtitle">'
        'Enter applicant details to generate an AI-based prediction'
        '</div>',
        unsafe_allow_html=True,
    )

    available_models = get_available_models()

    if not available_models:

        st.error(
            "No trained models are available."
        )

        st.info(
            "Run this command first:"
        )

        st.code(
            "python train_models.py"
        )

    else:

        col_form, col_result = st.columns(
            [1.05, 0.95]
        )

        with col_form:

            st.markdown(
                '<div class="glass-card">',
                unsafe_allow_html=True,
            )

            st.markdown(
                "### 👤 Applicant Details"
            )

            gender = st.selectbox(
                "Gender",
                [
                    "Male",
                    "Female",
                ],
            )

            married = st.selectbox(
                "Married",
                [
                    "Yes",
                    "No",
                ],
            )

            education = st.selectbox(
                "Education",
                [
                    "Graduate",
                    "Not Graduate",
                ],
            )

            applicant_income = st.number_input(
                "Applicant Income (₹)",
                min_value=0,
                max_value=1000000,
                value=5000,
                step=500,
            )

            loan_amount = st.number_input(
                "Loan Amount (₹)",
                min_value=0,
                max_value=1000000,
                value=150,
                step=10,
            )

            credit_history = st.selectbox(
                "Credit History",
                [
                    1.0,
                    0.0,
                ],
                format_func=lambda x:
                    "Good (1.0)"
                    if x == 1.0
                    else "Poor (0.0)",
            )

            property_area = st.selectbox(
                "Property Area",
                [
                    "Urban",
                    "Semiurban",
                    "Rural",
                ],
            )

            selected_model = st.selectbox(
                "Prediction Model",
                available_models,
                index=(
                    available_models.index(
                        get_best_model()
                    )
                    if get_best_model()
                    in available_models
                    else 0
                ),
            )

            predict_button = st.button(
                "✨ Predict Loan Status"
            )

            st.markdown(
                '</div>',
                unsafe_allow_html=True,
            )

        with col_result:

            if predict_button:

                applicant = {

                    "Gender":
                        gender,

                    "Married":
                        married,

                    "Education":
                        education,

                    "ApplicantIncome":
                        applicant_income,

                    "LoanAmount":
                        loan_amount,

                    "CreditHistory":
                        credit_history,

                    "PropertyArea":
                        property_area,
                }

                try:

                    result = predict_loan(
                        applicant,
                        selected_model,
                    )

                    status = result["status"]

                    probability = (
                        result[
                            "probability_percent"
                        ]
                    )

                    if status == "Approved":

                        st.markdown(
                            f"""
                            <div class="glass-card approved">

                                <div style="
                                    color:#67e8f9;
                                    font-size:13px;
                                    font-weight:700;
                                ">
                                    ✨ PREDICTION RESULT
                                </div>

                                <br>

                                <div class="result-title">
                                    🟢 LOAN APPROVED
                                </div>

                                <br>

                                <div style="
                                    color:#94a3b8;
                                ">
                                    Approval Probability
                                </div>

                                <div class="result-probability">
                                    {probability:.1f}%
                                </div>

                                <hr>

                                <div style="
                                    color:#cbd5e1;
                                    line-height:1.7;
                                ">
                                    The model predicts that
                                    this applicant has a
                                    relatively strong chance
                                    of loan approval based on
                                    the supplied information.
                                </div>

                                <br>

                                <div style="
                                    color:#64748b;
                                    font-size:12px;
                                ">
                                    Model: {selected_model}
                                </div>

                            </div>
                            """,
                            unsafe_allow_html=True,
                        )

                    else:

                        st.markdown(
                            f"""
                            <div class="glass-card rejected">

                                <div style="
                                    color:#fb7185;
                                    font-size:13px;
                                    font-weight:700;
                                ">
                                    ⚠️ PREDICTION RESULT
                                </div>

                                <br>

                                <div class="result-title">
                                    🔴 LOAN REJECTED
                                </div>

                                <br>

                                <div style="
                                    color:#94a3b8;
                                ">
                                    Approval Probability
                                </div>

                                <div class="result-probability">
                                    {probability:.1f}%
                                </div>

                                <hr>

                                <div style="
                                    color:#cbd5e1;
                                    line-height:1.7;
                                ">
                                    The model predicts a lower
                                    likelihood of loan approval
                                    for the supplied applicant
                                    information.
                                </div>

                                <br>

                                <div style="
                                    color:#64748b;
                                    font-size:12px;
                                ">
                                    Model: {selected_model}
                                </div>

                            </div>
                            """,
                            unsafe_allow_html=True,
                        )

                except Exception as error:

                    st.error(
                        f"Prediction failed: {error}"
                    )

            else:

                st.markdown(
                    """
                    <div class="glass-card">

                        <div style="
                            font-size:42px;
                        ">
                            🏦
                        </div>

                        <h2>
                            Ready for Prediction
                        </h2>

                        <p style="
                            color:#94a3b8;
                            line-height:1.7;
                        ">
                            Enter the applicant details
                            and click the prediction
                            button to generate an
                            AI-powered loan decision.
                        </p>

                    </div>
                    """,
                    unsafe_allow_html=True,
                )


# =========================================================
# ABOUT
# =========================================================

elif page == "About":

    st.markdown(
        '<div class="section-title">'
        'About LoanAI'
        '</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="glass-card">

            <h2>
                🏦 Loan Approval Prediction System
            </h2>

            <p style="
                color:#94a3b8;
                line-height:1.8;
            ">
                LoanAI is a machine learning based
                classification system designed to
                predict whether a loan application
                is likely to be approved or rejected.
            </p>

            <h3>
                Machine Learning Algorithms
            </h3>

            <ul style="
                color:#cbd5e1;
                line-height:2;
            ">
                <li>Logistic Regression</li>
                <li>Decision Tree Classifier</li>
                <li>Random Forest Classifier</li>
                <li>XGBoost Classifier</li>
            </ul>

            <h3>
                Input Features
            </h3>

            <ul style="
                color:#cbd5e1;
                line-height:2;
            ">
                <li>Gender</li>
                <li>Married Status</li>
                <li>Education</li>
                <li>Applicant Income</li>
                <li>Loan Amount</li>
                <li>Credit History</li>
                <li>Property Area</li>
            </ul>

            <h3>
                Technologies
            </h3>

            <p style="
                color:#22d3ee;
                font-weight:700;
            ">
                Python • Pandas • Scikit-learn
                • XGBoost • Streamlit • Joblib
            </p>

        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div style="
            text-align:center;
            color:#64748b;
            padding:35px;
            font-size:12px;
        ">
            LoanAI • Machine Learning Loan Approval System
            <br>
            Built with Python + Streamlit + Machine Learning
        </div>
        """,
        unsafe_allow_html=True,
    )