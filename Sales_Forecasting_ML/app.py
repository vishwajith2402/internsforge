import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

import pandas as pd
import matplotlib.pyplot as plt

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from preprocessing import (
    load_data,
    prepare_daily_data,
    prepare_monthly_data,
    prepare_yearly_data,
    prepare_product_summary,
    prepare_store_summary,
    prepare_holiday_summary
)

from forecasting import generate_forecast

from models import compare_models

from visualization import (
    plot_sales_trend,
    plot_monthly_sales,
    plot_yearly_sales,
    plot_store_sales,
    plot_product_sales,
    plot_discount_vs_sales,
    plot_holiday_sales,
    plot_forecast,
    plot_model_comparison
)

from export import (
    export_forecast_csv,
    export_forecast_excel,
    export_analysis_excel
)


# ==========================================================
# COLORS
# ==========================================================

BG = "#0B0F19"
SIDEBAR = "#0F172A"
CARD = "#111827"
CARD2 = "#1E293B"

TEXT = "#F8FAFC"
MUTED = "#94A3B8"

CYAN = "#22D3EE"
PURPLE = "#8B5CF6"
GREEN = "#22C55E"
RED = "#EF4444"


# ==========================================================
# APPLICATION
# ==========================================================

class SalesForecastingApp:

    def __init__(self, root):

        self.root = root

        self.root.title(
            "Sales Forecasting ML System"
        )

        self.root.geometry(
            "1450x900"
        )

        self.root.minsize(
            1150,
            700
        )

        self.root.configure(
            bg=BG
        )

        self.df = None
        self.daily_df = None
        self.monthly_df = None
        self.yearly_df = None

        self.product_summary = None
        self.store_summary = None

        self.current_forecast = None
        self.comparison_results = None

        self.setup_style()

        self.create_header()

        self.create_sidebar()

        self.create_main_area()

        self.show_overview()


    # ======================================================
    # STYLE
    # ======================================================

    def setup_style(self):

        style = ttk.Style()

        try:
            style.theme_use("clam")
        except Exception:
            pass

        style.configure(
            "Treeview",
            background=CARD,
            foreground=TEXT,
            fieldbackground=CARD,
            rowheight=30,
            font=("Segoe UI", 9)
        )

        style.configure(
            "Treeview.Heading",
            background=CARD2,
            foreground=TEXT,
            font=("Segoe UI", 9, "bold")
        )

        style.map(
            "Treeview",
            background=[
                ("selected", PURPLE)
            ]
        )

        style.configure(
            "TCombobox",
            fieldbackground=CARD2,
            background=CARD2,
            foreground=TEXT
        )


    # ======================================================
    # HEADER
    # ======================================================

    def create_header(self):

        header = tk.Frame(
            self.root,
            bg=BG,
            height=90
        )

        header.pack(
            fill="x",
            padx=25,
            pady=(18, 5)
        )

        tk.Label(
            header,
            text="SALES FORECASTING",
            font=("Segoe UI", 26, "bold"),
            fg=TEXT,
            bg=BG
        ).pack(
            anchor="w"
        )

        tk.Label(
            header,
            text="Machine Learning • Time-Series Analytics • Business Intelligence",
            font=("Segoe UI", 10),
            fg=CYAN,
            bg=BG
        ).pack(
            anchor="w"
        )


    # ======================================================
    # SIDEBAR
    # ======================================================

    def create_sidebar(self):

        self.sidebar = tk.Frame(
            self.root,
            bg=SIDEBAR,
            width=245
        )

        self.sidebar.pack(
            side="left",
            fill="y",
            padx=(25, 10),
            pady=10
        )

        self.sidebar.pack_propagate(False)

        tk.Label(
            self.sidebar,
            text="NAVIGATION",
            font=("Segoe UI", 9, "bold"),
            fg=MUTED,
            bg=SIDEBAR
        ).pack(
            anchor="w",
            padx=20,
            pady=(20, 12)
        )

        self.nav_buttons = {}

        navigation = [
            ("Overview", self.show_overview),
            ("Trends", self.show_trends),
            ("Products", self.show_products),
            ("Stores", self.show_stores),
            ("Forecast", self.show_forecast),
            ("ML Models", self.show_models)
        ]

        for name, command in navigation:

            button = tk.Button(
                self.sidebar,
                text=name,
                command=command,
                bg=SIDEBAR,
                fg=TEXT,
                activebackground=CARD2,
                activeforeground=CYAN,
                relief="flat",
                anchor="w",
                font=("Segoe UI", 10, "bold"),
                padx=20,
                pady=11,
                cursor="hand2"
            )

            button.pack(
                fill="x",
                padx=10,
                pady=2
            )

            self.nav_buttons[name] = button

        # ----------------------------------------------
        # DATASET SECTION
        # ----------------------------------------------

        tk.Label(
            self.sidebar,
            text="DATASET",
            font=("Segoe UI", 9, "bold"),
            fg=MUTED,
            bg=SIDEBAR
        ).pack(
            anchor="w",
            padx=20,
            pady=(30, 5)
        )

        self.file_label = tk.Label(
            self.sidebar,
            text="No dataset loaded",
            font=("Segoe UI", 9),
            fg=TEXT,
            bg=SIDEBAR,
            wraplength=200,
            justify="left"
        )

        self.file_label.pack(
            anchor="w",
            padx=20,
            pady=5
        )

        tk.Button(
            self.sidebar,
            text="LOAD CSV",
            command=self.load_dataset,
            bg=PURPLE,
            fg="white",
            activebackground=PURPLE,
            activeforeground="white",
            relief="flat",
            font=("Segoe UI", 9, "bold"),
            padx=10,
            pady=9,
            cursor="hand2"
        ).pack(
            fill="x",
            padx=20,
            pady=10
        )

        # ----------------------------------------------
        # EXPORT
        # ----------------------------------------------

        tk.Button(
            self.sidebar,
            text="EXPORT ANALYSIS",
            command=self.export_analysis,
            bg=CARD2,
            fg=TEXT,
            activebackground=PURPLE,
            activeforeground="white",
            relief="flat",
            font=("Segoe UI", 9, "bold"),
            padx=10,
            pady=9,
            cursor="hand2"
        ).pack(
            fill="x",
            padx=20,
            pady=4
        )


    # ======================================================
    # MAIN AREA
    # ======================================================

    def create_main_area(self):

        self.main = tk.Frame(
            self.root,
            bg=BG
        )

        self.main.pack(
            side="right",
            fill="both",
            expand=True,
            padx=(10, 25),
            pady=10
        )

    # ======================================================
    # CLEAR MAIN
    # ======================================================

    def clear_main(self):

        for widget in self.main.winfo_children():
            widget.destroy()


    # ======================================================
    # PAGE TITLE
    # ======================================================

    def page_title(
        self,
        title,
        description
    ):

        tk.Label(
            self.main,
            text=title,
            font=("Segoe UI", 20, "bold"),
            fg=TEXT,
            bg=BG
        ).pack(
            anchor="w"
        )

        tk.Label(
            self.main,
            text=description,
            font=("Segoe UI", 9),
            fg=MUTED,
            bg=BG
        ).pack(
            anchor="w",
            pady=(2, 12)
        )


    # ======================================================
    # OVERVIEW
    # ======================================================

    def show_overview(self):

        self.clear_main()

        self.page_title(
            "Overview",
            "Business-level summary of your sales dataset"
        )

        if self.df is None:

            self.show_empty_state()

            return

        # --------------------------------------------------
        # KPI CARDS
        # --------------------------------------------------

        cards = tk.Frame(
            self.main,
            bg=BG
        )

        cards.pack(
            fill="x"
        )

        total_sales = self.df["Sales"].sum()

        total_revenue = self.df["Revenue"].sum()

        avg_sales = self.daily_df["Sales"].mean()

        transactions = len(self.df)

        kpis = [
            ("TOTAL SALES", f"{total_sales:,.0f}"),
            ("TOTAL REVENUE", f"₹{total_revenue:,.0f}"),
            ("AVG DAILY SALES", f"{avg_sales:,.2f}"),
            ("TRANSACTIONS", f"{transactions:,}")
        ]

        for title, value in kpis:

            card = tk.Frame(
                cards,
                bg=CARD,
                height=105
            )

            card.pack(
                side="left",
                fill="x",
                expand=True,
                padx=5
            )

            tk.Label(
                card,
                text=title,
                font=("Segoe UI", 8, "bold"),
                fg=MUTED,
                bg=CARD
            ).pack(
                anchor="w",
                padx=16,
                pady=(15, 3)
            )

            tk.Label(
                card,
                text=value,
                font=("Segoe UI", 18, "bold"),
                fg=CYAN,
                bg=CARD
            ).pack(
                anchor="w",
                padx=16
            )

        # --------------------------------------------------
        # CHART
        # --------------------------------------------------

        chart_frame = tk.Frame(
            self.main,
            bg=CARD
        )

        chart_frame.pack(
            fill="both",
            expand=True,
            pady=12
        )

        fig, ax = plt.subplots(
            figsize=(9, 5)
        )

        fig.patch.set_facecolor(CARD)

        plot_sales_trend(
            ax,
            self.daily_df,
            "Historical Sales Trend"
        )

        canvas = FigureCanvasTkAgg(
            fig,
            chart_frame
        )

        canvas.draw()

        canvas.get_tk_widget().pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

        plt.close(fig)


    # ======================================================
    # TRENDS
    # ======================================================

    def show_trends(self):

        if not self.check_dataset():
            return

        self.clear_main()

        self.page_title(
            "Sales Trends",
            "Daily, monthly, yearly and business-factor analysis"
        )

        container = tk.Frame(
            self.main,
            bg=BG
        )

        container.pack(
            fill="both",
            expand=True
        )

        # Left
        left = tk.Frame(
            container,
            bg=CARD
        )

        left.pack(
            side="left",
            fill="both",
            expand=True,
            padx=(0, 6)
        )

        # Right
        right = tk.Frame(
            container,
            bg=CARD
        )

        right.pack(
            side="right",
            fill="both",
            expand=True,
            padx=(6, 0)
        )

        fig1, ax1 = plt.subplots(
            figsize=(6, 4)
        )

        fig1.patch.set_facecolor(CARD)

        plot_monthly_sales(
            ax1,
            self.monthly_df
        )

        canvas1 = FigureCanvasTkAgg(
            fig1,
            left
        )

        canvas1.draw()

        canvas1.get_tk_widget().pack(
            fill="both",
            expand=True
        )

        plt.close(fig1)

        fig2, ax2 = plt.subplots(
            figsize=(6, 4)
        )

        fig2.patch.set_facecolor(CARD)

        plot_discount_vs_sales(
            ax2,
            self.df
        )

        canvas2 = FigureCanvasTkAgg(
            fig2,
            right
        )

        canvas2.draw()

        canvas2.get_tk_widget().pack(
            fill="both",
            expand=True
        )

        plt.close(fig2)


    # ======================================================
    # PRODUCTS
    # ======================================================

    def show_products(self):

        if not self.check_dataset():
            return

        self.clear_main()

        self.page_title(
            "Product Analytics",
            "Identify the strongest products by sales and revenue"
        )

        container = tk.Frame(
            self.main,
            bg=BG
        )

        container.pack(
            fill="both",
            expand=True
        )

        chart_frame = tk.Frame(
            container,
            bg=CARD
        )

        chart_frame.pack(
            side="left",
            fill="both",
            expand=True,
            padx=(0, 6)
        )

        table_frame = tk.Frame(
            container,
            bg=CARD
        )

        table_frame.pack(
            side="right",
            fill="both",
            expand=True,
            padx=(6, 0)
        )

        fig, ax = plt.subplots(
            figsize=(6, 5)
        )

        fig.patch.set_facecolor(CARD)

        plot_product_sales(
            ax,
            self.df
        )

        canvas = FigureCanvasTkAgg(
            fig,
            chart_frame
        )

        canvas.draw()

        canvas.get_tk_widget().pack(
            fill="both",
            expand=True
        )

        plt.close(fig)

        self.create_table(
            table_frame,
            self.product_summary,
            [
                "Product",
                "Sales",
                "Revenue",
                "Average_Discount",
                "Transactions"
            ]
        )


    # ======================================================
    # STORES
    # ======================================================

    def show_stores(self):

        if not self.check_dataset():
            return

        self.clear_main()

        self.page_title(
            "Store Analytics",
            "Compare store performance and revenue contribution"
        )

        container = tk.Frame(
            self.main,
            bg=BG
        )

        container.pack(
            fill="both",
            expand=True
        )

        chart_frame = tk.Frame(
            container,
            bg=CARD
        )

        chart_frame.pack(
            side="left",
            fill="both",
            expand=True,
            padx=(0, 6)
        )

        table_frame = tk.Frame(
            container,
            bg=CARD
        )

        table_frame.pack(
            side="right",
            fill="both",
            expand=True,
            padx=(6, 0)
        )

        fig, ax = plt.subplots(
            figsize=(6, 5)
        )

        fig.patch.set_facecolor(CARD)

        plot_store_sales(
            ax,
            self.df
        )

        canvas = FigureCanvasTkAgg(
            fig,
            chart_frame
        )

        canvas.draw()

        canvas.get_tk_widget().pack(
            fill="both",
            expand=True
        )

        plt.close(fig)

        self.create_table(
            table_frame,
            self.store_summary,
            [
                "Store",
                "Sales",
                "Revenue",
                "Average_Discount",
                "Transactions"
            ]
        )


    # ======================================================
    # FORECAST
    # ======================================================

    def show_forecast(self):

        if not self.check_dataset():
            return

        self.clear_main()

        self.page_title(
            "Sales Forecast",
            "Generate future sales predictions using machine learning"
        )

        controls = tk.Frame(
            self.main,
            bg=CARD
        )

        controls.pack(
            fill="x",
            pady=(0, 10)
        )

        tk.Label(
            controls,
            text="MODEL",
            font=("Segoe UI", 9, "bold"),
            fg=MUTED,
            bg=CARD
        ).pack(
            side="left",
            padx=(15, 5),
            pady=15
        )

        self.forecast_model = tk.StringVar(
            value="Moving Average"
        )

        combo = ttk.Combobox(
            controls,
            textvariable=self.forecast_model,
            values=[
                "Moving Average",
                "ARIMA",
                "SARIMA",
                "Random Forest"
            ],
            state="readonly",
            width=18
        )

        combo.pack(
            side="left",
            padx=5
        )

        tk.Label(
            controls,
            text="DAYS",
            font=("Segoe UI", 9, "bold"),
            fg=MUTED,
            bg=CARD
        ).pack(
            side="left",
            padx=(20, 5)
        )

        self.forecast_days = tk.Entry(
            controls,
            bg=CARD2,
            fg=TEXT,
            insertbackground=TEXT,
            relief="flat",
            width=10
        )

        self.forecast_days.insert(
            0,
            "30"
        )

        self.forecast_days.pack(
            side="left",
            padx=5
        )

        tk.Button(
            controls,
            text="GENERATE",
            command=self.run_forecast,
            bg=CYAN,
            fg="#001018",
            relief="flat",
            font=("Segoe UI", 9, "bold"),
            padx=15,
            pady=8,
            cursor="hand2"
        ).pack(
            side="left",
            padx=15
        )

        tk.Button(
            controls,
            text="EXPORT CSV",
            command=self.export_forecast_csv,
            bg=CARD2,
            fg=TEXT,
            relief="flat",
            font=("Segoe UI", 9, "bold"),
            padx=12,
            pady=8,
            cursor="hand2"
        ).pack(
            side="left",
            padx=5
        )

        tk.Button(
            controls,
            text="EXPORT EXCEL",
            command=self.export_forecast_excel,
            bg=CARD2,
            fg=TEXT,
            relief="flat",
            font=("Segoe UI", 9, "bold"),
            padx=12,
            pady=8,
            cursor="hand2"
        ).pack(
            side="left",
            padx=5
        )

        self.forecast_chart = tk.Frame(
            self.main,
            bg=CARD
        )

        self.forecast_chart.pack(
            fill="both",
            expand=True
        )

        self.forecast_table = tk.Frame(
            self.main,
            bg=CARD,
            height=170
        )

        self.forecast_table.pack(
            fill="x",
            pady=(8, 0)
        )


    # ======================================================
    # RUN FORECAST
    # ======================================================

    def run_forecast(self):

        try:

            days = int(
                self.forecast_days.get()
            )

            if days <= 0:
                raise ValueError

        except Exception:

            messagebox.showerror(
                "Invalid Input",
                "Enter a valid positive number of days."
            )

            return

        model = self.forecast_model.get()

        try:

            self.root.config(
                cursor="wait"
            )

            self.root.update()

            forecast = generate_forecast(
                self.daily_df,
                model,
                days
            )

            self.current_forecast = forecast

            for widget in self.forecast_chart.winfo_children():
                widget.destroy()

            fig, ax = plt.subplots(
                figsize=(10, 5)
            )

            fig.patch.set_facecolor(CARD)

            plot_forecast(
                ax,
                self.daily_df,
                forecast,
                model
            )

            canvas = FigureCanvasTkAgg(
                fig,
                self.forecast_chart
            )

            canvas.draw()

            canvas.get_tk_widget().pack(
                fill="both",
                expand=True
            )

            plt.close(fig)

            for widget in self.forecast_table.winfo_children():
                widget.destroy()

            self.create_table(
                self.forecast_table,
                forecast,
                ["Date", "Forecast"]
            )

        except Exception as e:

            messagebox.showerror(
                "Forecast Error",
                str(e)
            )

        finally:

            self.root.config(
                cursor=""
            )


    # ======================================================
    # MODELS
    # ======================================================

    def show_models(self):

        if not self.check_dataset():
            return

        self.clear_main()

        self.page_title(
            "Machine Learning Models",
            "Compare forecasting models using MAE, RMSE and MAPE"
        )

        top = tk.Frame(
            self.main,
            bg=CARD
        )

        top.pack(
            fill="x",
            pady=(0, 10)
        )

        tk.Button(
            top,
            text="RUN MODEL COMPARISON",
            command=self.run_model_comparison,
            bg=PURPLE,
            fg="white",
            relief="flat",
            font=("Segoe UI", 9, "bold"),
            padx=15,
            pady=9,
            cursor="hand2"
        ).pack(
            side="left",
            padx=15,
            pady=12
        )

        self.model_chart = tk.Frame(
            self.main,
            bg=CARD
        )

        self.model_chart.pack(
            fill="both",
            expand=True
        )


    # ======================================================
    # MODEL COMPARISON
    # ======================================================

    def run_model_comparison(self):

        try:

            self.root.config(
                cursor="wait"
            )

            self.root.update()

            results = compare_models(
                self.daily_df["Sales"].values
            )

            self.comparison_results = results

            for widget in self.model_chart.winfo_children():
                widget.destroy()

            fig, ax = plt.subplots(
                figsize=(10, 5)
            )

            fig.patch.set_facecolor(CARD)

            plot_model_comparison(
                ax,
                results
            )

            canvas = FigureCanvasTkAgg(
                fig,
                self.model_chart
            )

            canvas.draw()

            canvas.get_tk_widget().pack(
                fill="both",
                expand=True
            )

            plt.close(fig)

            self.show_model_results(
                results
            )

        except Exception as e:

            messagebox.showerror(
                "Model Error",
                str(e)
            )

        finally:

            self.root.config(
                cursor=""
            )


    # ======================================================
    # MODEL RESULTS
    # ======================================================

    def show_model_results(self, results):

        window = tk.Toplevel(
            self.root
        )

        window.title(
            "Model Performance"
        )

        window.geometry(
            "750x450"
        )

        window.configure(
            bg=BG
        )

        tk.Label(
            window,
            text="MODEL PERFORMANCE COMPARISON",
            font=("Segoe UI", 18, "bold"),
            fg=TEXT,
            bg=BG
        ).pack(
            pady=20
        )

        self.create_table(
            window,
            results,
            [
                "Model",
                "MAE",
                "RMSE",
                "MAPE"
            ]
        )


    # ======================================================
    # TABLE
    # ======================================================

    def create_table(
        self,
        parent,
        dataframe,
        columns
    ):

        frame = tk.Frame(
            parent,
            bg=CARD
        )

        frame.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

        tree = ttk.Treeview(
            frame,
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
                width=130,
                anchor="center"
            )

        scrollbar = ttk.Scrollbar(
            frame,
            orient="vertical",
            command=tree.yview
        )

        tree.configure(
            yscrollcommand=scrollbar.set
        )

        scrollbar.pack(
            side="right",
            fill="y"
        )

        tree.pack(
            fill="both",
            expand=True
        )

        if dataframe is None:
            return

        for _, row in dataframe.iterrows():

            values = []

            for column in columns:

                value = row.get(
                    column,
                    ""
                )

                if isinstance(
                    value,
                    float
                ):

                    value = f"{value:,.2f}"

                values.append(
                    value
                )

            tree.insert(
                "",
                "end",
                values=values
            )


    # ======================================================
    # LOAD DATASET
    # ======================================================

    def load_dataset(self):

        path = filedialog.askopenfilename(
            title="Select Sales Dataset",
            filetypes=[
                ("CSV Files", "*.csv"),
                ("All Files", "*.*")
            ]
        )

        if not path:
            return

        try:

            self.df = load_data(
                path
            )

            self.daily_df = prepare_daily_data(
                self.df
            )

            self.monthly_df = prepare_monthly_data(
                self.df
            )

            self.yearly_df = prepare_yearly_data(
                self.df
            )

            self.product_summary = prepare_product_summary(
                self.df
            )

            self.store_summary = prepare_store_summary(
                self.df
            )

            self.file_label.config(
                text=os.path.basename(path)
            )

            self.show_overview()

            messagebox.showinfo(
                "Dataset Loaded",
                (
                    f"Dataset loaded successfully.\n\n"
                    f"Records: {len(self.df):,}\n"
                    f"Date range: "
                    f"{self.df['Date'].min().date()} → "
                    f"{self.df['Date'].max().date()}"
                )
            )

        except Exception as e:

            messagebox.showerror(
                "Dataset Error",
                str(e)
            )


    # ======================================================
    # CHECK DATASET
    # ======================================================

    def check_dataset(self):

        if self.df is None:

            messagebox.showwarning(
                "Dataset Required",
                "Please load a CSV dataset first."
            )

            return False

        return True


    # ======================================================
    # EXPORT FORECAST CSV
    # ======================================================

    def export_forecast_csv(self):

        if self.current_forecast is None:

            messagebox.showwarning(
                "No Forecast",
                "Generate a forecast first."
            )

            return

        path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[
                ("CSV Files", "*.csv")
            ],
            initialfile="sales_forecast.csv"
        )

        if path:

            export_forecast_csv(
                self.current_forecast,
                path
            )

            messagebox.showinfo(
                "Export Complete",
                "Forecast CSV exported successfully."
            )


    # ======================================================
    # EXPORT FORECAST EXCEL
    # ======================================================

    def export_forecast_excel(self):

        if self.current_forecast is None:

            messagebox.showwarning(
                "No Forecast",
                "Generate a forecast first."
            )

            return

        path = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[
                ("Excel Files", "*.xlsx")
            ],
            initialfile="sales_forecast.xlsx"
        )

        if path:

            export_forecast_excel(
                self.current_forecast,
                path
            )

            messagebox.showinfo(
                "Export Complete",
                "Forecast Excel file exported successfully."
            )


    # ======================================================
    # EXPORT ANALYSIS
    # ======================================================

    def export_analysis(self):

        if not self.check_dataset():
            return

        path = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[
                ("Excel Files", "*.xlsx")
            ],
            initialfile="sales_analysis.xlsx"
        )

        if path:

            export_analysis_excel(
                self.daily_df,
                self.monthly_df,
                self.yearly_df,
                self.product_summary,
                self.store_summary,
                path
            )

            messagebox.showinfo(
                "Export Complete",
                "Complete analysis exported successfully." 
            )


    # ======================================================
    # EMPTY STATE
    # ======================================================

    def show_empty_state(self):

        frame = tk.Frame(
            self.main,
            bg=CARD
        )

        frame.pack(
            fill="both",
            expand=True
        )

        tk.Label(
            frame,
            text="NO DATASET LOADED",
            font=("Segoe UI", 20, "bold"),
            fg=TEXT,
            bg=CARD
        ).pack(
            pady=(180, 5)
        )

        tk.Label(
            frame,
            text="Load your sales_data.csv to begin analysis.",
            font=("Segoe UI", 10),
            fg=MUTED,
            bg=CARD
        ).pack()


# ==========================================================
# MAIN
# ==========================================================

if __name__ == "__main__":

    root = tk.Tk()

    app = SalesForecastingApp(
        root
    )

    root.mainloop()
