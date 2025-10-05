# to update we use put method
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
from typing import Annotated , Literal , Optional

app = FastAPI()

class PatientUpdate(BaseModel):

    id:Annotated[Optional[str] , Field(... , description='ID of the patient' , examples=['P001'])]
    name: Annotated[Optional[str] , Field(... , description='Name of the patient')]
    city:Annotated[Optional[str] , Field(... , description='City where the patient is living')]
    age:Annotated[Optional[int] , Field(... , gt=0 , lt=120 , description='Age of the patient')]
    gender: Annotated[Optional[Literal['male' , 'female' , 'others']] , Field(... , description='Height of the patient')]
    height: Annotated[Optional[float] , Field(default=None , gt=0)]
    weight: Annotated[Optional[float] , Field(default=None , gt=0)]
     

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

@app.put('/edit/{patient_id}')
def update(patient_id:str , patient_update: PatientUpdate):
    data = load_data()
    if patient_id not in data:
        raise HTTPException(status_code=404 , detail='Patient not found')
    existing_patient_info = data[patient_id]
    # converting the pydantic object to dictionary
    updated_patient_info = patient_update.model_dump(exclude_unset=True)
    for key,value in updated_patient_info.items():
        existing_patient_info[key] = value 
    existing_patient_info['id'] = patient_id
    patient_pydantic_obj = PatientUpdate(**existing_patient_info)
    # pydantic object --> dict
    existing_patient_info = patient_pydantic_obj.model_dump(exclude='id')
    # add this dict to data
    data[patient_id] = existing_patient_info
    save_data(data)
    return JSONResponse(status_code=200 , content={'message': 'patient updated'})

@app.delete('/delete/{patient_id}')
def delete_patient(patient_id: str):
    # load data
    data = load_data()

    if patient_id not in data:
        raise HTTPException(status_code=404 , detail='Patient not found')
    del data[patient_id]
    save_data(data)
    return JSONResponse(status_code=200 , content={'message':"patient deleted"})
def load_data():
    with open('patients.json' , 'r') as f:
        data = json.load(f)
    return data 

def save_data(data):
    with open('patients.json' , 'w') as f:
        json.dump(data , f)