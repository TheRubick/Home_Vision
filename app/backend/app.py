from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
#from models import User, Course, Student, StaffMember, Semester, Requirement

from datetime import datetime



app = Flask(__name__)
CORS(app, support_credentials=True)

@app.route('/test',methods=['GET'])
def getStadiums():
    response = {'res':"there is data"}
    return jsonify(response)
