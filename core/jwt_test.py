from . import app
from flask import request, jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required


@app.route("/jwt-test", methods=["GET"])
@jwt_required()
def protected():
    if request.method == 'GET':
        # Access the identity of the current user with get_jwt_identity
        current_user = get_jwt_identity()
        print('current_user: ', current_user)
        if current_user:
            return jsonify(msg="Logged in, {}".format(current_user)), 200

    else:
        return jsonify({"msg": "Bad API Method"}), 401

