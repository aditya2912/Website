from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import select
import mysql.connector
import datetime
from .models import RegistrationDetails

#Write query functions here

#Custom function to generate uuid on the basis of time and date
# return type : string
# arguments : None

def generate_uuid():
    year = str(datetime.datetime.now().year)
    month = str(datetime.datetime.now().month)
    day = str(datetime.datetime.now().day)
    hour = str(datetime.datetime.now().hour)
    minute = str(datetime.datetime.now().minute)
    second = str(datetime.datetime.now().second)
    microsecond = str(datetime.datetime.now().microsecond)
    uuid = uuid = year + month + day + hour + minute + second + microsecond
    return str(uuid)

def saveRegistrationDetailsIntoDatabase(request_parameters):
    engine = create_engine('sqlite:///RegistrationDetailsDatabase.db')
    user_uuid = generate_uuid()
    user_name = request_parameters["user_name"]
    password = request_parameters["password"]
    email = request_parameters["email"]
    phone_number = request_parameters["phone_number"]
    Base = declarative_base()
    Base.metadata.bind = engine
    DBSession = sessionmaker(bind = engine)
    session = DBSession()
    userDetailsData = RegistrationDetails(user_uuid=user_uuid, username=user_name,password=password,email=email, phone_number=phone_number) 
    session.add(userDetailsData)
    try: 
        session.commit()
        print("Data saved successfully")
        return user_uuid
    except IOError: 
        print("Unable to save data", IOError)

    
    
# Create your views here.
@csrf_exempt
def register_user(request):
    user_name = ""
    password = ""
    email = ""
    phone_number = ""
    
    if request.method == "POST":
        user_object = json.loads(request.body.decode("utf-8"))
        request_parameters = {"user_name": user_object["userName"], "password": user_object['password'], "email": user_object["email"],"phone_number": user_object["phoneNumber"]}
        user_uuid = saveRegistrationDetailsIntoDatabase(request_parameters)
        user_uuid_json = json.dumps(user_uuid,indent=2)
        print("***************", user_uuid_json)
        return HttpResponse(user_uuid_json, content_type="application/json")
