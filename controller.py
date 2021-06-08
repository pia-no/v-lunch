import json
import test
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/absent", methods=['GET'])
def absent():
    test.absent("absent_test")
    return json.dumps({})

@app.route("/join", methods=['POST'])
def join():
    test.join("POST_JOIN")
    return json.dumps({})


@app.route("/join", methods=['GET'])
def join2():
    test.join("GET_JOIN")
    return json.dumps({})

@app.route("/party", methods=['GET'])
def getParty():
    return jsonify(test.getParty())

# @app.route("slackAction")
# def action():
#     slackData = request.json
#     if slackData['user']:
#         return


app.run()