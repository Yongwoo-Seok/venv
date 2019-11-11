from flask import Flask, render_template, requests
from bs4 import BeautifulSoup
app2 = Flask(__name__)

## URL 별로 함수명이 같거나,
## route('/') 등의 주소가 같으면 안됩니다.

@app2.route('/')
def home():
   return render_template('class_index.html')

@app2.route('/posting')
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

    print(og_image, og_title, og_description)


if __name__ == '__main__':
   app2.run('0.0.0.0',port=5000,debug=True)