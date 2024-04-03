#import necessary modules
import streamlit as st
import pandas as pd
from joblib import load
from pymongo import MongoClient

#load the model
model = load(r'E:\Career\internship\recruitment task\model\random_forest_model.joblib')

#connect to mongodb clien and connect to database
client = MongoClient('mongodb://localhost:27017/')
db = client['Heart_Disease']  
collection = db['user_data']  


st.title('Heart Disease Predictor')

#to get the input from each user
age = st.number_input('Age', min_value=0, max_value=150, value=50)
sex = st.radio('Sex', ['Male', 'Female'])
cp = st.radio('Chest Pain Type', ['Typical Angina', 'Atypical Angina', 'Non-Anginal Pain', 'Asymptomatic'])
trestbps = st.number_input('Resting Blood Pressure (mm Hg)', min_value=0, value=120)
chol = st.number_input('Cholesterol (mg/dl)', min_value=0, value=200)
fbs = st.radio('Fasting Blood Sugar > 120 mg/dl', ['No', 'Yes'])
restecg = st.radio('Resting Electrocardiographic Results', ['Normal', 'ST-T Wave Abnormality', 'Probable or Definite Left Ventricular Hypertrophy'])
thalach = st.number_input('Maximum Heart Rate Achieved', min_value=0, value=150)
exang = st.radio('Exercise Induced Angina', ['No', 'Yes'])
oldpeak = st.number_input('ST Depression Induced by Exercise Relative to Rest', min_value=0.0, value=0.0)
slope = st.radio('Slope of the Peak Exercise ST Segment', ['Upsloping', 'Flat', 'Downsloping'])
ca = st.selectbox('Number of Major Vessels Colored by Fluoroscopy', ['0', '1', '2', '3'])
thal = st.radio('Thalassemia', ['Normal', 'Fixed Defect', 'Reversible Defect'])


if st.button('Predict'):
    #mapped the valuesaccordinly
    sex_binary = 1 if sex == 'Male' else 0
    fbs_binary = 1 if fbs == 'Yes' else 0
    exang_binary = 1 if exang == 'Yes' else 0
    cp_mapping = {'Typical Angina': 0, 'Atypical Angina': 1, 'Non-Anginal Pain': 2, 'Asymptomatic': 3}
    cp_binary = cp_mapping[cp]
    restecg_mapping = {'Normal': 0, 'ST-T Wave Abnormality': 1, 'Probable or Definite Left Ventricular Hypertrophy': 2}
    restecg_binary = restecg_mapping[restecg]
    slope_mapping = {'Upsloping': 0, 'Flat': 1, 'Downsloping': 2}
    slope_binary = slope_mapping[slope]
    thal_mapping = {'Normal': 0, 'Fixed Defect': 1, 'Reversible Defect': 2}
    thal_binary = thal_mapping[thal]


    #put them in a dictionary to convert them into dataframe for easy loading into model for prediction
    binary_data = pd.DataFrame({
        'age': [age],
        'sex': [sex_binary],
        'cp': [cp_binary],
        'trestbps': [trestbps],
        'chol': [chol],
        'fbs': [fbs_binary],
        'restecg': [restecg_binary],
        'thalach': [thalach],
        'exang': [exang_binary],
        'oldpeak': [oldpeak],
        'slope': [slope_binary],
        'ca': [ca],
        'thal': [thal_binary]
    })
    
    #predicted from the userdata
    prediction = model.predict(binary_data)

    #created a dataframe of user data to load into mongo db database for collection
    user_data = pd.DataFrame({
        'age': [age],
        'sex': [sex],
        'cp': [cp],
        'trestbps': [trestbps],
        'chol': [chol],
        'fbs': [fbs],
        'restecg': [restecg],
        'thalach': [thalach],
        'exang': [exang],
        'oldpeak': [oldpeak],
        'slope': [slope],
        'ca': [ca],
        'thal': [thal],
    })
    
    #converting datas into strings
    user_data.index = user_data.index.astype(str)
    user_data_dict = user_data.iloc[0].to_dict()
    #converting binary prediction into positive/negative
    prediction_result = 'Positive' if prediction[0] == 1 else 'Negative'
    data_to_insert = {**user_data_dict, 'prediction': prediction_result}
    #insert the data into mongodb database
    collection.insert_one(data_to_insert)

   
    st.write('### Prediction:')
    #displaying the prediction
    if prediction[0] == 0:
        st.write('The patient is predicted negative for heart disease.')
    else:
        st.write('The patient is predicted positive for heart disease.')

#closing mongodb client
client.close()
