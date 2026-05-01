from flask import request, render_template, jsonify
from app.blueprints.referral import bp
from app.blueprints.referral.forms import RegistrationForm
from app.blueprints.referral.models import ReferringUser



# @bp.route('/query_credits', methods=["GET"])
# def query_credits():
#     current_app.db.collection('credits').find_one({'_id': 'credits'})

# @bp.route('/all_phone_credits', methods=["GET"])
# def all_phone_credits():
#     users = ReferringUser.objects.all()
#     print(users[0])
#     phone_credits = None
#     return jsonify({'success': True, 'phone_credits': phone_credits})

# @bp.route('/sign_up', methods=["GET", "POST"])
# def index():
#     if request.method == 'GET':
#         form = RegistrationForm()
#         return render_template('referral/sign_up.html', form=form)
