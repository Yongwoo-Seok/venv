from flask import Flask, render_template, jsonify, request
app = Flask(__name__)

from pymongo import MongoClient           # pymongo를 임포트 하기(패키지 인스톨 먼저 해야겠죠?)
client = MongoClient('localhost', 27017)  # mongoDB는 27017 포트로 돌아갑니다.
db = client.Sparta_class                  # 'dbsparta'라는 이름의 db를 만듭니다.

## HTML을 주는 부분
@app.route('/')
def home():
   return render_template('index.html')

@app.route('/movie', methods=['GET'])
def movie_info():
    name = request.args.get('name')
    info = db.movies.find_one({'title' : name}, {'_id':0})
    return jsonify({'result': 'success', 'title': info['title'], 'rank' :info['rank'], 'star':info['star']})

@app.route('/movie', methods=['POST'])
def update_movie_rank():
    name = request.form['name']
    star = float(request.form['rank'])
    db.movies.update_one({'name':name},{'$set':{'star': stat}})
    return jsonify({'result': 'success'})

@app.route('/test', methods=['GET'])
def test_get():
   title_receive = request.args.get('title_give')
   print(title_receive)
   return jsonify({'result':'success', 'msg': '이 요청은 GET!'})

if __name__ == '__main__':
   app.run('0.0.0.0',port=5000,debug=True)