import streamlit as st
import pandas as pd
import joblib

# Page Configuration
st.set_page_config(
    page_title="Credit Risk Assessment",
    page_icon="🏦",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Custom CSS for better UI
st.markdown("""
<style>
    /* Main container padding */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    
    /* Headers */
    h1, h2, h3 {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    /* Input field styling */
    .stNumberInput input, .stSelectbox select {
        border-radius: 8px;
        padding: 10px;
    }
    
    /* Predict Button Styling */
    .stButton > button {
        background: linear-gradient(135deg, #4b6cb7 0%, #182848 100%);
        color: white;
        font-weight: bold;
        border-radius: 12px;
        border: none;
        padding: 15px 0px;
        font-size: 1.2rem;
        transition: all 0.3s ease;
    }
    .stButton > button:hover {
        background: linear-gradient(135deg, #182848 0%, #4b6cb7 100%);
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        transform: translateY(-2px);
    }
    
    /* Section dividers */
    hr {
        margin: 1.5em 0;
        opacity: 0.2;
    }
</style>
""", unsafe_allow_html=True)

# Load model
@st.cache_resource
def load_model():
    return joblib.load("credit_risk_model.pkl")

try:
    model = load_model()
except Exception as e:
    st.error(f"Error loading the model: {e}")
    st.stop()

# Header
st.title("🏦 Credit Risk Assessment System")
st.markdown("Please fill out the customer details below to generate a risk assessment.")
st.divider()

# Organize inputs into groups using columns
st.subheader("👤 1. Personal Information")
col1, col2, col3 = st.columns(3)
with col1:
    age = st.number_input("Age", min_value=18, max_value=120, value=30)
with col2:
    sex = st.selectbox("Sex", ["male", "female"])
with col3:
    job = st.selectbox("Job Level", [0, 1, 2, 3], help="0: Unskilled/Non-resident, 1: Unskilled/Resident, 2: Skilled/Official, 3: Management/Self-employed")

st.subheader("💰 2. Financial Status")
col4, col5, col6 = st.columns(3)
with col4:
    housing = st.selectbox("Housing", ["own", "rent", "free"])
with col5:
    saving = st.selectbox("Saving Account", ["little", "moderate", "quite rich", "rich", "No account"])
with col6:
    checking = st.selectbox("Checking Account", ["little", "moderate", "No account"])

st.subheader("📋 3. Loan Details")
col7, col8, col9 = st.columns(3)
with col7:
    credit_amount = st.number_input("Credit Amount", min_value=0, value=1000, step=500)
with col8:
    duration = st.number_input("Duration (months)", min_value=1, max_value=120, value=12, step=1)
with col9:
    purpose = st.selectbox("Purpose", [
        "car", "furniture/equipment", "radio/TV",
        "domestic appliances", "repairs",
        "education", "business", "vacation/others"
    ])

st.divider()

# Centered predict button and results
if st.button("🔍 Predict Risk Status", type="primary", use_container_width=True):
    with st.spinner("Analyzing customer data..."):
        input_data = pd.DataFrame({
            "Age": [age],
            "Sex": [sex],
            "Job": [job],
            "Housing": [housing],
            "Saving accounts": [saving],
            "Checking account": [checking],
            "Credit amount": [credit_amount],
            "Duration": [duration],
            "Purpose": [purpose]
        })

        try:
            prob = model.predict_proba(input_data)[:, 1][0]
            prediction = 1 if prob >= 0.4 else 0
            
            reasons = []

            if credit_amount > 12000:
                reasons.append("High credit amount increases repayment risk.")
            if duration > 36:
                reasons.append("Long loan duration increases exposure to default risk.")
            if saving == "No account":
                reasons.append("No savings account indicates lower financial cushion.")
            if checking == "No account":
                reasons.append("No checking account indicates weak financial activity.")
            if job == 0:
                reasons.append("Unskilled job category may indicate unstable income.")
            if age < 25:
                reasons.append("Younger applicants may have limited credit history.")

            st.markdown("---")
            st.markdown("### 📊 Assessment Result")
            st.write("") # spacing
            
            # Use custom HTML/CSS for a better look
            if prediction == 1:
                result_color = "#ff4b4b"
                result_bg = "rgba(255, 75, 75, 0.1)"
                result_icon = "⚠️"
                result_title = "High Risk Customer"
                result_desc = "The applicant has a high probability of defaulting on their credit."
            else:
                result_color = "#00cc96"
                result_bg = "rgba(0, 204, 150, 0.1)"
                result_icon = "✅"
                result_title = "Low Risk Customer"
                result_desc = "The applicant is considered safe for credit approval."
                
            st.markdown(f"""
                <div style="background-color: {result_bg}; border: 1px solid {result_color}; border-radius: 10px; padding: 25px; text-align: center; margin-bottom: 25px;">
                    <h1 style="color: {result_color}; margin: 0; font-size: 2.5em;">{result_icon} {result_title}</h1>
                    <h3 style="margin-top: 10px; margin-bottom: 5px; opacity: 0.9;">Default Probability: {prob:.1%}</h3>
                    <p style="font-size: 1.1em; opacity: 0.8; margin-bottom: 0;">{result_desc}</p>
                </div>
            """, unsafe_allow_html=True)
            
            # Display reasons in a nice format if there are any
            if prediction == 1 and reasons:
                st.markdown("#### 🔍 Key Risk Factors:")
                for r in reasons:
                    st.markdown(f'<p style="font-size: 1.2em; margin-bottom: 5px;"><strong>-</strong> {r}</p>', unsafe_allow_html=True)
            elif prediction == 0:
                st.markdown("#### 🌟 Positive Indicators:")
                if credit_amount < 5000:
                    st.markdown('<p style="font-size: 1.2em; margin-bottom: 5px;"><strong>-</strong> Moderate credit amount.</p>', unsafe_allow_html=True)
                if duration <= 24:
                    st.markdown('<p style="font-size: 1.2em; margin-bottom: 5px;"><strong>-</strong> Short repayment duration.</p>', unsafe_allow_html=True)
                if saving in ["rich", "quite rich"]:
                    st.markdown('<p style="font-size: 1.2em; margin-bottom: 5px;"><strong>-</strong> Strong savings history.</p>', unsafe_allow_html=True)
                if not any([credit_amount < 5000, duration <= 24, saving in ["rich", "quite rich"]]):
                    st.markdown('<p style="font-size: 1.2em; margin-bottom: 5px;"><strong>-</strong> Overall profile indicates low risk.</p>', unsafe_allow_html=True)
                    
        except Exception as e:
            st.error(f"An error occurred during prediction: {e}")