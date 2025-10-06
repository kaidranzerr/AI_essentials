from fastapi import  
from fastapi.responses import JSONResponse
from pydantic import BaseModel , Field , computed_field
from typing import Literal , Annotated
import pickle 
import pandas as pd 

with open('model.pkl' , 'rb') as f:
    model = pickle.load(f)

app = FastAPI()

# pydantic model to validate incoming data
class UserInput(BaseModel):
    age: Annotated[int , Field(... , gt=0 , lt=120 , description='Age of the user')]
    weight: Annotated[float , Field(... , gt=0 , lt=120)]
    height: Annotated[float , Field(... , gt=0 , lt=120)]
    smoker: Annotated[bool , Field(... , description='Is he a smoker or not')]
    incoming_lpa: Annotated[float , Field(... , gt=0 , lt=120)]
    city: Annotated[str , Field(... , description="The city in which the user lives")]
    occupation: Annotated[str , Field(... , description="The job of the user")]


    @computed_field
    @property
    def bmi(self) -> float:
        bmi = round(self.weight / (self.height ** 2) , 2)
        return bmi 
    @computed_field
    @property
    def lifestyle_rish(self) -> str:
        if self.smoker and self.bmi > 30:
            return "high"
        elif self.smoker or self.bmi>27:
            return "medium"
        else:
            return "low"
        
    @app.post('/predict')
    def predict_premium(data: UserInput):
        input_df = pd.DataFrame([{
            'bmi':data.bmi,
            'age_group':data.age_group,
            'lifestyle_risk':data.lifestyle_risk,
            'city_tier':data.city_tier,
            'income_lpa': data.income_lpa,
            'occupation':data.occupation
        }])
        prediction = model.predict(input_df)[0]
        return JSONResponse(status_code=200 , content={'prediction_category':prediction})