# Heart Disease Prediction System

This is a simple web application built with Streamlit as well as FastAPI that predicts the likelihood of heart disease based on various input parameters provided by the user. This application uses MongoDB database for storing user data ,etc.. The prediction model is trained using a Random Forest classifier.

## Features

- **Prediction Form**: Users can enter their information such as age, sex, blood pressure, cholesterol level, etc., through an interactive form.
- **Prediction Display**: Upon submission of the form, the application predicts whether the user is likely to have heart disease or not.
- **Data Logging**: User input and prediction results are logged in a MongoDB database.


## Installation

1. Clone the repository:

```bash
git clone https://github.com/aashishops/Recruitment-Task.git
```

2. Create a Database in Mongodb named Heart_Disease and collection named user_data
##### To Run FastAPI application
3. Enter the following in Terminal
```bash
cd Heart Disease Prediction
pip install -r requirements.txt
cd src
cd FASTAPI
uvicorn main:app --reload
```
##### To Run Streamlit application
```bash
cd Heart Disease Prediction
pip install -r requirements.txt
cd src
cd script
streamlit run app.py
```

## Usage
Open your web browser and go to http://localhost:8000 for FASTAPI and http://http://localhost:8501 for Streamlit
Fill in the required information in the prediction form.
Click on the "Predict" button.
The prediction result will be displayed on the screen.

## Technologies Used
FastAPI: Web framework used for building the API.
HTML/CSS/JavaScript: Frontend technologies for creating the user interface.
MongoDB: NoSQL database used for storing user data and prediction results.
Scikit-learn: Machine learning library used for training the prediction model.
Joblib: Library used for saving and loading the trained model.

## License

This project is licensed under the MIT License. See the [LICENSE](https://github.com/aashishops/Recruitment-Task/blob/main/LICENSE) file for details.
