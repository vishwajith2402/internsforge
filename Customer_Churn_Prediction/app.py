import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

import pandas as pd
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

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
    customer_risk,
    generate_business_recommendation
)


# ============================================================
# APPLICATION
# ============================================================

class CustomerChurnApp:

    def __init__(self, root):

        self.root = root

        self.root.title(
            "Customer Churn Intelligence"
        )

        self.root.geometry(
            "1450x900"
        )

        self.root.minsize(
            1200,
            750
        )

        # ----------------------------------------------------
        # COLORS
        # ----------------------------------------------------

        self.bg = "#08090D"
        self.sidebar = "#0D0F16"
        self.card = "#12151E"
        self.card_hover = "#181C28"

        self.white = "#F8FAFC"
        self.gray = "#94A3B8"

        self.cyan = "#22D3EE"
        self.purple = "#8B5CF6"
        self.green = "#22C55E"
        self.red = "#EF4444"
        self.orange = "#F59E0B"

        # ----------------------------------------------------
        # DATA
        # ----------------------------------------------------

        self.data = None

        self.X_train = None
        self.X_test = None
        self.y_train = None
        self.y_test = None

        self.preprocessor = None

        self.trained_models = {}
        self.results_df = None

        self.best_model = None
        self.best_model_name = None

        self.feature_df = None

        self.current_page = None

        # ----------------------------------------------------
        # STYLE
        # ----------------------------------------------------

        self.configure_style()

        # ----------------------------------------------------
        # BUILD UI
        # ----------------------------------------------------

        self.build_layout()

        self.show_dashboard()

    # ========================================================
    # STYLE
    # ========================================================

    def configure_style(self):

        style = ttk.Style()

        try:
            style.theme_use(
                "clam"
            )
        except:
            pass

        style.configure(
            "TFrame",
            background=self.bg
        )

        style.configure(
            "Sidebar.TFrame",
            background=self.sidebar
        )

        style.configure(
            "Card.TFrame",
            background=self.card
        )

        style.configure(
            "TLabel",
            background=self.bg,
            foreground=self.white
        )

        style.configure(
            "Sidebar.TLabel",
            background=self.sidebar,
            foreground=self.white
        )

        style.configure(
            "Muted.TLabel",
            background=self.bg,
            foreground=self.gray
        )

        style.configure(
            "CardTitle.TLabel",
            background=self.card,
            foreground=self.gray,
            font=(
                "Segoe UI",
                10
            )
        )

        style.configure(
            "CardValue.TLabel",
            background=self.card,
            foreground=self.white,
            font=(
                "Segoe UI",
                22,
                "bold"
            )
        )

        style.configure(
            "Heading.TLabel",
            background=self.bg,
            foreground=self.white,
            font=(
                "Segoe UI",
                26,
                "bold"
            )
        )

        style.configure(
            "SubHeading.TLabel",
            background=self.bg,
            foreground=self.gray,
            font=(
                "Segoe UI",
                11
            )
        )

        style.configure(
            "TButton",
            background=self.purple,
            foreground=self.white,
            borderwidth=0,
            padding=10,
            font=(
                "Segoe UI",
                10,
                "bold"
            )
        )

        style.map(
            "TButton",
            background=[
                (
                    "active",
                    self.cyan
                )
            ]
        )

        style.configure(
            "Treeview",
            background=self.card,
            foreground=self.white,
            fieldbackground=self.card,
            rowheight=32,
            borderwidth=0
        )

        style.configure(
            "Treeview.Heading",
            background=self.purple,
            foreground=self.white,
            font=(
                "Segoe UI",
                10,
                "bold"
            )
        )

        style.map(
            "Treeview",
            background=[
                (
                    "selected",
                    self.purple
                )
            ]
        )

    # ========================================================
    # MAIN LAYOUT
    # ========================================================

    def build_layout(self):

        # Sidebar
        self.sidebar_frame = ttk.Frame(
            self.root,
            style="Sidebar.TFrame",
            width=250
        )

        self.sidebar_frame.pack(
            side="left",
            fill="y"
        )

        self.sidebar_frame.pack_propagate(
            False
        )

        self.create_sidebar()

        # Main area
        self.main_frame = ttk.Frame(
            self.root
        )

        self.main_frame.pack(
            side="right",
            fill="both",
            expand=True
        )

        # Header
        self.header_frame = ttk.Frame(
            self.main_frame
        )

        self.header_frame.pack(
            fill="x",
            padx=35,
            pady=(25, 10)
        )

        # Page container
        self.content_frame = ttk.Frame(
            self.main_frame
        )

        self.content_frame.pack(
            fill="both",
            expand=True,
            padx=35,
            pady=10
        )

    # ========================================================
    # SIDEBAR
    # ========================================================

    def create_sidebar(self):

        logo_frame = tk.Frame(
            self.sidebar_frame,
            bg=self.sidebar
        )

        logo_frame.pack(
            fill="x",
            padx=22,
            pady=(30, 30)
        )

        tk.Label(
            logo_frame,
            text="CHURN",
            bg=self.sidebar,
            fg=self.cyan,
            font=(
                "Segoe UI",
                22,
                "bold"
            )
        ).pack(
            anchor="w"
        )

        tk.Label(
            logo_frame,
            text="INTELLIGENCE",
            bg=self.sidebar,
            fg=self.white,
            font=(
                "Segoe UI",
                11,
                "bold"
            )
        ).pack(
            anchor="w"
        )

        tk.Label(
            logo_frame,
            text="Machine Learning Analytics",
            bg=self.sidebar,
            fg=self.gray,
            font=(
                "Segoe UI",
                9
            )
        ).pack(
            anchor="w",
            pady=(5, 0)
        )

        self.create_nav_button(
            "⌂   Dashboard",
            self.show_dashboard
        )

        self.create_nav_button(
            "◈   Model Performance",
            self.show_model_performance
        )

        self.create_nav_button(
            "◎   Customer Prediction",
            self.show_prediction
        )

        self.create_nav_button(
            "◆   Feature Importance",
            self.show_features
        )

        self.create_nav_button(
            "▤   Dataset Explorer",
            self.show_dataset
        )

        spacer = tk.Frame(
            self.sidebar_frame,
            bg=self.sidebar
        )

        spacer.pack(
            fill="both",
            expand=True
        )

        # Bottom buttons
        self.create_nav_button(
            "↥   Load Dataset",
            self.load_dataset
        )

        self.create_nav_button(
            "⚙   Train Models",
            self.train_models_ui
        )

        tk.Label(
            self.sidebar_frame,
            text="ML PROJECT • 2026",
            bg=self.sidebar,
            fg="#475569",
            font=(
                "Segoe UI",
                8
            )
        ).pack(
            pady=20
        )

    # ========================================================
    # NAV BUTTON
    # ========================================================

    def create_nav_button(
        self,
        text,
        command
    ):

        button = tk.Button(
            self.sidebar_frame,
            text=text,
            command=command,
            bg=self.sidebar,
            fg=self.gray,
            activebackground=self.card_hover,
            activeforeground=self.cyan,
            relief="flat",
            bd=0,
            anchor="w",
            padx=25,
            pady=12,
            font=(
                "Segoe UI",
                10
            ),
            cursor="hand2"
        )

        button.pack(
            fill="x",
            padx=10,
            pady=2
        )

        return button

    # ========================================================
    # HEADER
    # ========================================================

    def set_header(
        self,
        title,
        subtitle
    ):

        for widget in self.header_frame.winfo_children():

            widget.destroy()

        left = ttk.Frame(
            self.header_frame
        )

        left.pack(
            side="left"
        )

        ttk.Label(
            left,
            text=title,
            style="Heading.TLabel"
        ).pack(
            anchor="w"
        )

        ttk.Label(
            left,
            text=subtitle,
            style="SubHeading.TLabel"
        ).pack(
            anchor="w",
            pady=(3, 0)
        )

        status = (
            "MODEL READY"
            if self.best_model is not None
            else "MODEL NOT TRAINED"
        )

        status_color = (
            self.green
            if self.best_model is not None
            else self.orange
        )

        tk.Label(
            self.header_frame,
            text=f"●  {status}",
            bg=self.bg,
            fg=status_color,
            font=(
                "Segoe UI",
                9,
                "bold"
            )
        ).pack(
            side="right",
            pady=10
        )

    # ========================================================
    # CLEAR CONTENT
    # ========================================================

    def clear_content(self):

        for widget in self.content_frame.winfo_children():

            widget.destroy()

    # ========================================================
    # DASHBOARD
    # ========================================================

    def show_dashboard(self):

        self.current_page = "dashboard"

        self.clear_content()

        self.set_header(
            "Customer Churn Dashboard",
            "Machine learning powered customer retention analytics"
        )

        # ----------------------------------------------------
        # KPI ROW
        # ----------------------------------------------------

        kpi_frame = ttk.Frame(
            self.content_frame
        )

        kpi_frame.pack(
            fill="x",
            pady=(10, 20)
        )

        summary = {}

        if self.data is not None:

            summary = churn_summary(
                self.data
            )

        total = summary.get(
            "total_customers",
            0
        )

        churned = summary.get(
            "churned_customers",
            0
        )

        churn_rate = summary.get(
            "churn_percentage",
            0
        )

        best_score = 0

        if self.results_df is not None:

            best_score = (
                self.results_df.iloc[0]["ROC-AUC"]
            )

        self.create_kpi(
            kpi_frame,
            "TOTAL CUSTOMERS",
            str(total),
            self.cyan
        )

        self.create_kpi(
            kpi_frame,
            "CHURNED CUSTOMERS",
            str(churned),
            self.red
        )

        self.create_kpi(
            kpi_frame,
            "CHURN RATE",
            f"{churn_rate:.1f}%",
            self.orange
        )

        self.create_kpi(
            kpi_frame,
            "BEST ROC-AUC",
            f"{best_score:.3f}"
            if best_score
            else "--",
            self.green
        )

        # ----------------------------------------------------
        # LOWER AREA
        # ----------------------------------------------------

        lower = ttk.Frame(
            self.content_frame
        )

        lower.pack(
            fill="both",
            expand=True
        )

        # Left
        chart_card = self.create_card(
            lower
        )

        chart_card.pack(
            side="left",
            fill="both",
            expand=True,
            padx=(0, 10)
        )

        tk.Label(
            chart_card,
            text="Churn Overview",
            bg=self.card,
            fg=self.white,
            font=(
                "Segoe UI",
                13,
                "bold"
            )
        ).pack(
            anchor="w",
            padx=20,
            pady=(18, 5)
        )

        tk.Label(
            chart_card,
            text="Customer retention vs churn",
            bg=self.card,
            fg=self.gray,
            font=(
                "Segoe UI",
                9
            )
        ).pack(
            anchor="w",
            padx=20
        )

        if self.data is not None:

            self.draw_churn_chart(
                chart_card
            )

        else:

            tk.Label(
                chart_card,
                text="Load a dataset to view analytics",
                bg=self.card,
                fg=self.gray,
                font=(
                    "Segoe UI",
                    11
                )
            ).pack(
                expand=True
            )

        # Right
        info_card = self.create_card(
            lower
        )

        info_card.pack(
            side="right",
            fill="both",
            expand=True,
            padx=(10, 0)
        )

        tk.Label(
            info_card,
            text="ML System Status",
            bg=self.card,
            fg=self.white,
            font=(
                "Segoe UI",
                13,
                "bold"
            )
        ).pack(
            anchor="w",
            padx=20,
            pady=(18, 20)
        )

        self.status_row(
            info_card,
            "Dataset",
            "Loaded" if self.data is not None else "Not loaded",
            self.green if self.data is not None else self.orange
        )

        self.status_row(
            info_card,
            "Models",
            "4 Algorithms",
            self.cyan
        )

        self.status_row(
            info_card,
            "Best Model",
            self.best_model_name or "Not trained",
            self.purple
        )

        self.status_row(
            info_card,
            "Prediction",
            "Available" if self.best_model is not None else "Train model first",
            self.green if self.best_model is not None else self.orange
        )

        # Description
        tk.Label(
            info_card,
            text=(
                "The system uses supervised classification "
                "to identify customers who are likely to churn."
            ),
            bg=self.card,
            fg=self.gray,
            wraplength=380,
            justify="left",
            font=(
                "Segoe UI",
                10
            )
        ).pack(
            anchor="w",
            padx=20,
            pady=(25, 10)
        )

    # ========================================================
    # KPI CARD
    # ========================================================

    def create_kpi(
        self,
        parent,
        title,
        value,
        accent
    ):

        card = tk.Frame(
            parent,
            bg=self.card,
            height=120
        )

        card.pack(
            side="left",
            fill="both",
            expand=True,
            padx=6
        )

        tk.Frame(
            card,
            bg=accent,
            width=4
        ).pack(
            side="left",
            fill="y"
        )

        tk.Label(
            card,
            text=title,
            bg=self.card,
            fg=self.gray,
            font=(
                "Segoe UI",
                9,
                "bold"
            )
        ).pack(
            anchor="w",
            padx=20,
            pady=(20, 3)
        )

        tk.Label(
            card,
            text=value,
            bg=self.card,
            fg=self.white,
            font=(
                "Segoe UI",
                24,
                "bold"
            )
        ).pack(
            anchor="w",
            padx=20
        )

    # ========================================================
    # CARD
    # ========================================================

    def create_card(
        self,
        parent
    ):

        return tk.Frame(
            parent,
            bg=self.card,
            bd=0,
            highlightthickness=1,
            highlightbackground="#202633"
        )

    # ========================================================
    # STATUS ROW
    # ========================================================

    def status_row(
        self,
        parent,
        label,
        value,
        color
    ):

        row = tk.Frame(
            parent,
            bg=self.card
        )

        row.pack(
            fill="x",
            padx=20,
            pady=8
        )

        tk.Label(
            row,
            text=label,
            bg=self.card,
            fg=self.gray,
            font=(
                "Segoe UI",
                10
            )
        ).pack(
            side="left"
        )

        tk.Label(
            row,
            text=value,
            bg=self.card,
            fg=color,
            font=(
                "Segoe UI",
                10,
                "bold"
            )
        ).pack(
            side="right"
        )

    # ========================================================
    # CHURN CHART
    # ========================================================

    def draw_churn_chart(
        self,
        parent
    ):

        figure = Figure(
            figsize=(6, 3.8),
            dpi=100,
            facecolor=self.card
        )

        ax = figure.add_subplot(
            111
        )

        churn = (
            self.data["Churn"]
            .astype(str)
            .str.lower()
            .value_counts()
        )

        labels = [
            "Retained",
            "Churned"
        ]

        values = [
            churn.get(
                "no",
                0
            ),
            churn.get(
                "yes",
                0
            )
        ]

        ax.bar(
            labels,
            values
        )

        ax.set_facecolor(
            self.card
        )

        ax.tick_params(
            colors=self.gray
        )

        for spine in ax.spines.values():

            spine.set_visible(
                False
            )

        ax.set_title(
            "Customer Distribution",
            color=self.white,
            fontsize=11
        )

        figure.tight_layout()

        canvas = FigureCanvasTkAgg(
            figure,
            parent
        )

        canvas.draw()

        canvas.get_tk_widget().pack(
            fill="both",
            expand=True,
            padx=15,
            pady=10
        )

    # ========================================================
    # MODEL PERFORMANCE
    # ========================================================

    def show_model_performance(self):

        self.current_page = "models"

        self.clear_content()

        self.set_header(
            "Model Performance",
            "Compare classification algorithms across evaluation metrics"
        )

        if self.results_df is None:

            self.empty_state(
                "No trained models",
                "Click 'Train Models' to generate model performance."
            )

            return

        # ----------------------------------------------------
        # TABLE
        # ----------------------------------------------------

        card = self.create_card(
            self.content_frame
        )

        card.pack(
            fill="x",
            pady=(10, 20)
        )

        tk.Label(
            card,
            text="Classification Model Comparison",
            bg=self.card,
            fg=self.white,
            font=(
                "Segoe UI",
                13,
                "bold"
            )
        ).pack(
            anchor="w",
            padx=20,
            pady=(18, 15)
        )

        columns = (
            "Model",
            "Accuracy",
            "Precision",
            "Recall",
            "F1 Score",
            "ROC-AUC"
        )

        tree = ttk.Treeview(
            card,
            columns=columns,
            show="headings",
            height=5
        )

        for column in columns:

            tree.heading(
                column,
                text=column
            )

            tree.column(
                column,
                width=150,
                anchor="center"
            )

        for _, row in self.results_df.iterrows():

            tree.insert(
                "",
                "end",
                values=(
                    row["Model"],
                    f"{row['Accuracy']:.4f}",
                    f"{row['Precision']:.4f}",
                    f"{row['Recall']:.4f}",
                    f"{row['F1 Score']:.4f}",
                    f"{row['ROC-AUC']:.4f}"
                )
            )

        tree.pack(
            fill="x",
            padx=20,
            pady=(0, 20)
        )

        # ----------------------------------------------------
        # BAR CHART
        # ----------------------------------------------------

        chart_card = self.create_card(
            self.content_frame
        )

        chart_card.pack(
            fill="both",
            expand=True
        )

        tk.Label(
            chart_card,
            text="ROC-AUC Comparison",
            bg=self.card,
            fg=self.white,
            font=(
                "Segoe UI",
                13,
                "bold"
            )
        ).pack(
            anchor="w",
            padx=20,
            pady=15
        )

        self.draw_model_chart(
            chart_card
        )

    # ========================================================
    # MODEL CHART
    # ========================================================

    def draw_model_chart(
        self,
        parent
    ):

        figure = Figure(
            figsize=(8, 4),
            dpi=100,
            facecolor=self.card
        )

        ax = figure.add_subplot(
            111
        )

        models = self.results_df[
            "Model"
        ]

        scores = self.results_df[
            "ROC-AUC"
        ]

        ax.bar(
            models,
            scores
        )

        ax.set_ylim(
            0,
            1
        )

        ax.set_facecolor(
            self.card
        )

        ax.tick_params(
            colors=self.gray,
            labelrotation=15
        )

        for spine in ax.spines.values():

            spine.set_visible(
                False
            )

        ax.set_ylabel(
            "ROC-AUC",
            color=self.gray
        )

        figure.tight_layout()

        canvas = FigureCanvasTkAgg(
            figure,
            parent
        )

        canvas.draw()

        canvas.get_tk_widget().pack(
            fill="both",
            expand=True,
            padx=20,
            pady=10
        )

    # ========================================================
    # FEATURE IMPORTANCE
    # ========================================================

    def show_features(self):

        self.current_page = "features"

        self.clear_content()

        self.set_header(
            "Feature Importance",
            "Identify the factors influencing customer churn"
        )

        if self.feature_df is None:

            self.empty_state(
                "Feature analysis unavailable",
                "Train the machine learning models first."
            )

            return

        card = self.create_card(
            self.content_frame
        )

        card.pack(
            fill="both",
            expand=True
        )

        tk.Label(
            card,
            text="Top Churn Drivers",
            bg=self.card,
            fg=self.white,
            font=(
                "Segoe UI",
                14,
                "bold"
            )
        ).pack(
            anchor="w",
            padx=20,
            pady=(20, 5)
        )

        tk.Label(
            card,
            text=(
                f"Feature importance from "
                f"{self.best_model_name}"
            ),
            bg=self.card,
            fg=self.gray,
            font=(
                "Segoe UI",
                9
            )
        ).pack(
            anchor="w",
            padx=20
        )

        columns = (
            "Rank",
            "Feature",
            "Importance"
        )

        tree = ttk.Treeview(
            card,
            columns=columns,
            show="headings"
        )

        for column in columns:

            tree.heading(
                column,
                text=column
            )

        tree.column(
            "Rank",
            width=100,
            anchor="center"
        )

        tree.column(
            "Feature",
            width=500
        )

        tree.column(
            "Importance",
            width=180,
            anchor="center"
        )

        for index, row in self.feature_df.head(
            15
        ).iterrows():

            tree.insert(
                "",
                "end",
                values=(
                    index + 1,
                    row["Feature"],
                    f"{row['Importance']:.5f}"
                )
            )

        tree.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=20
        )

    # ========================================================
    # DATASET EXPLORER
    # ========================================================

    def show_dataset(self):

        self.current_page = "dataset"

        self.clear_content()

        self.set_header(
            "Dataset Explorer",
            "Inspect the customer data used by the ML system"
        )

        if self.data is None:

            self.empty_state(
                "No dataset loaded",
                "Use 'Load Dataset' to select a CSV file."
            )

            return

        card = self.create_card(
            self.content_frame
        )

        card.pack(
            fill="both",
            expand=True
        )

        columns = list(
            self.data.columns
        )

        tree = ttk.Treeview(
            card,
            columns=columns,
            show="headings"
        )

        for column in columns:

            tree.heading(
                column,
                text=column
            )

            tree.column(
                column,
                width=140,
                anchor="center"
            )

        for _, row in self.data.head(
            250
        ).iterrows():

            values = [
                str(
                    row[column]
                )
                for column in columns
            ]

            tree.insert(
                "",
                "end",
                values=values
            )

        scrollbar = ttk.Scrollbar(
            card,
            orient="vertical",
            command=tree.yview
        )

        tree.configure(
            yscrollcommand=scrollbar.set
        )

        tree.pack(
            side="left",
            fill="both",
            expand=True,
            padx=(20, 0),
            pady=20
        )

        scrollbar.pack(
            side="right",
            fill="y",
            pady=20,
            padx=(0, 20)
        )

    # ========================================================
    # PREDICTION
    # ========================================================

    def show_prediction(self):

        self.current_page = "prediction"

        self.clear_content()

        self.set_header(
            "Customer Prediction",
            "Estimate the probability that an individual customer will churn"
        )

        if self.best_model is None:

            self.empty_state(
                "Model not ready",
                "Train the models before making customer predictions."
            )

            return

        outer = ttk.Frame(
            self.content_frame
        )

        outer.pack(
            fill="both",
            expand=True
        )

        # Form
        form_card = self.create_card(
            outer
        )

        form_card.pack(
            side="left",
            fill="y",
            padx=(0, 12)
        )

        tk.Label(
            form_card,
            text="Customer Information",
            bg=self.card,
            fg=self.white,
            font=(
                "Segoe UI",
                14,
                "bold"
            )
        ).pack(
            anchor="w",
            padx=25,
            pady=(25, 5)
        )

        tk.Label(
            form_card,
            text="Enter customer attributes",
            bg=self.card,
            fg=self.gray,
            font=(
                "Segoe UI",
                9
            )
        ).pack(
            anchor="w",
            padx=25,
            pady=(0, 20)
        )

        self.prediction_entries = {}

        fields = [
            (
                "Gender",
                "Male"
            ),
            (
                "Tenure",
                "12"
            ),
            (
                "Monthly Charges",
                "70"
            ),
            (
                "Total Charges",
                "840"
            ),
            (
                "Contract Type",
                "Month-to-month"
            ),
            (
                "Internet Service",
                "Fiber optic"
            ),
            (
                "Payment Method",
                "Electronic check"
            )
        ]

        for label, default in fields:

            row = tk.Frame(
                form_card,
                bg=self.card
            )

            row.pack(
                fill="x",
                padx=25,
                pady=7
            )

            tk.Label(
                row,
                text=label,
                bg=self.card,
                fg=self.gray,
                width=20,
                anchor="w",
                font=(
                    "Segoe UI",
                    9
                )
            ).pack(
                side="left"
            )

            entry = tk.Entry(
                row,
                bg="#0B0D12",
                fg=self.white,
                insertbackground=self.white,
                relief="flat",
                width=28,
                font=(
                    "Segoe UI",
                    9
                )
            )

            entry.insert(
                0,
                default
            )

            entry.pack(
                side="right",
                ipady=7
            )

            self.prediction_entries[
                label
            ] = entry

        tk.Button(
            form_card,
            text="PREDICT CHURN",
            command=self.predict_customer,
            bg=self.purple,
            fg=self.white,
            activebackground=self.cyan,
            activeforeground=self.bg,
            relief="flat",
            bd=0,
            padx=20,
            pady=12,
            font=(
                "Segoe UI",
                10,
                "bold"
            ),
            cursor="hand2"
        ).pack(
            fill="x",
            padx=25,
            pady=25
        )

        # Result
        self.prediction_result_card = self.create_card(
            outer
        )

        self.prediction_result_card.pack(
            side="right",
            fill="both",
            expand=True,
            padx=(12, 0)
        )

        self.show_prediction_placeholder()

    # ========================================================
    # PREDICTION PLACEHOLDER
    # ========================================================

    def show_prediction_placeholder(self):

        tk.Label(
            self.prediction_result_card,
            text="Prediction Result",
            bg=self.card,
            fg=self.white,
            font=(
                "Segoe UI",
                18,
                "bold"
            )
        ).pack(
            pady=(80, 10)
        )

        tk.Label(
            self.prediction_result_card,
            text="Enter customer details and run the ML model.",
            bg=self.card,
            fg=self.gray,
            font=(
                "Segoe UI",
                10
            )
        ).pack()

    # ========================================================
    # PREDICT CUSTOMER
    # ========================================================

    def predict_customer(self):

        try:

            values = self.prediction_entries

            customer = pd.DataFrame([
                {
                    "Gender": values[
                        "Gender"
                    ].get(),

                    "Tenure": float(
                        values[
                            "Tenure"
                        ].get()
                    ),

                    "Monthly Charges": float(
                        values[
                            "Monthly Charges"
                        ].get()
                    ),

                    "Total Charges": float(
                        values[
                            "Total Charges"
                        ].get()
                    ),

                    "Contract Type": values[
                        "Contract Type"
                    ].get(),

                    "Internet Service": values[
                        "Internet Service"
                    ].get(),

                    "Payment Method": values[
                        "Payment Method"
                    ].get()
                }
            ])

            prediction = self.best_model.predict(
                customer
            )[0]

            probability = self.best_model.predict_proba(
                customer
            )[0][1]

            risk = customer_risk(
                probability
            )

            recommendations = (
                generate_business_recommendation(
                    probability,
                    customer.iloc[0].to_dict()
                )
            )

            self.display_prediction(
                prediction,
                probability,
                risk,
                recommendations
            )

        except Exception as error:

            messagebox.showerror(
                "Prediction Error",
                str(error)
            )

    # ========================================================
    # DISPLAY PREDICTION
    # ========================================================

    def display_prediction(
        self,
        prediction,
        probability,
        risk,
        recommendations
    ):

        for widget in (
            self.prediction_result_card
            .winfo_children()
        ):

            widget.destroy()

        risk_color = {
            "VERY HIGH RISK": self.red,
            "HIGH RISK": self.orange,
            "MEDIUM RISK": self.orange,
            "LOW RISK": self.green
        }.get(
            risk,
            self.gray
        )

        result = (
            "LIKELY TO CHURN"
            if prediction == 1
            else "LIKELY TO STAY"
        )

        result_color = (
            self.red
            if prediction == 1
            else self.green
        )

        tk.Label(
            self.prediction_result_card,
            text="PREDICTION RESULT",
            bg=self.card,
            fg=self.gray,
            font=(
                "Segoe UI",
                10,
                "bold"
            )
        ).pack(
            pady=(40, 10)
        )

        tk.Label(
            self.prediction_result_card,
            text=result,
            bg=self.card,
            fg=result_color,
            font=(
                "Segoe UI",
                25,
                "bold"
            )
        ).pack(
            pady=5
        )

        tk.Label(
            self.prediction_result_card,
            text=f"{probability * 100:.2f}%",
            bg=self.card,
            fg=self.white,
            font=(
                "Segoe UI",
                38,
                "bold"
            )
        ).pack(
            pady=(25, 0)
        )

        tk.Label(
            self.prediction_result_card,
            text="CHURN PROBABILITY",
            bg=self.card,
            fg=self.gray,
            font=(
                "Segoe UI",
                9
            )
        ).pack()

        tk.Label(
            self.prediction_result_card,
            text=risk,
            bg=self.card,
            fg=risk_color,
            font=(
                "Segoe UI",
                14,
                "bold"
            )
        ).pack(
            pady=20
        )

        tk.Label(
            self.prediction_result_card,
            text=f"Model: {self.best_model_name}",
            bg=self.card,
            fg=self.cyan,
            font=(
                "Segoe UI",
                10
            )
        ).pack()

        # Recommendation box
        recommendation_box = tk.Frame(
            self.prediction_result_card,
            bg="#0D1118"
        )

        recommendation_box.pack(
            fill="x",
            padx=35,
            pady=30
        )

        tk.Label(
            recommendation_box,
            text="BUSINESS RECOMMENDATION",
            bg="#0D1118",
            fg=self.purple,
            font=(
                "Segoe UI",
                10,
                "bold"
            )
        ).pack(
            anchor="w",
            padx=15,
            pady=(15, 8)
        )

        for recommendation in recommendations:

            tk.Label(
                recommendation_box,
                text=f"• {recommendation}",
                bg="#0D1118",
                fg=self.gray,
                wraplength=480,
                justify="left",
                font=(
                    "Segoe UI",
                    9
                )
            ).pack(
                anchor="w",
                padx=15,
                pady=3
            )

        tk.Label(
            recommendation_box,
            text=""
        ).pack(
            pady=5
        )

    # ========================================================
    # LOAD DATASET
    # ========================================================

    def load_dataset(self):

        file_path = filedialog.askopenfilename(
            title="Select Customer Churn Dataset",
            filetypes=[
                (
                    "CSV files",
                    "*.csv"
                )
            ]
        )

        if not file_path:
            return

        try:

            data = load_data(
                file_path
            )

            self.data = data

            self.results_df = None
            self.best_model = None
            self.best_model_name = None
            self.feature_df = None

            messagebox.showinfo(
                "Dataset Loaded",
                (
                    f"Dataset loaded successfully.\n\n"
                    f"Rows: {len(data)}\n"
                    f"Columns: {len(data.columns)}"
                )
            )

            self.show_dashboard()

        except Exception as error:

            messagebox.showerror(
                "Dataset Error",
                str(error)
            )

    # ========================================================
    # TRAIN MODELS
    # ========================================================

    def train_models_ui(self):

        if self.data is None:

            messagebox.showwarning(
                "Dataset Required",
                "Please load a dataset first."
            )

            return

        try:

            self.root.config(
                cursor="watch"
            )

            self.root.update()

            (
                self.X_train,
                self.X_test,
                self.y_train,
                self.y_test,
                self.preprocessor,
                _,
                _
            ) = prepare_data(
                self.data
            )

            models = create_models(
                self.preprocessor
            )

            (
                self.trained_models,
                self.results_df
            ) = train_models(
                models,
                self.X_train,
                self.y_train,
                self.X_test,
                self.y_test
            )

            self.best_model_name = (
                self.results_df.iloc[0]["Model"]
            )

            self.best_model = (
                self.trained_models[
                    self.best_model_name
                ]
            )

            save_best_model(
                self.trained_models,
                self.results_df
            )

            self.feature_df = (
                get_feature_importance(
                    self.best_model
                )
            )

            os.makedirs(
                "outputs",
                exist_ok=True
            )

            self.results_df.to_csv(
                "outputs/model_comparison.csv",
                index=False
            )

            self.feature_df.to_csv(
                "outputs/feature_importance.csv",
                index=False
            )

            self.root.config(
                cursor=""
            )

            messagebox.showinfo(
                "Training Complete",
                (
                    f"All 4 models trained successfully.\n\n"
                    f"Best Model:\n"
                    f"{self.best_model_name}\n\n"
                    f"ROC-AUC:\n"
                    f"{self.results_df.iloc[0]['ROC-AUC']:.4f}"
                )
            )

            self.show_dashboard()

        except Exception as error:

            self.root.config(
                cursor=""
            )

            messagebox.showerror(
                "Training Error",
                str(error)
            )

    # ========================================================
    # EMPTY STATE
    # ========================================================

    def empty_state(
        self,
        title,
        message
    ):

        card = self.create_card(
            self.content_frame
        )

        card.pack(
            fill="both",
            expand=True,
            pady=10
        )

        tk.Label(
            card,
            text=title,
            bg=self.card,
            fg=self.white,
            font=(
                "Segoe UI",
                20,
                "bold"
            )
        ).pack(
            pady=(150, 10)
        )

        tk.Label(
            card,
            text=message,
            bg=self.card,
            fg=self.gray,
            font=(
                "Segoe UI",
                10
            )
        ).pack()


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":

    root = tk.Tk()

    app = CustomerChurnApp(
        root
    )

    root.mainloop()