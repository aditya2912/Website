from django.db import models
from django import forms
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine


# Create your models here.
Base = declarative_base()

class RegistrationDetails(Base):
    __tablename__ = 'registration-details'
    user_uuid = Column(String, primary_key =True)
    username = Column(String, nullable=False)
    password = Column(String, nullable=False)
    email = Column(String, nullable=False)
    phone_number = Column(String, nullable=False)
    
    
registration_details_engine = create_engine('sqlite:///RegistrationDetailsDatabase.db')
Base.metadata.create_all(registration_details_engine)
