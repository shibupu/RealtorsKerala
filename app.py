import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from flask import Flask, render_template, request
from flaskext.mysql import MySQL
from config import (db, cities, urls)

app = Flask(__name__)

mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = db['user']
app.config['MYSQL_DATABASE_PASSWORD'] = db['pass']
app.config['MYSQL_DATABASE_DB'] = db['name']
app.config['MYSQL_DATABASE_HOST'] = db['host']
mysql.init_app(app)


@app.route("/")
def index():
    return render_template('index.html')


@app.route('/city/', methods=['GET'])
@app.route('/city/<city>/', methods=['GET'])
def list(city=None):
    sql = "select source, title, type, summary, locality, price, time, link, contact_name, contact_number from ad where date(added_date) = curdate()"
    if bool(city) is True:
        sql += " and city = '" + city + "'"
    else:
        city = 'All'
    sql += " order by added_date desc limit 10"

    cursor = mysql.connect().cursor()
    cursor.execute(sql)
    ads = cursor.fetchall()

    return render_template('list.html', city=city, cities=cities, ads=ads, urls=urls)


@app.route('/search/', methods=['GET', 'POST'])
def search():
    params = request.values
    keyword = params.get('keyword', '').strip()
    location = params.get('location', '').strip()

    warning = ''
    if bool(keyword) is False:
        warning = 'Please enter keyword'

    sql = "select source, title, type, summary, locality, price, time, link, contact_name, contact_number from ad where (title like '%" + keyword + "%' or summary like '%" + keyword + "%')"
    if bool(location):
        sql += " and (city like '%" + location + "%' or locality like '%" + location + "%')"
    sql += " order by added_date desc"

    cursor = mysql.connect().cursor()
    cursor.execute(sql)
    ads = cursor.fetchall()

    return render_template('list.html', city='Result', cities=cities, ads=ads, urls=urls, keyword=keyword, location=location, warning=warning)

if __name__ == "__main__":
    app.debug = True
    app.run(host="0.0.0.0")
