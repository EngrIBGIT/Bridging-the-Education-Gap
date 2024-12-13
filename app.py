import streamlit as st
import pandas as pd
import pickle
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from io import BytesIO

# Load the trained model
with open('enrollment_prediction_model.pkl', 'rb') as file:
    rf_model = pickle.load(file)

# Function to predict enrollment
def predict_enrollment(region, sub_school, school_type, male, female):
    # Ensure the inputs match the 10 features expected by the model
    input_data = pd.DataFrame({
        'Male': [male],
        'Female': [female],
        'North Central': [1 if region == 'North Central' else 0],
        'North East': [1 if region == 'North East' else 0],
        'North West': [1 if region == 'North West' else 0],
        'South East': [1 if region == 'South East' else 0],
        'South South': [1 if region == 'South South' else 0],
        'South West': [1 if region == 'South West' else 0],
        'Sub-Schools': [float(sub_school)],
        'Type of Schools': [float(school_type)]
    })

    # Feature scaling
    scaler = StandardScaler()
    input_data = scaler.fit_transform(input_data)

    # Predict the enrollment
    predicted_enrollment = rf_model.predict(input_data)
    return predicted_enrollment[0]

# Streamlit layout
st.set_page_config(page_title="Enrollment Prediction Dashboard", page_icon="📊", layout="wide")

# Display logo
st.image("logo.png", width=400)

# Title and explanation
st.title("🎓 Education Enrollment Prediction")
st.write("**Welcome!** This application predicts school enrollment based on selected criteria. "
         "Simply provide the required inputs, and you'll receive an accurate prediction alongside visualization insights.")

# Sidebar inputs
st.sidebar.header("User Inputs")

# School inputs
region = st.sidebar.selectbox(
    "Select Region", 
    ['North Central', 'North East', 'North West', 'South East', 'South South', 'South West']
)

sub_school = st.sidebar.selectbox(
    "Select Sub-School", 
    ['1.0 (ECCDE/Pre-Primary)', '2.0 (Primary)', '3.0 (JSS)', '4.0 (SSS)']
)

school_type = st.sidebar.selectbox(
    "Select Type of School", 
    ['1.0 (Conventional)', '2.0 (Special Needs)', '3.0 (Nomadic)', 
     '4.0 (Migrant Fishermen/Farmers)', '5.0 (Islamiyya)', '6.0 (Tsangaya/Almajiri)']
)

# Gender inputs
male = st.sidebar.text_input("Enter Number of Males", value="0")
female = st.sidebar.text_input("Enter Number of Females", value="0")

# Convert inputs to numeric
try:
    male = int(male)
    female = int(female)
except ValueError:
    st.sidebar.error("Please ensure Male and Female inputs are integers.")

# Predict button
if st.sidebar.button("Predict Enrollment"):
    # Get the prediction
    predicted_enrollment = predict_enrollment(
        region, sub_school.split()[0], school_type.split()[0], male, female
    )

    # Display prediction
    st.subheader("📊 Prediction Results")
    st.write(f"**Predicted Total Enrollment:** {predicted_enrollment:.2f}")

    # Visualization
    st.subheader("Enrollment Breakdown")
    labels = ['Male', 'Female']
    sizes = [male, female]
    colors = sns.color_palette("pastel")
    plt.figure(figsize=(2, 2))
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=120, colors=colors)
    plt.title("Gender Distribution")
    st.pyplot(plt)

    st.write(
        f"**Explanation:** The predicted enrollment is based on the input factors. "
        f"This breakdown provides insights into the gender distribution, offering a clear "
        f"visualization of the male-to-female ratio in the specified region and school type."
    )

# Option to save data
def save_data_as_excel(data):
    buffer = BytesIO()
    with pd.ExcelWriter(buffer) as writer:
        data.to_excel(writer, index=False)
    st.download_button(
        label="Download Data as Excel",
        data=buffer.getvalue(),
        file_name="enrollment_data.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

if st.sidebar.button("Save Data"):
    data = pd.DataFrame({
        'Region': [region],
        'Sub-School': [sub_school],
        'School Type': [school_type],
        'Male Enrollment': [male],
        'Female Enrollment': [female],
        'Predicted Enrollment': [predicted_enrollment]
    })
    save_data_as_excel(data)
