from core.views_dashboard import check_jwt
from . import app
from flask import request, jsonify, session
from flask_jwt_extended import get_jwt_identity, jwt_required


@app.route("/jwt-test", methods=["GET", "POST"])
# @jwt_required()
def protected():
    if request.method in ['GET', 'POST']:
        email, user_type = check_jwt(session)
        # Access the identity of the current user with get_jwt_identity
        current_user = email # get_jwt_identity()
        print('current_user: ', current_user)
        if current_user:
            return jsonify(msg="Logged in, {}".format(current_user)), 200

    else:
        return jsonify({"msg": "Bad API Method"}), 401

