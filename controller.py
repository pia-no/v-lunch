import json
from urllib import parse

import test
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/party", methods=['GET'])
def getParty():
    return jsonify(test.getParty())


@app.route("/slackAction", methods=['POST'])
def slackAction():
    prefix = "payload="
    data = request.get_data(as_text=True)[len(prefix):]
    app.logger.info("req_data %s", data)

    slack_req_body = json.loads(parse.unquote_plus(data))
    app.logger.info("Action body: %s", slack_req_body)

    name = slack_req_body.get("user").get("name")
    action = slack_req_body.get("actions")[0].get("value")
    test.slackAction(name, action)

    return json.dumps({})

@app.route("/startLunch", methods=['GET'])
def startLunch():
    channelName = request.args.get("channel")
    test.sendJoinParty(channel=channelName)
    return json.dumps({})

@app.route("/partyIs", methods=['GET'])
def partyIs():
    test.test()
    return json.dumps({})

@app.route("/init", methods=['GET'])
def initParty():
    test.initFilterList()
    return json.dumps({})
app.run(host="0.0.0.0")