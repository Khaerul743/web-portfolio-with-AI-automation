from flask import jsonify

def response(message, data, status):
    return jsonify({"message":message, "data":data}), status