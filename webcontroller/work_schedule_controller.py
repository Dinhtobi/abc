
from flask import Blueprint, render_template, request, redirect, url_for, jsonify,json,Response,abort
from webmodel.models import *
from datetime import datetime ,timedelta
work_schedule_controller = Blueprint('work_schedule_controller', __name__, url_prefix='/api/work_schedule')


@work_schedule_controller.route('/getby', methods=['POST'])
def getallSessionbyPageandiddepartment():
    try:
        id_department = request.form['id_department']
        page = request.form['page']
        if page :
            now = datetime.now()
            days = 5*int(page)
            days_ago = now - timedelta(days)
            fivedayago = days_ago.strftime("%Y-%m-%d")
            if page != 1 :
                day2 =5*(int(page)-1)
                day_now = now - timedelta(day2)
                daynow = day_now.strftime("%Y-%m-%d")
            else :
                daynow = now.strftime("%Y-%m-%d")
            work_schedules = Work_schedule.query.filter(Work_schedule.work_date <= daynow, Work_schedule.work_date  >= fivedayago).filter_by(id_department = id_department).order_by(Work_schedule.work_date.desc()).all()
            serialized_list_work_schedule = []
            for i in work_schedules:
                listsession = Sessions.query.filter_by(id_work_schedule = i.id_work_schedule).all()
                serialized_list_employstatus = []
                users = Users.query.filter_by(id_department=id_department).all()
                for k in users:
                    found = False
                    for j in listsession:
                        if k.id_user == j.id_user:
                            found = True
                            session = j
                            break
                    if not found : 
                        session = None
                    serialized_employstatus = serialize_employstatus(session,k)
                    serialized_list_employstatus.append(serialized_employstatus)
                
                serialized_employstatus = serialize_work_schedule(i.work_date ,serialized_list_employstatus )
                serialized_list_work_schedule.append(serialized_employstatus)
            data = {"listwork_schedules": serialized_list_work_schedule}
            return jsonify(list(serialized_list_work_schedule))
        else :
            return 'null'
    except Exception as e:
        print(e)

@work_schedule_controller.route('/', methods=['GET'])
def getWork_schedules():
    # try:
        id_employee = request.json['id_employee']
        start_day = request.json['start_day'].encode('utf8')
        end_day = request.json['end_day'].encode('utf8')
        user = Users.query.filter_by(id_user = id_employee).first()
        work_schedules = Work_schedule.query.filter(Work_schedule.work_date <= end_day, Work_schedule.work_date  >= start_day).filter_by(id_department = user.id_department).order_by(Work_schedule.work_date.desc()).all()
        listwork_schedule = []
        for i in work_schedules:
            print(i.id_work_schedule)
            listwork_schedule.append(serialize_work_schedule_one_employee(i))
        return jsonify(listwork_schedule)
    # except Exception as e:
    #     print(e)

def serialize_work_schedule(date , listsession ):
    return{
        'date': date,
        'employeeStatuses' : listsession
    }   
def serialize_employstatus( session ,user):
    if session != None:
        if session.session_id :
            status = 1
            time = session.created_at
    else :
        status = 0 
        time = ''
    return{
        'id' : user.id_user,
        'img_avatar' : user.img_avatar,
        'roll_name' : user.rolename,
        'name' : user.name,
        'status' : status,
        'time': time,
    }   
def serialize_work_schedule_one_employee(work_schedule):
    return{
        'id' : work_schedule.id_work_schedule ,
        'work_date' : work_schedule.work_date ,
        'start_time': work_schedule.start_time.isoformat(),
        'end_time': work_schedule.end_time.isoformat(),
    }