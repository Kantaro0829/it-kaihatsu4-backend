#from _typeshed import Self
from typing_extensions import Self
from sqlalchemy.engine import engine_from_config
from sqlalchemy.orm.scoping import scoped_session
from sqlalchemy.sql.expression import false, true
from sqlalchemy.sql.functions import user
from sqlalchemy import desc, asc
from setting import session# セッション変数の取得
from db_model import User, Languages, History
import hashlib#ハッシュ化用
from datetime import date
#import datetime

class UserRegistry():

    def __init__(self, user_info):
        self.password = hashlib.sha256(user_info['password'].encode()).hexdigest()
        self.mail = user_info["email"]
        self.lang_id = user_info["lang_id"]
        self.dic = {}

    def new_user_reg(self):
        user = User()
        language = Languages()
        user.mail = self.mail
        user.lang_id = self.lang_id
        user.password = self.password
        dic = {}

        session.add(user)#データ登録
        session.flush()
        session.commit()#コミット

        #自動で生成されたID
        id = user.id
        lang_id = user.lang_id
        session.close

        lang_code = session.query(Languages.lang_code).\
                            filter(Languages.lang_id == lang_id).\
                                one()

        self.dic = {"id": id, "lang_code": lang_code[0]}
        print(f"new_user_reg: {self.dic}")
        return self.dic
    
    def update_user(self):
        pass

class UserLogin():
    def __init__(self, user_info):
        self.password = hashlib.sha256(user_info['password'].encode()).hexdigest()
        self.mail = user_info['email']
        self.dic = {}
    
    def login(self):
        user = User()
        language = Languages()

        #このメールアドレスのパスワードを抽出
        auth_pass = session.query(User.password).\
            filter(User.mail == self.mail).\
                one()

        print(auth_pass[0], "は", self.mail, "のパスワード！！")

        #パスワード比較
        if self.password == auth_pass[0]:
            
            #return tuple (user_id, lang_id)
            id, lang_id = session.query(User.id, User.lang_id).\
                    filter(User.mail == self.mail).\
                        one()
            
            print(f'id: {id}, lang_id: {lang_id}')

            lang_code = session.query(Languages.lang_code).\
                            filter(Languages.lang_id == lang_id).\
                                one()
            
            print(f'lang_code: {lang_code}')


            self.dic = {"id": id, "lang_code": lang_code[0]}

            session.close
            print(f"login: {self.dic}")
            return self.dic
        
        else:
            self.dic = {"id": 0}
            return self.dic

class GetLanguageCodes():

    def get_all_lang_code(self):
        language = Languages()
        #order_by(desc(User.created_at))
        all_code = session.query(Languages.lang_id, Languages.lang_name).\
                                    order_by(asc(Languages.lang_id)).\
                                        all()
        print(type(all_code))
        print(all_code)
        data_list = []
        for i in all_code:
            temp_dic = {}
            lang_id, lang_name = i
            temp_dic['lang_id'] = lang_id
            temp_dic['lang_name'] = lang_name
            data_list.append(temp_dic)
        
        print(data_list)
        return data_list
    
    def get_one_lang_code(self, lang_id):
        language = Languages()
        lang_code = session.query(Languages.lang_code).\
                                    filter(Languages.lang_id == lang_id).\
                                        one()
        print(lang_code[0])
        return lang_code[0]

class RegistryHistory():
    
    def insert_data(self, user_id, b4_lang_code, aft_lang_code, b4_trans, aft_trans):
        """
        data = {
            user_id:Int, 
            before_translation:String, 
            after_translation:String, 
            before_lang_code:String, 
            after_lang_code:String, 
            #recoded_date:date
        }
        """
        today = date.today()
        print(f'今日の日付確認用ログ：{today}')

        history = History()
        history.user_id = user_id
        history.before_translation = b4_trans
        history.after_translation = aft_trans
        history.before_lang_code = b4_lang_code
        history.after_lang_code = aft_lang_code
        history.recoded_date = today

        session.add(history)#データ登録
        session.flush()
        session.commit()#コミット

        log_data = {
            "user_id":history.user_id,
            "b4_trans": history.before_translation,
            "aft_trans": history.after_translation,
            "b4_lang_code": history.before_lang_code,
            "aft_lang_code": history.after_lang_code,
            "today": history.recoded_date
        }

        print(f'登録された値：{log_data}')

        if history.user_id == user_id:
            print(f'LOG: 登録された')
            session.close()
            return true
        
        session.close
        return false
    
    def get_all_history(self, user_id):
        history = History()
        
        #History Table 全件取得
        all_history = session.query(History).\
            filter(History.user_id == user_id).\
                all()
        
        history_array = []
        for i in all_history:
            temp_dic = {}
            temp_dic["data_id"] = i.data_id
            temp_dic["user_id"] = i.user_id
            temp_dic["before_translation"] = i.before_translation
            temp_dic["after_translation"] = i.after_translation
            temp_dic["before_lang_code"] = i.before_lang_code
            temp_dic["after_lang_code"] = i.after_lang_code
            temp_dic["recoded_date"] = i.recoded_date

            history_array.append(temp_dic)

            print(i.data_id)
            print(i.user_id)
            print(i.before_translation)
            print(i.after_translation)
            print(i.before_lang_code)
            print(i.after_lang_code)
            print(i.recoded_date)

        
        return history_array
        
        
