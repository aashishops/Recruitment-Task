#loaded necessary libraries
from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from joblib import load
import json
from pymongo import MongoClient

#connected to fastapi
app = FastAPI()

#loaded the model 
model = load(r"E:\Career\internship\recruitment task\model\random_forest_model.joblib")

#connected to mongodb client and the database
client = MongoClient('mongodb://localhost:27017/')
db = client['Heart_Disease']
collection = db['user_data']

#created a class for storing the data
class HeartData(BaseModel):
    age: int
    sex: str
    cp: str
    trestbps: int
    chol: int
    fbs: str
    restecg: str
    thalach: int
    exang: str
    oldpeak: float
    slope: str
    ca: str
    thal: str

#requesting from html page to get the variable datas
@app.get("/", response_class=HTMLResponse)
async def read_root():
    with open("static/index.html", "r") as file:
        html_content = file.read()
    return HTMLResponse(content=html_content)

#receiving data and returning the prediction value
@app.post("/", response_class=HTMLResponse)
async def predict(data: HeartData):
    #mapping the datas into numbers accordingly 
    sex_binary = 1 if data.sex == 'Male' else 0
    fbs_binary = 1 if data.fbs == 'Yes' else 0
    exang_binary = 1 if data.exang == 'Yes' else 0
    
    cp_mapping = {'Typical Angina': 0, 'Atypical Angina': 1, 'Non-Anginal Pain': 2, 'Asymptomatic': 3}
    cp_binary = cp_mapping[data.cp]

    restecg_mapping = {'Normal': 0, 'ST-T Wave Abnormality': 1, 'Probable or Definite Left Ventricular Hypertrophy': 2}
    restecg_binary = restecg_mapping[data.restecg]

    slope_mapping = {'Upsloping': 0, 'Flat': 1, 'Downsloping': 2}
    slope_binary = slope_mapping[data.slope]

    thal_mapping = {'Normal': 0, 'Fixed Defect': 1, 'Reversible Defect': 2}
    thal_binary = thal_mapping[data.thal]

    #put them in a dictionary to convert them into dataframe for easy loading into model for prediction
    user_data = [[data.age, sex_binary, cp_binary, data.trestbps, data.chol, fbs_binary, restecg_binary,
                  data.thalach, exang_binary, data.oldpeak, slope_binary, int(data.ca), thal_binary]]
    
    #for predictin
    prediction = model.predict(user_data)
    
    prediction_result = {"prediction": "The patient is predicted to have heart disease."} if prediction[0] == 1 else {"prediction": "The patient is predicted to not have heart disease."}
    print(prediction_result)
       
    user_data_dict = data.dict()
    user_data_dict.update(prediction_result)
    #enered the user data value into mongo db database
    collection.insert_one(user_data_dict)
    
    print("Data inserted successfully")
    
    return HTMLResponse(content=json.dumps(prediction_result))
