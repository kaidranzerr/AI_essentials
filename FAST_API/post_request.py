# a request body is a portion of HTTP request that contains data sent by the client ti the server it is typically used in HTTP methods 
# such as POST , PUT to transmit structured data

# 3 steps 
# client sends data
#  validate --> pydantic model
#  json file --> new record added

from fastapi import FastAPI , Path , HTTPException , Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel , Field , computed_field
import json 
from typing import Annotated , Literal

app = FastAPI()

class Patient(BaseModel):

    id:Annotated[str , Field(... , description='ID of the patient' , examples=['P001'])]
    name: Annotated[str , Field(... , description='Name of the patient')]
    city:Annotated[str , Field(... , description='City where the patient is living')]
    age:Annotated[int , Field(... , gt=0 , lt=120 , description='Age of the patient')]
    gender: Annotated[Literal['male' , 'female' , 'others'] , Field(... , description='Height of the patient')]
    height: float 
    weight: float 

    @computed_field
    @property
    def bmi(self) -> float:
        bmi = round(self.weight / (self.height ** 2) , 2)
        return bmi 
    
    @computed_field
    @property
    def verdict(self) -> str:

        if self.bmi < 18.5:
            return 'Underweight'
        elif self.bmi < 25:
            return 'Normal'
        elif self.bmi < 30:
            return 'Normal but motu'
        else:
            return 'Gende saale!!!'

@app.post('/create')
def create_patient(patient: Patient):

    # load existing data 
    data = load_data()

    #check if the patient already exists 
    if patient.id in data:
        raise HTTPException(status_code=400 , detail='Patient already exists')

    # new patient add to the database 
    data[patient.id] = patient.model_dump(exclude=['id'])

    save_data(data)
    return JSONResponse(status_code=201 , content={'message': 'patient created successfully'})




def load_data():
    with open('patients.json' , 'r') as f:
        data = json.load(f)
    return data 

def save_data(data):
    with open('patients.json' , 'w') as f:
        json.dump(data , f)