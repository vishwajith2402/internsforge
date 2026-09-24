# 🏠 House Price Prediction System

## 📌 Project Overview

The House Price Prediction System is a Machine Learning based application that predicts the estimated price of a house using property-related features such as area, number of bedrooms, number of bathrooms, location, and property age.

The project uses supervised learning regression algorithms and provides an interactive Streamlit web application for making predictions.

## 🎯 Objective

To develop a Machine Learning model capable of estimating house prices based on historical property data.

## ❓ Problem Statement

Real estate companies, buyers, and sellers require reliable price estimates before purchasing or selling a property. This project uses historical housing data to build regression models that can estimate the price of a house based on its characteristics.

## 🤖 Machine Learning Type

**Supervised Learning — Regression**

## 🧠 Algorithms Used

* Linear Regression
* Decision Tree Regressor
* Random Forest Regressor

## 📊 Dataset Features

| Feature      | Description                  |
| ------------ | ---------------------------- |
| Area         | Property area in square feet |
| Bedrooms     | Number of bedrooms           |
| Bathrooms    | Number of bathrooms          |
| Location     | Property location            |
| Property Age | Age of the property          |
| Price        | Target house price           |

## ⚙️ Project Workflow

1. Load the dataset
2. Handle missing values
3. Separate features and target
4. Encode categorical variables
5. Split data into training and testing sets
6. Train multiple regression models
7. Generate predictions
8. Evaluate model performance
9. Compare models
10. Select the best-performing model
11. Save the trained model
12. Deploy the prediction system using Streamlit

## 📏 Evaluation Metrics

The models are evaluated using:

* Mean Absolute Error (MAE)
* Mean Squared Error (MSE)
* Root Mean Squared Error (RMSE)
* R² Score

## 🛠️ Technologies Used

* Python
* Pandas
* NumPy
* Scikit-learn
* Joblib
* Streamlit
* Matplotlib
* Seaborn
* Plotly

## 📁 Project Structure

```text
House-Price-Prediction/
│
├── app.py
├── train_model.py
├── house_prices.csv
├── model_results.csv
├── requirements.txt
├── README.md
│
├── models/
│   └── best_model.pkl
│
├── notebooks/
│   └── house_price_analysis.ipynb
│
└── reports/
```

## ▶️ How to Run

### Step 1 — Create virtual environment

```bash
python -m venv .venv
```

### Step 2 — Activate environment

Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

### Step 3 — Install dependencies

```bash
pip install -r requirements.txt
```

### Step 4 — Train the models

```bash
python train_model.py
```

This creates the dataset if one does not already exist, trains the regression models, evaluates them, and saves the best model.

### Step 5 — Launch the application

```bash
streamlit run app.py
```

## 🔮 Application

The Streamlit application allows users to enter:

* Area
* Bedrooms
* Bathrooms
* Location
* Property Age

The trained Machine Learning model then provides an estimated house price.

## 📈 Future Enhancements

Possible future improvements include:

* Larger real-world datasets
* Additional property features
* Interactive EDA dashboard
* Feature importance visualization
* Price prediction confidence ranges
* Geographic visualization
* Model hyperparameter tuning
* Cloud deployment
* Database integration

## 👨‍💻 Project Type

Machine Learning Internship Project

**Domain:** Real Estate Analytics

**Task:** House Price Prediction

**Learning Type:** Supervised Learning

**Problem Type:** Regression
