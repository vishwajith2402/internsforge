
import numpy as np
import pandas as pd

from statsmodels.tsa.arima.model import ARIMA


# ==========================================================
# MOVING AVERAGE
# ==========================================================

def moving_average_forecast(
    sales,
    forecast_days,
    window=7
):

    sales = np.asarray(
        sales,
        dtype=float
    )

    if len(sales) == 0:
        raise ValueError(
            "No sales data available."
        )

    window = min(
        window,
        len(sales)
    )

    average = np.mean(
        sales[-window:]
    )

    forecast = np.repeat(
        average,
        forecast_days
    )

    return forecast


# ==========================================================
# ARIMA
# ==========================================================

def arima_forecast(
    sales,
    forecast_days
):

    sales = np.asarray(
        sales,
        dtype=float
    )

    if len(sales) < 10:

        return moving_average_forecast(
            sales,
            forecast_days
        )

    try:

        model = ARIMA(
            sales,
            order=(5, 1, 0)
        )

        fitted_model = model.fit()

        forecast = fitted_model.forecast(
            steps=forecast_days
        )

        return np.asarray(
            forecast,
            dtype=float
        )

    except Exception:

        return moving_average_forecast(
            sales,
            forecast_days
        )


# ==========================================================
# SARIMA
# ==========================================================

def sarima_forecast(
    sales,
    forecast_days
):

    sales = np.asarray(
        sales,
        dtype=float
    )

    if len(sales) < 30:

        return arima_forecast(
            sales,
            forecast_days
        )

    try:

        from statsmodels.tsa.statespace.sarimax import SARIMAX

        model = SARIMAX(
            sales,
            order=(1, 1, 1),
            seasonal_order=(1, 1, 1, 7),
            enforce_stationarity=False,
            enforce_invertibility=False
        )

        fitted_model = model.fit(
            disp=False
        )

        forecast = fitted_model.forecast(
            steps=forecast_days
        )

        return np.asarray(
            forecast,
            dtype=float
        )

    except Exception:

        return arima_forecast(
            sales,
            forecast_days
        )


# ==========================================================
# RANDOM FOREST
# ==========================================================

def random_forest_forecast(
    sales,
    forecast_days
):

    from sklearn.ensemble import RandomForestRegressor

    sales = np.asarray(
        sales,
        dtype=float
    )

    if len(sales) < 15:

        return moving_average_forecast(
            sales,
            forecast_days
        )

    # ------------------------------------------
    # Create lag features
    # ------------------------------------------

    lag = 7

    X = []
    y = []

    for i in range(
        lag,
        len(sales)
    ):

        X.append(
            sales[
                i - lag:i
            ]
        )

        y.append(
            sales[i]
        )

    X = np.asarray(X)
    y = np.asarray(y)

    model = RandomForestRegressor(
        n_estimators=200,
        random_state=42,
        max_depth=10
    )

    model.fit(
        X,
        y
    )

    # ------------------------------------------
    # Recursive forecasting
    # ------------------------------------------

    history = list(
        sales[-lag:]
    )

    predictions = []

    for _ in range(
        forecast_days
    ):

        features = np.asarray(
            history[-lag:]
        ).reshape(
            1,
            -1
        )

        prediction = model.predict(
            features
        )[0]

        prediction = max(
            0,
            prediction
        )

        predictions.append(
            prediction
        )

        history.append(
            prediction
        )

    return np.asarray(
        predictions
    )


# ==========================================================
# MAIN FORECAST FUNCTION
# ==========================================================

def generate_forecast(
    daily_df,
    model_name,
    forecast_days
):

    if daily_df is None:

        raise ValueError(
            "Daily sales data is not available."
        )

    if len(daily_df) == 0:

        raise ValueError(
            "No sales data available."
        )

    sales = (
        daily_df["Sales"]
        .astype(float)
        .values
    )

    # ------------------------------------------
    # Select model
    # ------------------------------------------

    if model_name == "Moving Average":

        predictions = moving_average_forecast(
            sales,
            forecast_days
        )

    elif model_name == "ARIMA":

        predictions = arima_forecast(
            sales,
            forecast_days
        )

    elif model_name == "SARIMA":

        predictions = sarima_forecast(
            sales,
            forecast_days
        )

    elif model_name == "Random Forest":

        predictions = random_forest_forecast(
            sales,
            forecast_days
        )

    else:

        raise ValueError(
            f"Unknown forecasting model: {model_name}"
        )

    # ------------------------------------------
    # Future dates
    # ------------------------------------------

    last_date = pd.to_datetime(
        daily_df["Date"]
    ).max()

    future_dates = pd.date_range(
        start=last_date + pd.Timedelta(days=1),
        periods=forecast_days,
        freq="D"
    )

    forecast_df = pd.DataFrame({
        "Date": future_dates,
        "Forecast": predictions
    })

    # Prevent negative sales
    forecast_df["Forecast"] = (
        forecast_df["Forecast"]
        .clip(lower=0)
    )

    return forecast_df
