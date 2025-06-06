from sqlalchemy import Column, Integer, String, Text, DateTime, JSON
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

base = declarative_base()

# The table called "resumes" for DB
class Resume(base):
    __tablename__='resumes'
    id=Column(Integer,primary_key=True,index=True)
    file_name = Column(String)
    name=Column(String)
    email=Column(String)
    phone=Column(String)
    skills=Column(JSON)
    experience=Column(Text)
    suggestions=Column(Text)
    recommended_skills = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)



