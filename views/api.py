import json
from . import crypto_key, db, conn, removeItemFromList, updateItemFromList

from datetime import datetime as dt
from datetime import timezone as tz
from flask import Blueprint, request, url_for, jsonify, make_response
from flask import current_app as app
from flask_login import current_user, login_required
from models.models import Appointments, CatalogIDDocumentTypes, CatalogUserRoles, CatalogServices, Country, RTCOnlineUsers, ServicesSupplement, Surveys, SurveysAnswered
from models.models import User, UserExtraInfo, UserXEmployeeAssigned, UserXRole
from sqlalchemy import and_, column, func, join, select, text
api = Blueprint('api', __name__, template_folder='templates', static_folder='static')

# Set the Appointment's Details
@api.route('/api/detail/appointment/', methods = ['POST'])
# @login_required
def _d_appointment():
    app.logger.debug('** SWING_CMS ** - API Appointment Detail')
    try:
        # POST: Save Appointment
        if request.method == 'POST':
            usr_id = request.json['uid']
            emp_id = request.json['eid']
            srv_id = request.json['sid']
            sch_date = request.json['sch']
            usr_data = request.json['udata']

            # Update User information
            if usr_data is not None:
                _u_userinfo(usr_data)

            # Get scheduled hours in UTC - Javascript Timestamp needs to be divided by 1000 (miliseconds)
            scheduled_dt = dt.fromtimestamp((sch_date / 1000), tz.utc)
            # Get Service ID
            service = CatalogServices.query.filter_by(name_short = srv_id).first()
            # Get Employee Assigned ID
            employee_assigned = UserXEmployeeAssigned.query.filter_by(
                employee_id = emp_id,
                enabled = True,
                service_id = service.id,
                user_id = usr_id
            ).order_by(UserXEmployeeAssigned.datecreated.desc()).first()

            if employee_assigned is None:
                employee_assigned = UserXEmployeeAssigned()
                employee_assigned.employee_id = emp_id
                employee_assigned.user_id = usr_id
                employee_assigned.service_id = service.id
                db.session.add(employee_assigned)
            
            appointment = Appointments()
            appointment.created_by = current_user.id
            appointment.created_for = usr_id
            appointment.date_scheduled = scheduled_dt
            appointment.emp_assigned = employee_assigned.id
            appointment.service_id = service.id
            if not current_user.is_user_role(['usr']):
                appointment.emp_accepted = True
            db.session.add(appointment)

            db.session.commit()

            return jsonify({ 'status': 200, 'msg': 'Cita creada' })
    except Exception as e:
        app.logger.error('** SWING_CMS ** - API Appointment Detail Error: {}'.format(e))
        return jsonify({ 'status': 'error', 'msg': repr(e) })

# Update the Appointment's Details
@api.route('/api/detail/extra_info/', methods = ['PUT'])
# @login_required
def _d_update_appointment():
    app.logger.debug('** SWING_CMS ** - API Update extra_info')
    try:
        # POST: Save Appointment
        if request.method == 'PUT':
            usr_data = request.json['data']

            # Update User information
            if usr_data is not None:
                _u_userinfo(usr_data)
            return jsonify({ 'status': 201, 'msg': 'Información actualizada' })
    except Exception as e:
        app.logger.error('** SWING_CMS ** - API Update extra_info Error: {}'.format(e))
        return jsonify({ 'status': 'error', 'msg': repr(e) })

# Get the Service's Details
@api.route('/api/detail/service/<string:service_id>/', methods = ['GET'])
# @login_required
def _d_service(service_id = None):
    app.logger.debug('** SWING_CMS ** - API Service Detail')
    try:
        if request.method == 'GET':
            if service_id is not None:
                response = {
                    'break_minutes': None,
                    'duration_minutes': None,
                    'enabled': None,
                    'id': None,
                    'name': None,
                    'name_short': None,
                    'service_user_role': None,
                    'sessions_schedule': None,
                    'status': 404
                }

                detail = CatalogServices.query.filter(CatalogServices.name_short == service_id).first()
                if detail is not None:
                    response['status'] = 200
                    response['id'] = detail.id
                    response['name'] = detail.name
                    response['name_short'] = detail.name_short
                    response['break_minutes'] = detail.break_minutes
                    response['duration_minutes'] = detail.duration_minutes
                    response['sessions_schedule'] = detail.sessions_schedule
                    response['enabled'] = detail.enabled
                    if detail.service_user_role is not None:
                        serv_ur = CatalogServices.query.filter_by(id = detail.service_user_role).first()
                        response['service_user_role'] = serv_ur.name_short

                return jsonify(response)
            else:
                return jsonify({ 'status': 400 })
        
    except Exception as e:
        app.logger.error('** SWING_CMS ** - API Service Detail Error: {}'.format(e))
        return jsonify({ 'status': 'error', 'msg': repr(e) })


# Get the User's Details
@api.route('/api/detail/user/<int:user_id>/', methods = ['GET'])
# @login_required
def _d_user(user_id = None):
    app.logger.debug('** SWING_CMS ** - API User Detail')
    try:
        if request.method == 'GET':
            if user_id is not None:
                response = {
                    'alias': None,
                    'birthdate': None,
                    'city': None,
                    'country': None,
                    'email': None,
                    'enabled': None,
                    'id': user_id,
                    'last_names': None,
                    'name': None,
                    'names': None,
                    'national_id': None,
                    'national_id_type': None,
                    'phonenumber': None,
                    'extra_data_form': None,
                    'roles': None,
                    'state': None,
                    'status': 404
                }

                detail = User.query.filter(User.id == user_id).first()
                if detail is not None:
                    response['status'] = 200
                    response['id'] = user_id
                    response['name'] = detail.name
                    response['email'] = detail.email
                    response['phonenumber'] = detail.phonenumber
                    response['enabled'] = detail.enabled
                    response['roles'] = detail.get_user_roles(True)
                    if detail.birthdate is not None:
                        response['birthdate'] = detail.birthdate.strftime('%Y-%m-%d')
                    if detail.extra_info is not None:
                        if detail.extra_info.national_id_type is not None:
                            natid = CatalogIDDocumentTypes.query.filter_by(id = detail.extra_info.national_id_type).first()
                            response['national_id_type'] = natid.name_short
                        response['national_id'] = detail.extra_info.national_id
                        response['last_names'] = detail.extra_info.last_names
                        response['names'] = detail.extra_info.names
                        response['alias'] = detail.extra_info.alias
                        response['country_id'] = detail.extra_info.country_id
                        response['state'] = detail.extra_info.state
                        response['city'] = detail.extra_info.city
                        response['extra_data_form'] = detail.extra_info.extra_data_form

                return jsonify(response)
            else:
                return jsonify({ 'status': 400 })
        
    except Exception as e:
        app.logger.error('** SWING_CMS ** - API User Detail Error: {}'.format(e))
        return jsonify({ 'status': 'error', 'msg': repr(e) })


# Get a list of Appointments
@api.route('/api/list/appointments/<string:cmds>/<int:user_id>/', methods = ['GET'])
# @login_required
def _l_appointments(cmds = None, user_id = None):
    app.logger.debug('** SWING_CMS ** - API List Appointments')
    try:
        if request.method == 'GET':
            if cmds is not None and user_id is not None:
                cmd_lst = cmds.split('-')
                dt_today = dt.now(tz.utc).replace(hour=0, minute=0, second=0, microsecond=0)
                
                response = {
                    'appointments': [],
                    'datetime': dt_today,
                    'id': user_id,
                    'status': 404
                }

                for cmd in cmd_lst:
                    details = None
                    
                    if cmd == 'assigned':
                        # Appointments - emp_assigned
                        details = Appointments.query.join(UserXEmployeeAssigned).filter(
                            Appointments.date_scheduled > dt_today,
                            UserXEmployeeAssigned.user_id == Appointments.created_for,
                            UserXEmployeeAssigned.employee_id == user_id,
                            Appointments.cancelled == False
                        ).order_by(Appointments.date_scheduled.asc())
                    elif cmd == 'by':
                        # Appointments - created_by
                        details = Appointments.query.filter(
                            Appointments.created_by == user_id,
                            Appointments.cancelled == False,
                            Appointments.date_scheduled > dt_today
                        ).order_by(Appointments.date_scheduled.asc())
                    elif cmd == 'for':
                        # Appointments - created_for
                        details = Appointments.query.filter(
                            Appointments.created_for == user_id,
                            Appointments.cancelled == False,
                            Appointments.date_scheduled > dt_today
                        ).order_by(Appointments.date_scheduled.asc())
                    
                    if details is not None:
                        response['status'] = 200
                        for record in details:
                            usr_for = User.query.filter_by(id = record.created_for).first()
                            emp_crt = User.query.filter_by(id = record.created_by).first()
                            emp_tab = UserXEmployeeAssigned.query.filter_by(id = record.emp_assigned).first()
                            emp_asg = User.query.filter_by(id = emp_tab.employee_id).first()
                            service = CatalogServices.query.filter_by(id = record.service_id).first()
                            
                            response['appointments'].append({
                                'id': record.id,
                                'appointment_type': cmd,
                                'cancelled': record.cancelled,
                                'created_by': {
                                    'name': emp_crt.name
                                },
                                'created_for': {
                                    'attended': record.usr_attendance,
                                    'name': usr_for.name
                                },
                                'date_created': record.date_created,
                                'date_scheduled': record.date_scheduled,
                                'emp_assigned': {
                                    'accepted': record.emp_accepted,
                                    'attended': record.emp_attendance,
                                    'name': emp_asg.name
                                },
                                'service': {
                                    'duration': service.duration_minutes,
                                    'name': service.name,
                                    'name_short': service.name_short
                                }
                            })

                return jsonify(response)
            else:
                return jsonify({ 'status': 400 })
            
    except Exception as e:
        app.logger.error('** SWING_CMS ** - API List Appointments Error: {}'.format(e))
        return jsonify({ 'status': 'error', 'msg': repr(e) })


# Get a list of Users
@api.route('/api/list/users/', methods = ['GET'])
# @login_required
def _l_users():
    app.logger.debug('** SWING_CMS ** - API List Users')
    try:
        if request.method == 'GET':
            query = request.args.get('qry')
            filters = request.args.get('flt')
            filters_type = request.args.get('ft')

            if query is not None:
                ulist, total = User.search(query, 1, 5)

                # Check if there is a User Role Filter parameter and Filter by it
                if filters is not None and filters != '':
                    userRolesFilters = filters.split('-')
                    
                    # Check if the Filters are of type Servie User Role
                    if filters_type is not None and filters_type == 'sur':
                        newUserRolesFilters = []
                        
                        services = CatalogServices.query.filter(CatalogServices.name_short.in_(userRolesFilters))
                        for service in services:
                            user_role = CatalogUserRoles.query.filter(CatalogUserRoles.id == service.service_user_role).first()
                            if user_role is not None:
                                newUserRolesFilters.append(user_role.name_short)
                        
                        userRolesFilters = newUserRolesFilters

                    ulistFiltered = []
                    for user in ulist:
                        if user.is_user_role(userRolesFilters):
                            ulistFiltered.append(user)
                    ulist = ulistFiltered
                    total = len(ulistFiltered)

                response = {
                    'r_filter': filters,
                    'r_total': total,
                    'records': [],
                    'status': 404
                }

                if total > 0:
                    response['status'] = 200
                    for usr in ulist:
                        response['records'].append({
                            'u_id': usr.id,
                            'u_name': usr.name,
                            'u_email': usr.email
                        })
                
                return jsonify(response)
            else:
                return jsonify({ 'status': 400 })
        
    except Exception as e:
        app.logger.error('** SWING_CMS ** - API List Users Error: {}'.format(e))
        return jsonify({ 'status': 'error', 'msg': repr(e) })


# Update User Info
def _u_userinfo(js):
    app.logger.debug('** SWING_CMS ** - API Save User Info')
    try:
        user = User.query.filter_by(id = js['id']).first()
        
        if user.extra_info is None:
            user_extra = UserExtraInfo()
            user_extra.id = user.id
            
            db.session.add(user_extra)
            db.session.commit()
            user.extra_info = user_extra
            # db.session.refresh(user)
        
        if js.get('alias') is not None:
            user.extra_info.alias = js['alias']
        if js.get('names') is not None:
            user.extra_info.names = js['names']
        if js.get('last_names') is not None:
            user.extra_info.last_names = js['last_names']
        if js.get('country_id') is not None:
            user.extra_info.country_id = js['country_id']
        if js.get('state') is not None:
            user.extra_info.state = js['state']
        if js.get('city') is not None:
            user.extra_info.city = js['city']
        if js.get('extra_data_form') is not None:
            user.extra_info.extra_data_form = js['extra_data_form']
        if js.get('national_id_type') is not None:
            natid = CatalogIDDocumentTypes.query.filter_by(name_short = js['national_id_type']).first()
            user.extra_info.national_id = js['national_id']
            user.extra_info.national_id_type = natid.id

        if js.get('birthdate') is not None:
            date_format = '%Y-%m-%d'
            user.birthdate = dt.strptime(js['birthdate'], date_format)
        if js.get('phonenumber') is not None:
            user.phonenumber = js['phonenumber']
        
        db.session.add(user)
        db.session.commit()

    except Exception as e:
        app.logger.error('** SWING_CMS ** - API Save User Info Error: {}'.format(e))
        return jsonify({ 'status': 'error', 'msg': repr(e) })

# Get a list countries
@api.route('/api/list/countries', methods = ['GET'])
def list_countries():
    app.logger.debug('** SWING_CMS ** - API get countries')
    try:
        if request.method == 'GET':
            response = {
                'data': None,
                'status': 404
            }
        result = Country.query.all()
        if result is not None:
            response['status'] = 200
            response['data'] = list(map(lambda x: dict(x), result))
        return jsonify(response)
        
    except Exception as e:
        app.logger.error('** SWING_CMS ** - API User Detail Error: {}'.format(e))
        return jsonify({ 'status': 'error', 'msg': repr(e) })


# Get a country by id
@api.route('/api/list/countries/<int:country_id>', methods = ['GET'])
def get_country_by_id(country_id = None):
    app.logger.debug('** SWING_CMS ** - API get countries')
    try:
        if request.method == 'GET':
            if country_id is not None:
                response = {
                    'data': None,
                    'status': 404
                }
        country = Country.query.filter(Country.id == country_id).first()
        if country is not None:
            response['status'] = 200
            response['data'] = dict(country)
        return jsonify(response)
        
    except Exception as e:
        app.logger.error('** SWING_CMS ** - API User Detail Error: {}'.format(e))
        return jsonify({ 'status': 'error', 'msg': repr(e) })

# Get the filtered data
@api.route('/api/report/filters', methods=['POST'])
def _r_kpi():
    app.logger.debug('** SWING_CMS ** - API User Detail')
    try:
        if request.method == 'POST':
            response = {
                'data': None,
                'status': 404
            }
        filter_data = request.json
        """
        query = sqlalchemy.select([
            BOOKS.c.genre, sqlalchemy.func.sum(BOOKS.c.book_price)
        ]).order_by(BOOKS.c.genre).group_by(BOOKS.c.genre)
        """
        join_tables = join(User, UserXRole, and_(User.id == UserXRole.user_id, UserXRole.user_role_id == 1))
        # join_tables = join(User, UserXRole) sin filtros
        # SELECT * [ --> FROM user inner join user_x_role on user.id = user_x_role.user_id AND user_x_role.user_role_id = 1
        columns = []

        # SELECT clause
        if filter_data.get('select', None) is not None:
            for table in filter_data["select"]:
                if table != 'user':
                    join_tables = add_join_table(joins=join_tables, tablenames=filter_data["select"], tablename=table)
                for field in filter_data["select"][table]:
                    if type(field) is dict:
                        field_key = ''
                        field_dict = None
                        for key in field:
                            field_key = key
                            field_dict = field[key]
                        function_select = add_function_to_query(table, field=field_key, value=field_dict)
                        print(function_select)
                        columns.append(function_select)
                    else:
                        columns.append(text('%s.%s' % (table, field)))
                    # SELECT [columns] FROM ... Ej. [user.id, counties.name, extra_data_user.names]
                    # User.id, Country.name
        query = select(columns).select_from(join_tables)

        # Filter clause
        if filter_data.get('filters', None) is not None:
            for table in filter_data["filters"]:
                for field in filter_data["filters"][table]:
                    if type(filter_data["filters"][table][field]) is str:
                        query = query.filter(text('%s.%s = \'%s\'' % (table, field, filter_data["filters"][table][field])))
                    elif type(filter_data["filters"][table][field]) is dict:
                        function_filter = add_function_to_query(table, field, value=filter_data["filters"][table][field])
                        print(function_filter)
                        query = query.filter(function_filter)
                    else:
                        query = query.filter(text('%s.%s = %s' % (table, field, filter_data["filters"][table][field])))
            # WHERE [--> user.id = 2 AND country.name = 'Honduras'

        # Order clause
        if filter_data.get('order', None) is not None:
            for table in filter_data["order"]:
                for fields in filter_data["order"][table]:
                    for field in fields:
                        order = 'DESC'
                        if fields[field] == 1:
                            order = 'ASC'
                        query = query.order_by(text('%s.%s %s' % (table, field, order)))

        # Group clause
        if filter_data.get('group', None) is not None:
            for table in filter_data["group"]:
                for field in filter_data["group"][table]:
                    query = query.group_by(text('%s.%s' % (table, field)))
            # ORDER BY [--> user.birthdate DESC, country.name DESC
        # query.filter(text("id = 1"))
        #query = select(User).join(UserXRole, )
        print(query)
        #result = query.all()
        result = conn.execute(query).all()
        if result is not None:
            response['status'] = 200
            response['data'] = list(map(lambda x: dict(x), result))

        return jsonify(response)
        #result = conn.execute(get_kpis()).one()
        #return json.dumps(dict(result))
    except Exception as e:
        app.logger.error('** SWING_CMS ** - API User Detail Error: {}'.format(e))
        return jsonify({'status': 'error', 'msg': repr(e)})

# For define joins for dynamic filters
def add_join_table(joins, tablenames, tablename):
    
    switcher = {
        'user_extra_info': user_extra_info,
        'catalog_id_document_types': catalog_id_document_types,
        'countries': countries,
        'appointments': appointments,
        'catalog_services': catalog_services,
        'services_supplement': services_supplement,
        'user_x_employees_assigned': user_x_employees_assigned,
        'rtc_online_users': rtc_online_users,
        'surveys_answered': surveys_answered,
        'surveys': surveys
    }
    func = switcher.get(tablename, default_join)
    return func(joins, tablenames)

# Methods por joins

def user_extra_info(joins, tablenames):
    # left outer join user_extra_info on user.id = user_extra_info.id
    return join(joins, UserExtraInfo, isouter=True)

def catalog_id_document_types(joins, tablenames):
    # left outer join user_extra_info on user.id = 
    return join(joins, CatalogIDDocumentTypes, UserExtraInfo.catalog_id_document_types == CatalogIDDocumentTypes.id, isouter=True)

def countries(joins, tablenames):
    if tablenames.get('user_extra_info', None) is None:
        joins = join(joins, UserExtraInfo, isouter=True)
        # left outer join user_extra_info on user.id = user_extra_info.id
    # left outer join countries on user_extra_info.country_id = countries.id
    return join(joins, Country, isouter=True)

def appointments(joins, tablenames):
    joins = join(joins, Appointments, isouter=True)

def catalog_services(joins, tablenames):
    if tablenames.get('appointments', None) is None and tablenames.get('surveys', None) is None and tablenames.get('surveys_answered', None) is None and tablenames.get('user_x_employees_assigned', None) is None:
        joins = join(joins, Appointments, isouter=True)
    joins = join(joins, CatalogServices, isouter=True)

def services_supplement(joins, tablenames):
    if tablenames.get('appointments', None) is None and tablenames.get('catalog_services', None) is None and tablenames.get('surveys_answered', None) is None and tablenames.get('user_x_employees_assigned', None) is None:
        joins = join(joins, Appointments, isouter=True)
    joins = join(joins, ServicesSupplement, isouter=True)

def user_x_employees_assigned(joins, tablenames):
    if tablenames.get('appointments', None) is None and tablenames.get('catalog_services', None) is None and tablenames.get('surveys_answered', None) is None and tablenames.get('surveys', None) is None:
        joins = join(joins, Appointments, isouter=True)
    joins = join(joins, UserXEmployeeAssigned, isouter=True)

def surveys_answered(joins, tablenames):
    if tablenames.get('appointments', None) is None and tablenames.get('catalog_services', None) is None and tablenames.get('surveys', None) is None and tablenames.get('user_x_employees_assigned', None) is None:
        joins = join(joins, Appointments, isouter=True)
    joins = join(joins, SurveysAnswered, isouter=True)

def surveys(joins, tablenames):
    if tablenames.get('appointments', None) is None and tablenames.get('catalog_services', None) is None and tablenames.get('surveys_answered', None) is None and tablenames.get('user_x_employees_assigned', None) is None:
        joins = join(joins, Appointments, isouter=True)
    if tablenames.get('surveys_answered', None) is None:
        joins = join(joins, surveys_answered, isouter=True)
    joins = join(joins, Surveys, isouter=True)

def rtc_online_users(joins, tablenames):
    joins = join(joins, RTCOnlineUsers, isouter=True)

def default_join(joins):
    return joins

# Methods for add functions for filters logics
def add_function_to_query(table, field, value):
    function = ''
    newValue = ''
    for key in value:
        function = key
        newValue = value[key]
        break
    switcher = {
        '$not': function_not,
        '$eq': function_equal,
        '$neq': function_not_equal,
        '$in': function_in,
        '$nin': function_not_in,
        '$between': function_between,
        '$count': function_count,
        '$sum': function_sum,
        '$max': function_max,
        '$min': function_min,
        '$avg': function_avg,
        '$like': function_like,
        '$ilike': function_ilike
    }
    func = switcher.get(function.lower(), default_filter)
    return func(table, field, value = newValue)

# Functions defined that can be useful in filters
def validate_type_dict(value):
    return 

def function_not(table, field, value):
    return ~column('%s' % (field))

def function_equal(table, field, value):
    if type(value) is str:
        return text('%s.%s = \'%s\'' % (table, field, value))
    return text('%s.%s = %s' % (table, field, value))

def function_not_equal(table, field, value):
    if type(value) is str:
        return text('%s.%s <> \'%s\'' % (table, field, value))
    return text('%s.%s <> %s' % (table, field, value))

def function_in(table, field, value):
    return column('%s' % (field)).in_(value)

def function_not_in(table, field, value):
    return ~column('%s' % (field)).in_(value)

def function_between(table, field, value):
    return column('%s' % (field)).between(value[0], value[1])
    
def function_count(table, field, value):
    return func.count(text('%s.%s' % (table, field)))

def function_sum(table, field, value):
    return func.sum(text('%s.%s' % (table, field)))

def function_max(table, field, value):
    return func.max(text('%s.%s' % (table, field)))

def function_min(table, field, value):
    return func.min(text('%s.%s' % (table, field)))

def function_avg(table, field, value):
    return text('CAST(avg(%s.%s) AS FLOAT) as %s' % (table, field, value))

def function_like(table, field, value):
    return text('%s.%s like \'%s\'' % (table, field, value))

def function_ilike(table, field, value):
    return text('%s.%s ilike \'%s\'' % (table, field, value))

def default_filter(table, field, value):
    if type(value) is str:
        return text('%s.%s = \'%s\'' % (table, field, value))
    return text('%s.%s = %s' % (table, field, value))

def function_call(table, field, value):
    return