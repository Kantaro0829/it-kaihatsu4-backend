from flask import Flask, jsonify, make_response, request, abort
import hashlib#ハッシュ化用
from sqlalchemy import exc, func
from sqlalchemy.sql.expression import true
from sqlalchemy.sql.functions import user
from sqlalchemy.sql.operators import istrue
from werkzeug.exceptions import RequestURITooLarge
from flask_cors import CORS, cross_origin
import base64
import qrcode
import os


# from setting import session# セッション変数の取得
# from db import *# Userモデルの取得

from db import UserLogin, UserRegistry, GetLanguageCodes, RegistryHistory
from jwt_auth import JwtAuth
from deepl import GetTranslatedWord
import json
import time


app = Flask(__name__)
CORS(app, support_credentials=True)
app.config['JSON_AS_ASCII'] = False

@app.route("/", methods=['GET'])
@cross_origin(supports_credentials=True)
def index():
    return jsonify({"status":200})

@app.route("/new_user_reg", methods=["POST"])
@cross_origin(supports_credentials=True)
def new_user_reg():
    '''app
    受け取るJSON : user_info[]
    {
        "password": String,
        "email": String,
        "lang_id: Int 
    }

    '''
    user_info = json.loads(request.get_data().decode())#jsonデコード
    print(user_info)#辞書型配列

    #user table にレコードの追加
    try:
        ur = UserRegistry(user_info)
        dic_temp = ur.new_user_reg()#ユーザ登録
        jwt_auth = JwtAuth()#JsonWebToken生成用インスタンス
        #token生成
        token = jwt_auth.encode(dic_temp)
        temp = {
            "status": 200,
            "token": token
        }

        return jsonify(temp)
        
    except exc.SQLAlchemyError as e:#DB のエラーとメールアドレスがすでに登録されていた時の処理
        message = None
        if type(e) is exc.IntegrityError:
            message = "メールアドレスがすでに登録されています"
            print(type(e))
            return jsonify({
                "status": 400,
                "message": message,
        })
        return jsonify({"status":400, "massage":"DBに問題あるかも"})

@app.route("/login", methods=["POST"])
@cross_origin(supports_credentials=True)
def login():
    '''
    受け取るjson: user_info[]
    {
        "email": mail,
        "password": password
    }
    '''
    user_info = json.loads(request.get_data().decode())
    try:
        ul = UserLogin(user_info)
        id_and_lang_code = ul.login()

        print("out side of if")
        if id_and_lang_code['id'] != 0:
            print("inside of if")
            jwt_auth = JwtAuth()
            token = jwt_auth.encode(id_and_lang_code)
            print("token was created")
            return jsonify({"status":200, "token":token})

        return jsonify({
            "status": 400,
            "message": "正しいメールアドレスまたはパスワードを入力してください"
        })
    except:
        return jsonify({
            "status": 400,
            "message": "db のエラー？"
        })

@app.route("/get_lang_code", methods=["GET"])
@cross_origin(supports_credentials=True)
def get_lang_code():
    get_lang_code = GetLanguageCodes()
    data = get_lang_code.get_all_lang_code()

    if data:
        return jsonify({"status":200, "data":data})
    return jsonify({"status":400})


@app.route("/translate", methods=["POST"])
@cross_origin(supports_credentials=True)
def translate():
    """
    受け取るjson: user_info[]
    {
        token: String,
        text: String,
    }
    """
    token_and_text = json.loads(request.get_data().decode())
    jwt_auth = JwtAuth()
    id_lang_code = jwt_auth.decode(token_and_text['token'])#tokenをデコードしてIDとLang_codeを取り出す
    print(f'userIdと言語コード：{id_lang_code}')

    deepl = GetTranslatedWord(id_lang_code['lang_code'])
    b4_lang, aft_lang, b4_text, result_text = deepl.request_deepl_api(token_and_text['text'])
    reg_history = RegistryHistory()

    result = reg_history.insert_data(
        id_lang_code['id'], b4_lang, aft_lang, b4_text, result_text
    )

    if result:
        return jsonify({"status": 200, "result":result_text})

    return jsonify({"status": 400,"message": "登録失敗"})

@app.route("/translate_with_option", methods=["POST"])
@cross_origin(supports_credentials=True)
def taranslate_with_option():
    """
    受け取るjson: user_info[]
    {
        token: String,
        text: String,
        to_translate_lang_id
    }
    """

    token_text_and_lang_id = json.loads(request.get_data().decode())
    jwt_auth = JwtAuth()
    id_lang_code = jwt_auth.decode(token_text_and_lang_id['token'])#tokenをデコードしてIDとLang_codeを取り出す
    print(f'userIdと言語コード：{id_lang_code}')

    get_lang_code = GetLanguageCodes()
    lang_code =  get_lang_code.get_one_lang_code(token_text_and_lang_id['to_translate_lang_id'])

    deepl = GetTranslatedWord(lang_code)
    b4_lang, aft_lang, b4_text, result_text = deepl.request_deepl_api(token_text_and_lang_id['text'])
    reg_history = RegistryHistory()

    result = reg_history.insert_data(
        id_lang_code['id'], b4_lang, aft_lang, b4_text, result_text
    )

    if result:
        return jsonify({"status": 200, "result":result_text})

    return jsonify({"status": 400,"message": "登録失敗"})

    pass 


@app.route("/history", methods=["POST"])
@cross_origin(supports_credentials=True)
def history():
    """
    受け取るJSON
    {
        token: String
    }
    """
    token = json.loads(request.get_data().decode())
    jwt_auth = JwtAuth()
    id_and_lang = jwt_auth.decode(token['token'])#tokenをデコードしてIDとLang_codeを取り出す
    rh = RegistryHistory()
    print("user_id: ", id_and_lang['id'])
    data = rh.get_all_history(id_and_lang['id'])
    print(data)
    if data:
        return jsonify({"status":200, "data":data})

    return jsonify({"status":400, "message":"faliure"})

@app.route('/qr_code/<qr_text>')
@cross_origin(supports_credentials=True)
def qr_code(qr_text):
    """
    受け取った文字列でQRコードを作成した後、
    base64に変換してjson形式で送信する
    """
    # 文字列をQRcodeにする
    qr_img = qrcode.make(qr_text)
    qr_img.save('./temp/qr_image.png')

    with open(r"./temp/qr_image.png", 'rb') as f:
        data = f.read()
    encode = base64.b64encode(data).decode('utf-8')

    os.remove('./temp/qr_image.png')
    print(os.listdir('temp'))

    # デコードした画像を確認の為保存する(無くてもいい)
    # with open("qr_check.jpg", "wb") as f:
    #     f.write(base64.b64decode(encode))

    qr_data = {
        # エンコードしたQRコード
        "qr_data":encode,
        "text":qr_text
    }
    return jsonify(qr_data)


if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5000, threaded=True, debug=True)