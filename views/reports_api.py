import decimal
import json

from . import crypto_key, db, conn, removeItemFromList, updateItemFromList

from datetime import datetime as dt, datetime
from datetime import timezone as tz
from flask import Blueprint, request, url_for, jsonify, make_response
from flask import current_app as app
from flask_login import current_user, login_required
from models.models import Appointments, CatalogIDDocumentTypes, CatalogUserRoles, CatalogServices
from models.models import User, UserExtraInfo
from models.queries import *
reports_api = Blueprint('reports_api', __name__, template_folder='templates', static_folder='static')


# Get the KPI's Report
@reports_api.route('/api/report/kpis', methods=['GET'])
def _r_kpi():
    app.logger.debug('** SWING_CMS ** - API User Detail')
    try:
        result = conn.execute(get_kpis()).one()
        return json.dumps(dict(result))
    except Exception as e:
        app.logger.error('** SWING_CMS ** - API User Detail Error: {}'.format(e))
        return jsonify({'status': 'error', 'msg': e})