from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from datetime import date 
from sqlalchemy import Column, Integer, DateTime
import json
db = SQLAlchemy()


class Users(db.Model):
    __tablename__ = 'users'
    id_user = db.Column(db.Integer, primary_key = True)
    Name = db.Column(db.String(100))
    Email = db.Column(db.String(100))
    Password = db.Column(db.String(100))
    address=db.Column(db.String(100))
    date_of_birth=db.Column(db.Date)
    img_avatar=db.Column(db.String(200))
    Roll = db.Column(db.Integer)
    id_department = db.Column(db.Integer,db.ForeignKey('departments.id_department'),nullable=False)
    sesstion_user = db.relationship('sessions', backref = 'sessions_user' , lazy = True)
    work_schedule_user = db.relationship('work_schedule', backref = 'work_schedule_user' , lazy = True)
    def get_id(self):
        return(self.id_user)
    def serialize(self):
        return {
            "id_user": self.id_user,
            "name": self.Name,
            "email": self.Email,
            "role": self.Roll,
            "address": self.address,
            "date_of_birth": self.date_of_birth,
            "img_avatar": self.img_avatar,
            
        }

class Department(db.Model):
    __tablename__ = 'departments'
    id_department = db.Column(db.Integer, primary_key = True)
    Name = db.Column(db.String(100))
    Decription = db.Column(db.String(100))
    def get_id(self):
        return(self.id_department)
    def serialize(self):
        return{
            'id_department': self.id_department,
            'Name' : self.Name,
            'Decription': self.Decription,
        }



class sessions(db.Model):
    __tablename__ = 'sessions'
    session_id = db.Column(db.Integer , primary_key = True)
    id_user = db.Column(db.Integer, db.ForeignKey('users.id_user'), nullable = False)
    id_work_schedule = db.Column(db.Integer, db.ForeignKey('work_schedule.id_work_schedule'), nullable = False)
    image_url = db.Column(db.String(200))   
    token = db.Column(db.String(200)) 
    created_at = db.Column(db.DateTime, server_default=func.now())

class work_schedule(db.Model):
    __tablename__ ='work_schedule'
    id_work_schedule = db.Column(db.Integer , primary_key = True)
    work_name = db.Column(db.String(100))
    work_date = db.Column(db.Date)
    start_time = db.Column(db.Time)
    end_time = db.Column(db.Time)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id_user'), nullable = False)
    id_department = db.Column(db.Integer , db.ForeignKey('departments.id_department') , nullable = False)
    work_schedule_sesstions = db.relationship('sessions', backref = 'work_schedule_session' , lazy = True)
    def serialize(self):
        return{
            'id_work_schedule': self.id_work_schedule,
            'work_name' : self.work_name,
            'work_date': self.work_date.isoformat(),
            'start_time': self.start_time.isoformat(),
            'end_time': self.end_time.isoformat(),
            'created_by': self.created_by,
        }