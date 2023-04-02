from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Users(db.Model):
    __tablename__ = 'users'
    id_user = db.Column(db.Integer, primary_key = True)
    Name = db.Column(db.String(100))
    Email = db.Column(db.String(100))
    Password = db.Column(db.String(100))
    Roll = db.Column(db.Integer)
    detaildepartment_user = db.relationship('DetailDepartment', backref = 'detaildepartment_user' , lazy = True)
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
