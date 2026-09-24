import numpy as np
import pandas as pd

from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error

from statsmodels.tsa.arima.model import ARIMA


# ==========================================================
# MOVING AVERAGE
# ==========================================================

def moving_average_predict(
    train,
    test,
    window=7
):

    train = np.asarray(
        train,
        dtype=float
    )

    window = min(
        window,
        len(train)
    )

    prediction = np.mean(
        train[-window:]
    )

    return np.repeat(
        prediction,
        len(test)
    )


# ==========================================================
# ARIMA
# ==========================================================

def arima_predict(
    train,
    test
):

    train = np.asarray(
        train,
        dtype=float
    )

    if len(train) < 10:

        return moving_average_predict(
            train,
            test
        )

    try:

        model = ARIMA(
            train,
            order=(5, 1, 0)
        )

        fitted = model.fit()

        predictions = fitted.forecast(
            steps=len(test)
        )

        return np.asarray(
            predictions,
            dtype=float
        )

    except Exception:

        return moving_average_predict(
            train,
            test
        )


# ==========================================================
# SARIMA
# ==========================================================

def sarima_predict(
    train,
    test
):

    train = np.asarray(
        train,
        dtype=float
    )

    if len(train) < 30:

        return arima_predict(
            train,
            test
        )

    try:

        from statsmodels.tsa.statespace.sarimax import SARIMAX

        model = SARIMAX(
            train,
            order=(1, 1, 1),
            seasonal_order=(1, 1, 1, 7),
            enforce_stationarity=False,
            enforce_invertibility=False
        )

        fitted = model.fit(
            disp=False
        )

        predictions = fitted.forecast(
            steps=len(test)
        )

        return np.asarray(
            predictions,
            dtype=float
        )

    except Exception:

        return arima_predict(
            train,
            test
        )


# ==========================================================
# RANDOM FOREST
# ==========================================================

def create_lag_dataset(
    values,
    lag=7
):

    X = []
    y = []

    for i in range(
        lag,
        len(values)
    ):

        X.append(
            values[
                i - lag:i
            ]
        )

        y.append(
            values[i]
        )

    return (
        np.asarray(X),
        np.asarray(y)
    )


def random_forest_predict(
    train,
    test,
    lag=7
):

    train = np.asarray(
        train,
        dtype=float
    )

    if len(train) <= lag:

        return moving_average_predict(
            train,
            test
        )

    X, y = create_lag_dataset(
        train,
        lag
    )

    model = RandomForestRegressor(
        n_estimators=200,
        max_depth=10,
        random_state=42,
        n_jobs=-1
    )

    model.fit(
        X,
        y
    )

    history = list(
        train[-lag:]
    )

    predictions = []

    for _ in range(
        len(test)
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
# MAPE
# ==========================================================

def calculate_mape(
    actual,
    predicted
):

    actual = np.asarray(
        actual,
        dtype=float
    )

    predicted = np.asarray(
        predicted,
        dtype=float
    )

    mask = actual != 0

    if not np.any(mask):
        return np.nan

    return (
        np.mean(
            np.abs(
                (
                    actual[mask]
                    -
                    predicted[mask]
                )
                /
                actual[mask]
            )
        )
        * 100
    )


# ==========================================================
# EVALUATE MODEL
# ==========================================================

def evaluate_model(
    actual,
    predicted
):

    actual = np.asarray(
        actual,
        dtype=float
    )

    predicted = np.asarray(
        predicted,
        dtype=float
    )

    mae = mean_absolute_error(
        actual,
        predicted
    )

    rmse = np.sqrt(
        mean_squared_error(
            actual,
            predicted
        )
    )

    mape = calculate_mape(
        actual,
        predicted
    )

    return mae, rmse, mape


# ==========================================================
# COMPARE MODELS
# ==========================================================

def compare_models(
    sales,
    test_size=0.2
):

    sales = np.asarray(
        sales,
        dtype=float
    )

    sales = sales[
        np.isfinite(sales)
    ]

    if len(sales) < 20:

        raise ValueError(
            "At least 20 daily sales records are required "
            "for model comparison."
        )

    # ------------------------------------------------------
    # Train / test split
    # ------------------------------------------------------

    split_index = int(
        len(sales) * (1 - test_size)
    )

    # Make sure both sets have data
    split_index = max(
        10,
        min(
            split_index,
            len(sales) - 1
        )
    )

    train = sales[
        :split_index
    ]

    test = sales[
        split_index:
    ]

    results = []

    # ------------------------------------------------------
    # Moving Average
    # ------------------------------------------------------

    try:

        prediction = moving_average_predict(
            train,
            test
        )

        mae, rmse, mape = evaluate_model(
            test,
            prediction
        )

        results.append({
            "Model": "Moving Average",
            "MAE": mae,
            "RMSE": rmse,
            "MAPE": mape
        })

    except Exception:

        results.append({
            "Model": "Moving Average",
            "MAE": np.nan,
            "RMSE": np.nan,
            "MAPE": np.nan
        })

    # ------------------------------------------------------
    # ARIMA
    # ------------------------------------------------------

    try:

        prediction = arima_predict(
            train,
            test
        )

        mae, rmse, mape = evaluate_model(
            test,
            prediction
        )

        results.append({
            "Model": "ARIMA",
            "MAE": mae,
            "RMSE": rmse,
            "MAPE": mape
        })

    except Exception:

        results.append({
            "Model": "ARIMA",
            "MAE": np.nan,
            "RMSE": np.nan,
            "MAPE": np.nan
        })

    # ------------------------------------------------------
    # SARIMA
    # ------------------------------------------------------

    try:

        prediction = sarima_predict(
            train,
            test
        )

        mae, rmse, mape = evaluate_model(
            test,
            prediction
        )

        results.append({
            "Model": "SARIMA",
            "MAE": mae,
            "RMSE": rmse,
            "MAPE": mape
        })

    except Exception:

        results.append({
            "Model": "SARIMA",
            "MAE": np.nan,
            "RMSE": np.nan,
            "MAPE": np.nan
        })

    # ------------------------------------------------------
    # Random Forest
    # ------------------------------------------------------

    try:

        prediction = random_forest_predict(
            train,
            test
        )

        mae, rmse, mape = evaluate_model(
            test,
            prediction
        )

        results.append({
            "Model": "Random Forest",
            "MAE": mae,
            "RMSE": rmse,
            "MAPE": mape
        })

    except Exception:

        results.append({
            "Model": "Random Forest",
            "MAE": np.nan,
            "RMSE": np.nan,
            "MAPE": np.nan
        })

    # ------------------------------------------------------
    # DataFrame
    # ------------------------------------------------------

    results_df = pd.DataFrame(
        results
    )

    results_df = results_df.sort_values(
        "MAE",
        na_position="last"
    ).reset_index(
        drop=True
    )

    return results_df


# ==========================================================
# BEST MODEL
# ==========================================================

def get_best_model(
    results
):

    valid = results.dropna(
        subset=["MAE"]
    )

    if valid.empty:

        return None

    return valid.iloc[0]["Model"]
