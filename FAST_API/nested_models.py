# if in pydantic we start using a model in some different model as a field then we call it a nested model

from pydantic import BaseModel
class Address(BaseModel):
    city: str 
    state: str 
    pincode: int 

class Patient(BaseModel):
    name: str 
    gender: str 
    age: int 
    address : Address

address_dict = {'city': 'gurgaon',  'state': 'haryana' , 'pin': '123456'}
address1 = Address(**address_dict)
patient_dict = {'name':'nitish' , 'gender':'asdasd' , 'age':45 , 'address':address1}
patient1 = Patient(**patient_dict)
print(patient1.address.pin)

temp = patient1.model_dump(include=['name' , 'gender']) # we also have exclude
