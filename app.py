from flask import Flask, jsonify, request
from flask.json import JSONEncoder

app          = Flask(__name__)
app.id_count = 1
app.users    = {}

app.tweets = []

class CustomJSONEncoder(JSONEncoder) :
    def default(self, obj) :
        if isinstance(obj,set) :
            return list(obj)

        return JSONEncoder.default(self,obj)
app.json_encoder = CustomJSONEncoder


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

@app.route("/wTweet", methods=['POST'])
def wTweet() :

    playload        = request.json
    user_id         = int(playload['id'])
    new_tweet       = playload['tweet']

    if user_id not in app.users :
        return '사용자가 존재하지 않습니다', 400
    if len(new_tweet) > 300 :
        return '300자를 초과했습니다', 400

    
    app.tweets.append({
        'user_id' : user_id,
        'new_tweet' : new_tweet
    })
    return '', 200

@app.route('/follow', methods=['POST'])
def follow() :
    playload              = request.json
    user_id               = int(playload['id'])
    user_to_follow_id     = int(playload['follow'])


    if user_id not in app.users or user_to_follow_id not in app.users :
        return '사용자가 존재하지 않습니다', 400

    user = app.users[user_id]

    user.setdefault('follow', set()).add(user_to_follow_id)
    return jsonify(user)