from flask import Flask, render_template, request

import requests

app = Flask(__name__)

@app.route('/')
def main():
    name = 'sparta'
    r = requests.get('http://openapi.seoul.go.kr:8088/6d4d776b466c656533356a4b4b5872/json/RealtimeCityAir/1/99')
    response = r.json()
    rows = response['RealtimeCityAir']['row']
    return render_template("test2.html", name=name, rows= rows)

@app.route('/detail/<keyword>')
def detail(keyword):
    # 원래는 detail() 였음.
    # 브라우저에서 도메인 부분에 ? 으로 parameter 을 넘겨주고 word_give=hello 를 붙여준다.
    # word 값을 그대로 가지고 와보자
    # 이번에는 URL 안에 있는 <keyword> 값을 가지고 와보자
    #word_receive = request.args.get("word_give")
    return render_template("test1.html", word=keyword)
'''
파이썬으로 Owlbot 에 API 요청 보내기
r = requests.get("https://owlbot.info/api/v4/dictionary/owl", headers={"Authorization": "Token cf2d1479a4a52e822922b9e7f1a5d1eed86e84e9"})
result = r.json()
print(result)
'''

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)