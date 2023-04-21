
from flask import Blueprint, render_template, request, redirect, url_for, jsonify,json,Response,abort
from webmodel.models import *
from datetime import datetime ,timedelta
work_schedule_controller = Blueprint('work_schedule_controller', __name__, url_prefix='/api/work_schedule')


@work_schedule_controller.route('/getby', methods=['POST'])
def getallSessionbyPageandiddepartment():
    # try:
        id_department = request.form['id_department']
        page = request.form['page']
        # users = Users.query.filter_by(id_department=id_department).all()
        if page :
            now = datetime.now()
            five_days_ago = now - timedelta(days=5)
            fivedayago = five_days_ago.strftime("%Y-%m-%d")
            daynow = now.strftime("%Y-%m-%d")
            work_schedules = work_schedule.query.filter(work_schedule.work_date <= daynow, work_schedule.work_date  >= fivedayago).filter_by(id_department = id_department).all()
            serialized_list_work_schedule = []
            for i in work_schedules:
                listsession = sessions.query.filter_by(id_work_schedule = i.id_work_schedule).all()
                serialized_list_employstatus = []
                users = Users.query.all()
                for k in users:
                    # user = Users.query.filter_by(id_user = j.id_user).first()
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
    # except Exception as e:
    #     print(e)

def serialize_work_schedule(date , listsession ):
    return{
        'Date': date,
        'list<work_schedule>' : listsession
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
        'roll_name' : user.Roll,
        'name' : user.Name,
        'status' : status,
        'time': time,
    }   