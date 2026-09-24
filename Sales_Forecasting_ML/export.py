
import os
import pandas as pd


# ==========================================================
# CREATE OUTPUT DIRECTORY
# ==========================================================

def ensure_directory(file_path):

    directory = os.path.dirname(
        os.path.abspath(file_path)
    )

    if directory:
        os.makedirs(
            directory,
            exist_ok=True
        )


# ==========================================================
# EXPORT FORECAST TO CSV
# ==========================================================

def export_forecast_csv(
    forecast,
    output_path
):

    if forecast is None:
        raise ValueError(
            "No forecast data available."
        )

    ensure_directory(
        output_path
    )

    forecast.to_csv(
        output_path,
        index=False
    )


# ==========================================================
# EXPORT FORECAST TO EXCEL
# ==========================================================

def export_forecast_excel(
    forecast,
    output_path
):

    if forecast is None:
        raise ValueError(
            "No forecast data available."
        )

    ensure_directory(
        output_path
    )

    forecast.to_excel(
        output_path,
        index=False,
        sheet_name="Forecast"
    )


# ==========================================================
# EXPORT COMPLETE ANALYSIS
# ==========================================================

def export_analysis_excel(
    daily,
    monthly,
    yearly,
    product_summary,
    store_summary,
    output_path
):

    ensure_directory(
        output_path
    )

    with pd.ExcelWriter(
        output_path,
        engine="openpyxl"
    ) as writer:

        if daily is not None:

            daily.to_excel(
                writer,
                sheet_name="Daily Sales",
                index=False
            )

        if monthly is not None:

            monthly.to_excel(
                writer,
                sheet_name="Monthly Sales",
                index=False
            )

        if yearly is not None:

            yearly.to_excel(
                writer,
                sheet_name="Yearly Sales",
                index=False
            )

        if product_summary is not None:

            product_summary.to_excel(
                writer,
                sheet_name="Products",
                index=False
            )

        if store_summary is not None:

            store_summary.to_excel(
                writer,
                sheet_name="Stores",
                index=False
            )


# ==========================================================
# EXPORT MODEL RESULTS
# ==========================================================

def export_model_results(
    results,
    output_path
):

    if results is None:
        raise ValueError(
            "No model results available."
        )

    ensure_directory(
        output_path
    )

    results.to_excel(
        output_path,
        index=False,
        sheet_name="Model Results"
    )


# ==========================================================
# EXPORT EVERYTHING
# ==========================================================

def export_complete_report(
    daily,
    monthly,
    yearly,
    product_summary,
    store_summary,
    model_results,
    forecast,
    output_path
):

    ensure_directory(
        output_path
    )

    with pd.ExcelWriter(
        output_path,
        engine="openpyxl"
    ) as writer:

        if daily is not None:

            daily.to_excel(
                writer,
                sheet_name="Daily Sales",
                index=False
            )

        if monthly is not None:

            monthly.to_excel(
                writer,
                sheet_name="Monthly Sales",
                index=False
            )

        if yearly is not None:

            yearly.to_excel(
                writer,
                sheet_name="Yearly Sales",
                index=False
            )

        if product_summary is not None:

            product_summary.to_excel(
                writer,
                sheet_name="Products",
                index=False
            )

        if store_summary is not None:

            store_summary.to_excel(
                writer,
                sheet_name="Stores",
                index=False
            )

        if model_results is not None:

            model_results.to_excel(
                writer,
                sheet_name="Model Results",
                index=False
            )

        if forecast is not None:

            forecast.to_excel(
                writer,
                sheet_name="Forecast",
                index=False
            )
