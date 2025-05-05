from google import genai
# pip install -q -U google-genai
import os
current_dir = os.path.dirname(os.path.abspath(__file__))

with open(current_dir+"/confidencial_information.txt", "r") as file:
    lines = file.readlines()

api_key=lines[0]
client = genai.Client(api_key=api_key)

def get_introduction(loc):
    # 地名の取得
    location_ja=loc['prefecture']+loc['city']+loc['town']
    prompt = f"{location_ja}の観光案内文を1つだけ、読み上げ用に短く自然な日本語で出力してください。前置きや説明、装飾（太字・番号・インデント）は不要です。出力は案内文1文のみ。"

    # 紹介文の生成
    response = client.models.generate_content(
        model="gemini-2.0-flash", contents=prompt
    )
    print(prompt)
    print(response.text)
    return response.text

if __name__ == '__main__':
    loc = {'prefecture': '東京都', 'city': '新宿区', 'town': '歌舞伎町'}
    print(get_introduction(loc))