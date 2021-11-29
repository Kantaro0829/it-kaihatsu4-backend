import requests

class GetTranslatedWord():
    def __init__(self, mother_tongue):
        self.api_key = "18fb2c69-6d08-6178-46ae-33b218317838:fx"
        self.mother_tongue = mother_tongue
    
    def request_deepl_api(self, text):
        #URLクエリに仕込むパラメータの辞書
        params = {
            "auth_key": self.api_key,
            "text": text,
            #"source_lang": 'EN', # 入力テキストの言語を英語に設定
            "target_lang": self.mother_tongue #'JA'  # 出力テキストの言語を日本語に設定（JPではなくJAなので注意）
        }

        request = requests.post("https://api-free.deepl.com/v2/translate", data=params)
        result = request.json()

        print(f'{text}:{result}')
        """
        need 

        'detected_source_language', 'self.mother_tongue', 
        'text', 'result["translations"][0]["text"]'
        
        for using thease data to insert to history table
        """
        return result["translations"][0]["text"]

"""
{'translations': [{'detected_source_language': 'ZH', 'text': 'ありがとうございました。'}]}
"""

# #apiキー
# api_key = "18fb2c69-6d08-6178-46ae-33b218317838:fx"
# #翻訳したい文章、単語
# text = "謝謝"#"I played baseball"

# #URLクエリに仕込むパラメータの辞書
# params = {
#     "auth_key": api_key,
#     "text": text,
#     #"source_lang": 'EN', # 入力テキストの言語を英語に設定
#     "target_lang": 'JA'  # 出力テキストの言語を日本語に設定（JPではなくJAなので注意）
# }

# request = requests.post("https://api-free.deepl.com/v2/translate", data=params)
# result = request.json()

# print(f'{text}:{result}')