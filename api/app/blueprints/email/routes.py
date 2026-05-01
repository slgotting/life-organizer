import time
# from app import sql_db
# from app import mongo_db as db
from app import sql_db as db
from flask import request, render_template, jsonify, current_app
from app.blueprints.sql.models import IPAddress
from app.blueprints.email import bp
from app.blueprints.email.email import send_email
from pprint import pprint

# @bp.route('/pw_req', methods=["POST"])
# def pressure_wash_request():
#     try:
#         send_email(
#             'Pressure wash request',
#             'Buford Pressure Wash, LLC',
#             ['sgotting21@gmail.com'],
#             '',
#             html_body=render_template(
#                 'email/pressure_wash_request.html',
#             )
#         )
#         return jsonify({'success': True, 'message': 'Request sent successfully', 'description': 'We will contact you by the end of the day with your personalized quote. Thank you!'})

#     except:
#         current_app.logger.exception('Quote request error')
#         return jsonify({'success': False, 'message': 'An unexpected error occurred', 'description': 'Please give us a call at 678-752-7320'})
