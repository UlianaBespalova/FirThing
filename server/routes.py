from flask import jsonify
from server import app


@app.route('/hello', methods=['GET'])
def start():

    print("I'm alive")

    iv = ["1", "11111"]
    resp = jsonify(iv)
    resp.status_code = 200
    return resp

