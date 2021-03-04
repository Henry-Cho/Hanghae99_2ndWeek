from flask import Flask, render_template, request, jsonify, redirect, url_for
from pymongo import MongoClient
import requests
from datetime import datetime

app = Flask(__name__)

client = MongoClient('3.36.99.44', 27017, username="test", password="test")
db = client.dbsparta_plus_week2


@app.route('/')
def main():
    # DB에서 저장된 단어 찾아서 HTML에 나타내기
    words = list(db.words.find({}, {"_id": False}))
    msg = request.args.get("msg")
    return render_template("index.html", words=words, msg=msg)


@app.route('/detail/<keyword>')
def detail(keyword):
    status_receive = request.args.get("status_give")
    # API에서 단어 뜻 찾아서 결과 보내기
    r = requests.get(f"https://owlbot.info/api/v4/dictionary/{keyword}", headers={"Authorization": "Token cf2d1479a4a52e822922b9e7f1a5d1eed86e84e9"})
    if r.status_code != 200:
        return redirect(url_for("main", msg="단어가 이상하다.."))
    result = r.json()
    print(result)

    return render_template("detail.html", word=keyword, result=result, status = status_receive)


@app.route('/api/save_word', methods=['POST'])
def save_word():
    # 단어 저장하기
    word_receive = request.form["word_give"]
    definition_receive = request.form["definition_give"]
    doc = {
        "word": word_receive,
        "definition": definition_receive
    }

    db.words.insert_one(doc)

    #print(doc)

    return jsonify({'result': 'success', 'msg': f'{word_receive} 저장'})


@app.route('/api/delete_word', methods=['POST'])
def delete_word():
    # 단어 삭제하기
    word_receive = request.form["word_give"]
    db.words.delete_one({"word": word_receive})
    return jsonify({'result': 'success', 'msg': f'{word_receive} 삭제'})

@app.route('/api/get_exs', methods=['GET'])
def get_exs():
    # 예문 가져오기
    all_examples = list(db.examples.find({}, {"_id": False}))
    return jsonify({'all_examples': all_examples})

@app.route('/api/save_ex', methods=['POST'])
def save_ex():
    # 예문 저장하기
    ex_receive = request.form['ex_give']
    word_receive = request.form['word_give']
    today = datetime.now()
    ex_id = f'{today} {word_receive}'
    print(today)
    #example_id = f"{word_receive} {0}"
    dic = {
        "ex_id": ex_id,
        "example": ex_receive,
        "word": word_receive
    }
    db.examples.insert_one(dic)
    return jsonify({'result': f'{ex_receive} 저장 완료'})


@app.route('/api/delete_ex', methods=['POST'])
def delete_ex():
    # 예문 삭제하기

    word_receive = request.form['word_give']
    id_receive = request.form['id_give']
    db.examples.delete_one({'ex_id': id_receive})

    return jsonify({'result': f'{word_receive} 가 삭제 되었습니다.'})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)