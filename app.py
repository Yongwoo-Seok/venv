from flask import Flask, render_template ,jsonify, request
app = Flask(__name__)

from pymongo import MongoClient           # pymongo를 임포트 하기(패키지 인스톨 먼저 해야겠죠?)
client = MongoClient('localhost', 27017)  # mongoDB는 27017 포트로 돌아갑니다.
db = client.Sparta_class                  # 'dbsparta'라는 이름의 db를 만듭니다.

import requests
from bs4 import BeautifulSoup

@app.route('/')
def home():
   return render_template('index.html')

@app.route('/best')
def get_best():
    return 'this is the best'

@app.route('/movie', methods=['GET'])
def movie_info():
    title = request.args.get('title')
    info = db.movies.find_one({'title' : title}, {'_id':0})
    return jsonify({'result': 'success', 'title': info['title'], 'rank' :info['rank'], 'star':info['star']})

@app.route('/movie', methods=['POST'])
def update_movie_rank():
    title = request.form['title']
    star = float(request.form['rank'])
    db.movies.update_one({'title':title},{'$set':{'star': star}})
    return jsonify({'result': 'success'})

@app.route('/review', methods=['POST'])
def update_movie_review():
   ID = request.form['ID']
   title = request.form['title']
   star = float(request.form['star'])
   db.user_reviews.insert_one({ 'User_ID' : ID, 'title': title, 'star' : star})
   moive_info = db.moive_reviews.find_one({'title':title})
   n_reviews = movie_info['n_reviews']
   mean_star = movie_info['star']
   mean_star = (mean_star*n_reviews +star) /(n_reviews+1)
   n_reviews += 1
   db.movie_reviews.update_one({'title':title},{'$set':{'n_reviews': +1 }})
   return jsonify({'result': 'success'})


@app.route('/review', methods=['GET'])
def find_movie_rank():
    rank = int(request.args.get('rank'))
    movies = list(db.movie_reviews.find({}, sort=[{'start',pymongo.DESCENDING}]).limit(rank))
    target_movie = movies[-1]
    return jsonify({'result': 'success', 'name' : target_movie['name'], 'rank':rank , 'star':target_movie['star']})

@app.route('/posting', methods=['POST'])
def posting():
    url = request.form['url_give']
    comment = request.form['comment_give']
    author = request.form['author_give']

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    data = requests.get(url, headers=headers)
    soup = BeautifulSoup(data.text, 'html.parser')

    og_image = soup.select_one('meta[property="og:image"]')
    og_title = soup.select_one('meta[property="og:title"]')
    og_description = soup.select_one('meta[property="og:description"]')

    image = og_image['content']
    title = og_title['content']
    description = og_description['content']

    article = {'url' : url , 'comment': comment , 'author' : author , 'image' : image , 'title' : title , 'desc' : description }
    db.articles.insert_one(article)
    return jsonify({'result': 'success'})


@app.route('/posting', methods=['GET'])
def listing():
    author = request.args.get('author_give')
    articles = list(db.articles.find({'author':author},{'_id':0}))
    return jsonify({'result':'success', 'articles':articles})


#여기서부터 숙제입니다.
#주문 넣기 부분!
@app.route('/shop', methods=['POST'])
def buying():
    name = request.form['name_give']
    count = request.form['count_give']
    address = request.form['address_give']
    phone = request.form['phone_give']
    item = request.form['item_give']
    order_list = {'name' : name , 'count': count , 'address' : address , 'phone' : phone , 'item' : item }
    db.orders.insert_one(order_list)
    return jsonify({'result': 'success'})

#주문 넣은거 보는 부분!
@app.route('/shop', methods=['GET'])
def showing():
    item = request.args.get('item_give')
    orders = list(db.orders.find({'item' : item},{'_id':0}))
    return jsonify({'result':'success', 'orders':orders})

if __name__ == '__main__':
   app.run('0.0.0.0',port=5000,debug=True)