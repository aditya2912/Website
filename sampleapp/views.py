from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import select
from django.template.response import SimpleTemplateResponse

# import mysql.connector
import datetime
from .models import RegistrationDetails
from django.views.decorators.csrf import ensure_csrf_cookie

# Write query functions here

# Custom function to generate uuid on the basis of time and date
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
    uuid = year + month + day + hour + minute + second + microsecond
    return str(uuid)


def saveRegistrationDetailsIntoDatabase(request_parameters):
    engine = create_engine("sqlite:///RegistrationDetailsDatabase.db")
    user_uuid = generate_uuid()
    user_name = request_parameters["user_name"]
    password = request_parameters["password"]
    email = request_parameters["email"]
    phone_number = request_parameters["phone_number"]
    Base = declarative_base()
    Base.metadata.bind = engine
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    userDetailsData = RegistrationDetails(
        user_uuid=user_uuid,
        username=user_name,
        password=password,
        email=email,
        phone_number=phone_number,
    )
    session.add(userDetailsData)
    try:
        session.commit()
        print("Data saved successfully")
        return user_uuid
    except IOError:
        print("Unable to save data", IOError)


def get_details_from_database(uuid):
    engine = create_engine("sqlite:///RegistrationDetailsDatabase.db")
    Base = declarative_base()
    Base.metadata.bind = engine
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    user_query = session.query(RegistrationDetails).filter(
        RegistrationDetails.user_uuid.in_([uuid])
    )
    result = user_query.first()
    return result


# Create your views here.
@csrf_exempt
def register_user(request):
    user_name = ""
    password = ""
    email = ""
    phone_number = ""

    if request.method == "POST":
        user_object = json.loads(request.body.decode("utf-8"))
        request_parameters = {
            "user_name": user_object["userName"],
            "password": user_object["password"],
            "email": user_object["email"],
            "phone_number": user_object["phoneNumber"],
        }
        user_uuid = saveRegistrationDetailsIntoDatabase(request_parameters)
        user_uuid_json = json.dumps(user_uuid, indent=2)

        return HttpResponse(user_uuid_json, content_type="application/json")
        # return render(request, "index.html", {"user_uuid_json": user_uuid_json})


@csrf_exempt
def get_registered_user(request):
    print(request.method, "REQUEST METHOD")
    return render(request, "index.html", {})


def fetch_details_by_uuid(request, uuid):
    # uuid = request.GET.get("uuid")
    print(" I am Here")
    print(request.method, "UUID ")
    if request.method == "GET":
        user_details = get_details_from_database(uuid)
        # user_details_in_json = json.dumps(user_details, indent=2)
        # print(user_details_in_json, "USER DETAILS")
        name = json.dumps(user_details.username, indent=2)
        print(name, "NAME ")
        return SimpleTemplateResponse("index.html", {"name": json.dumps(name)})

        # return HttpResponse(user_details, content_type="application/json")
        # return render(request, "C:/Website/build/index.html", {"name": name})
