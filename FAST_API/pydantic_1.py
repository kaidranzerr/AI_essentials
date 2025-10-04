# for complex type and data validation || strict schema 
# why --> we dont have any strict schema in python since it's a dynamically typed language
# define a pydantic model that represents the ideal schema of the data
# instantiate the model with raw input data 
# pass the validated model object 
from pydantic import BaseModel , EmailStr , AnyUrl , Field
from typing import List , Dict , Optional , Annotated

class Patient(BaseModel):
    name: str = Field(max_length=50)
    email: EmailStr
    linkedin_url: AnyUrl
    age: int = Field(gt=0 , lt=120)
    weight: float = Field(gt=0)
    married: bool 
    allergies: List[str] = Field(max_length=5)
    contact_details: Dict[str]

def insert_patient_model(patient: Patient):
    print(patient.name)

patient_info = {'name': 'nitish' , 'age':30 , 'weight':75.4 , 'married':True , 'allergies':['pollen' , 'dust'] , 'contact details':{'email':'abc@gmail.com' , 'phone':'1234567'}}

patient1 = Patient(**patient_info)
