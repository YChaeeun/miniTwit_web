from flask import Flask, jsonify, request

app          = Flask(__name__)
app.id_count = 1
app.users    = {}

@app.route("/ping", methods=['GET'])
def ping():
    return "pong"


@app.route("/join", methods=['POST'])
def join() :
    new_user                = request.json
    new_user['id']          = app.id_count
    app.users[app.id_count] = new_user
    app.id_count            = app.id_count+1

    return jsonify(new_user)
