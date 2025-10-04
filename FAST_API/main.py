# HTTP Methods --> software --> static || dynamic || CRUD (Create , Retrieve , Update , Delete)
from fastapi import FastAPI , Path , HTTPException , Query
import json 


app = FastAPI()
def load_data():
    with open('patients.json' , 'r') as f:
        data = json.load(f)
    return data 
@app.get("/")
def hello():
    return {'message':'Patient management system API'}


@app.get("/about")
def about():
    return {"message": 'A fully functional API to manage your patient records'}

@app.get("/view")
def view():
    data = load_data()
    return data 

# path parameters are dynamic segments of a URL path used to identify a specific resource 

@app.get('/patient/{patient_id}')
def view_patient(patient_id: str = Path(..., description='ID of the patient in the DB' , example='P001')):
    # load all the patients 
    data = load_data()
    if patient_id in data:
        return data[patient_id]
    return HTTPException(status_code=404 , detail='Patient not Found!')

@app.get('/sort')
def sort_patients(sort_by: str = Query(... , description = 'Sort on the basis of height , weight , bmi') , order: str = Query('asc' , description="Sort in ascending or descending order")):
    valid_fields = ['height' , 'weight' , 'bmi']
    if sort_by in valid_fields:
        raise HTTPException(status_code=400 , detail = 'Invalid field select from {valid_fields}')
    if order not in ['asc' , 'desc']:
        raise HTTPException(status_code=400 , detail = 'Invalid ord select from asc or desc')

    data = load_data()
    sort_order = True if order == 'desc' else False  
    sorted_data = sorted(data.values() , key = lambda x:x.get('sort_by' , 0) , reverse=sort_order)
    return sorted_data



# Path helps in enhancing path parameters readability || it helps in providing metadata , validation rules and documentation hints in 
# path parameters in your API endpoints

# HTTP status codes are 3 digit numbers returned by a web server to indicate the results of a client's request
# 2 --> Success || 3 --> Redirection || 4 --> Client Error || 5 --> Server Error
# HTTPException is a special built in exception in FastAPI used to return custom HTTP error responses when something goes wrong in your API
# gracefully raise the error

# Query params are optional key-value pairs appended to the end of the URL used to pass additional data to serverin an HTTP request
# filtering , sorting , searching and pagination w/o altering end point paths itself

# Query() is a utility function provided by FastAPI to declare validate and document query parameters in API endpoints