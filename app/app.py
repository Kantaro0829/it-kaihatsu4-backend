from flask import Flask, jsonify, make_response, request, abort
import hashlib#ハッシュ化用
from sqlalchemy import exc, func
from werkzeug.exceptions import RequestURITooLarge
from flask_cors import CORS, cross_origin


from setting import session# セッション変数の取得
from db import *# Userモデルの取得

from user_registry import UserLogin, UserRegistry, WordService, ToeicService
from jwt_auth import JwtAuth


app = Flask(__name__)
CORS(app, support_credentials=True)
app.config['JSON_AS_ASCII'] = False

print(hashlib.sha256('password'.encode()).hexdigest())
@app.route("/", methods=['GET'])
@cross_origin(supports_credentials=True)
def index():
    return jsonify({"status":200})

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5000, threaded=True, debug=True)