from flask import jsonify, render_template, redirect, url_for, request, g
from models import *
from app import app, db, auth
from datetime import datetime
import json


# helper functions handle routing error handling etc
@app.errorhandler(404)
def page_not_found(e = ""):
    return jsonify({"err": "404 error page not found"}), 404

@app.errorhandler(403)
def not_authorized(e = ""):
    return jsonify({"err": "403 not authorized. Sorry but you are not authorized to perform operations on this content"}), 403

@app.errorhandler(400)
def something_missing(e = ""):
    return jsonify({"err": "Arguments provided were not enough to carry out this request"}), 400

@app.errorhandler(500)
def internal_error(e = ""):
    return jsonify({"err": "Hmm looks like our servers are not working the way they should be. Kindly try again after sometime"}), 500

def as_msg(s, errors = []):
    return jsonify({"err": "there seems to be some error", "description": s, "errors": []})

def as_success(s, di = {}, warnings = [], errors = []):
    d = {}
    if not len(errors) == 0:
        d["errors"] = errors
    if not len(warnings) == 0:
        d["warnings"] = warnings
    d["success"] = s
    d.update(di)
    return jsonify(d)

@app.before_request
def before_request():
    g.user = None
    if not request.json:
        return
    else:
        if request.json.has_key("user_token"):
            user = User.verify_auth_token(request.json["user_token"])
            g.user = user

@auth.verify_password
def verify_password(username = "", password = ""):
    if g.user:
        return True
    else:
        return False

@app.after_request
def after_request(response):
    try:
        user_token = request.json["user_token"]
        data = json.loads(response.get_data())
        data["user_token"] = user_token
        response.set_data(json.dumps(data))
    except Exception as e:
        pass
    return response

@app.route("/index", methods = ["GET", "POST"])
def index():
    return as_success("kamehameha")
