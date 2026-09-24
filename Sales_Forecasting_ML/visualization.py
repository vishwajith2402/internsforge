import matplotlib.pyplot as plt
import matplotlib.dates as mdates


def prepare_axis(ax):
    ax.set_facecolor("#111827")

    ax.tick_params(
        colors="#CBD5E1",
        labelsize=9
    )

    ax.xaxis.label.set_color("#CBD5E1")
    ax.yaxis.label.set_color("#CBD5E1")

    for spine in ax.spines.values():
        spine.set_color("#334155")

    ax.grid(
        True,
        alpha=0.15
    )


def plot_sales_trend(ax, df, title="Sales Trend"):

    ax.clear()

    prepare_axis(ax)

    ax.plot(
        df["Date"],
        df["Sales"],
        linewidth=2
    )

    ax.set_title(
        title,
        color="#F8FAFC",
        fontsize=14,
        fontweight="bold"
    )

    ax.set_xlabel("Date")
    ax.set_ylabel("Sales")

    ax.tick_params(
        axis="x",
        rotation=45
    )


def plot_forecast(
    ax,
    historical,
    forecast,
    model_name
):

    ax.clear()

    prepare_axis(ax)

    ax.plot(
        historical["Date"],
        historical["Sales"],
        label="Historical",
        linewidth=2
    )

    ax.plot(
        forecast["Date"],
        forecast["Forecast"],
        label=f"{model_name} Forecast",
        linewidth=2,
        linestyle="--"
    )

    ax.axvline(
        historical["Date"].iloc[-1],
        linestyle=":",
        linewidth=1.5,
        label="Forecast Start"
    )

    ax.set_title(
        f"Sales Forecast — {model_name}",
        color="#F8FAFC",
        fontsize=14,
        fontweight="bold"
    )

    ax.set_xlabel("Date")
    ax.set_ylabel("Sales")

    ax.legend(
        facecolor="#111827",
        labelcolor="#F8FAFC"
    )

    ax.tick_params(
        axis="x",
        rotation=45
    )


def plot_monthly_sales(ax, monthly_df):

    ax.clear()

    prepare_axis(ax)

    ax.bar(
        monthly_df["Date"],
        monthly_df["Sales"],
        width=20
    )

    ax.set_title(
        "Monthly Sales",
        color="#F8FAFC",
        fontsize=14,
        fontweight="bold"
    )

    ax.set_xlabel("Month")
    ax.set_ylabel("Sales")

    ax.tick_params(
        axis="x",
        rotation=45
    )


def plot_yearly_sales(ax, yearly_df):

    ax.clear()

    prepare_axis(ax)

    ax.bar(
        yearly_df["Year"].astype(str),
        yearly_df["Sales"]
    )

    ax.set_title(
        "Yearly Sales",
        color="#F8FAFC",
        fontsize=14,
        fontweight="bold"
    )

    ax.set_xlabel("Year")
    ax.set_ylabel("Sales")


def plot_store_sales(ax, df):

    ax.clear()

    prepare_axis(ax)

    store_sales = (
        df.groupby("Store")["Sales"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
    )

    ax.barh(
        store_sales.index[::-1],
        store_sales.values[::-1]
    )

    ax.set_title(
        "Top Stores by Sales",
        color="#F8FAFC",
        fontsize=14,
        fontweight="bold"
    )

    ax.set_xlabel("Sales")
    ax.set_ylabel("Store")


def plot_product_sales(ax, df):

    ax.clear()

    prepare_axis(ax)

    product_sales = (
        df.groupby("Product")["Sales"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
    )

    ax.barh(
        product_sales.index[::-1],
        product_sales.values[::-1]
    )

    ax.set_title(
        "Top Products by Sales",
        color="#F8FAFC",
        fontsize=14,
        fontweight="bold"
    )

    ax.set_xlabel("Sales")
    ax.set_ylabel("Product")


def plot_discount_vs_sales(ax, df):

    ax.clear()

    prepare_axis(ax)

    ax.scatter(
        df["Discount"],
        df["Sales"],
        alpha=0.6
    )

    ax.set_title(
        "Discount vs Sales",
        color="#F8FAFC",
        fontsize=14,
        fontweight="bold"
    )

    ax.set_xlabel("Discount")
    ax.set_ylabel("Sales")


def plot_holiday_sales(ax, df):

    ax.clear()

    prepare_axis(ax)

    holiday_sales = (
        df.groupby("Holiday")["Sales"]
        .mean()
    )

    labels = [
        "Non-Holiday",
        "Holiday"
    ]

    values = [
        holiday_sales.get(0, 0),
        holiday_sales.get(1, 0)
    ]

    ax.bar(
        labels,
        values
    )

    ax.set_title(
        "Average Sales: Holiday Impact",
        color="#F8FAFC",
        fontsize=14,
        fontweight="bold"
    )

    ax.set_ylabel("Average Sales")


def plot_model_comparison(ax, results):

    ax.clear()

    prepare_axis(ax)

    valid = results.dropna(
        subset=["MAE"]
    )

    ax.bar(
        valid["Model"],
        valid["MAE"]
    )

    ax.set_title(
        "Model Comparison — MAE",
        color="#F8FAFC",
        fontsize=14,
        fontweight="bold"
    )

    ax.set_ylabel("MAE")

    ax.tick_params(
        axis="x",
        rotation=25
    )

