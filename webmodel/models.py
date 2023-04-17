from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from datetime import date
from sqlalchemy import Column, Integer, DateTime
db = SQLAlchemy()


class Users(db.Model):
    __tablename__ = 'users'
    id_user = db.Column(db.Integer, primary_key = True)
    Name = db.Column(db.String(100))
    Email = db.Column(db.String(100))
    Password = db.Column(db.String(100))
    Roll = db.Column(db.Integer)
    detaildepartment_user = db.relationship('DetailDepartment', backref = 'detaildepartment_user' , lazy = True)
    face_user = db.relationship('faces', backref = 'faces_user' , lazy = True)
    sesstion_user = db.relationship('sessions', backref = 'sessions_user' , lazy = True)
    work_schedule_user = db.relationship('work_schedule', backref = 'work_schedule_user' , lazy = True)
    def get_id(self):
        return(self.id_user)
    def serialize(self):
        return{
            'id_user': self.id_user,
            'Name' : self.Name,
            'Email': self.Email,
            'Password': self.Password,
            'Roll' : self.Roll,
        }

class Department(db.Model):
    __tablename__ = 'department'
    id_department = db.Column(db.Integer, primary_key = True)
    Name = db.Column(db.String(100))
    Decription = db.Column(db.String(100))
    detaildepartment_department = db.relationship('DetailDepartment', backref = 'detaildepartment_department' , lazy = True)
    def get_id(self):
        return(self.id_department)
    def serialize(self):
        return{
            'id_department': self.id_department,
            'Name' : self.Name,
            'Decription': self.Decription,
        }

class DetailDepartment(db.Model):
    __tablename__ = 'detaildepartment'
    id = db.Column(db.Integer ,primary_key = True)
    id_department = db.Column(db.Integer, db.ForeignKey('department.id_department'), nullable = False)
    id_user = db.Column(db.Integer ,db.ForeignKey('users.id_user'), nullable = False)
    def get_id(self):
        return(self.id)


class faces(db.Model):
    __tablename__ = 'faces'
    id_face = db.Column(db.Integer , primary_key = True)
    id_user = db.Column(db.Integer, db.ForeignKey('users.id_user'), nullable = False)
    image_url = db.Column(db.String(200))   
    created_at = db.Column(db.DateTime, server_default=func.now())
    id_session = db.Column(db.Integer, db.ForeignKey('sessions.session_id'), nullable = False)


class sessions(db.Model):
    __tablename__ = 'sessions'
    session_id = db.Column(db.Integer , primary_key = True)
    id_user = db.Column(db.Integer, db.ForeignKey('users.id_user'), nullable = False)
    id_work_schedule = db.Column(db.Integer, db.ForeignKey('work_schedule.id_work_schedule'), nullable = False)
    token = db.Column(db.String(200)) 
    created_at = db.Column(db.DateTime, server_default=func.now())
    sesstions_faces = db.relationship('faces', backref = 'session_faces' , lazy = True)

class work_schedule(db.Model):
    __tablename__ ='work_schedule'
    id_work_schedule = db.Column(db.Integer , primary_key = True)
    work_name = db.Column(db.String(100))
    work_date = db.Column(db.Date)
    start_time = db.Column(db.Time)
    end_time = db.Column(db.Time)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id_user'), nullable = False)
    work_schedule_sesstions = db.relationship('sessions', backref = 'work_schedule_session' , lazy = True)