# 💳 Credit Risk Assessment & Decision Support System

## 📖 Overview
This project is an end-to-end Machine Learning system designed to help financial institutions assess loan applicants as **High Risk** or **Low Risk**.

Instead of optimizing purely for accuracy, the system aligns with business objectives by prioritizing detection of risky customers and allowing threshold tuning based on risk appetite.

The application provides:
- Default probability estimation
- Risk classification (High / Low)
- Explanation of key contributing factors

---

## 🎯 Problem Statement
Banks must minimize loan defaults while maintaining business growth. A simple accuracy-focused model may fail to detect risky customers in imbalanced datasets.

This project builds a robust ML solution that:
- Handles class imbalance
- Evaluates models using Recall, Precision, F1-score, and ROC-AUC
- Tunes classification threshold based on business needs
- Provides interpretable predictions

---

## 🛠 Tech Stack
- Python
- Pandas
- NumPy
- Scikit-learn
- Streamlit
- SHAP (optional for advanced explanation)
- Joblib

---

## 📊 Dataset
German Credit Risk Dataset (1000 instances)

Features include:
- Age
- Job
- Housing
- Saving Account
- Checking Account
- Credit Amount
- Loan Duration
- Purpose
- Risk (Target Variable)

---

## ⚙️ Project Workflow

### 1️⃣ Data Preprocessing
- Removed unnecessary columns
- Handled missing values
- Applied Ordinal Encoding & One-Hot Encoding
- Used ColumnTransformer
- Stratified Train-Test Split

### 2️⃣ Model Training
Models evaluated:
- Logistic Regression
- Logistic Regression (Class Weighted)
- Random Forest (Final Model)

### 3️⃣ Evaluation Metrics
- Confusion Matrix
- Precision
- Recall
- F1-Score
- ROC-AUC

Final Model Selected:
- Random Forest
- ROC-AUC ≈ 0.75
- Recall (Bad Class) improved using threshold tuning

---

## 🎛 Threshold Tuning
Default threshold (0.5) was adjusted to **0.4** to improve detection of risky customers.

Why?
Because in credit risk, approving a bad customer (False Negative) is more costly than rejecting a good one.

Threshold tuning allows:
- Conservative strategy → Lower threshold
- Aggressive growth → Higher threshold

---

## 📈 Feature Importance
Top contributing features:
- Credit Amount
- Age
- Loan Duration
- Checking Account
- Saving Account

These align with financial risk intuition.

---

## 🖥 Streamlit Application

The app allows users to:
- Enter applicant details
- View predicted default probability
- Get High/Low Risk classification
- See key contributing risk factors

---

## 🚀 How to Run Locally

1. Clone the repository
2. Create virtual environment
3. Install dependencies:

```bash
pip install -r requirements.txt