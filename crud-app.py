from flask import Flask, json, request
from flaskext.mysql import MySQL

app = Flask(__name__)
mysql = MySQL()

users = list(range(100))

# mysql configuratoin
app.config['MYSQL_DATABASE_HOST']       = 'localhost'
app.config['MYSQL_DATABASE_USER']       = 'root'
app.config['MYSQL_DATABASE_PASSWORD']   = 'root'
app.config['MYSQL_DATABASE_DB']         = 'UserList'
mysql.init_app(app)

@app.route('/list')
def show():
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tbl_user")
    data = cursor.fetchall()
    dataList = []
    if data is not None:
        for item in data:
            dataTempObj = {
                'id'        : item[0],
                'username'  : item[1],
                'password'  : item[2],
                'fullname'  : item[3],
                'city'      : item[4],
                'status'    : item[5]
            }
            dataList.append(dataTempObj)
        return json.dumps(dataList)
    else:
        return 'data kosong'

@app.route('/update/<id>',methods=['POST'])
def update(id):
    conn = mysql.connect()
    cursor = conn.cursor()
    result = cursor.execute("UPDATE tbl_user SET username = %s, password = %s, fullname = %s, city = %s, status = %s WHERE user_id = %s",(request.form['username'],request.form['password'],request.form['fullname'],request.form['city'],request.form['status'],int(id)))
    conn.commit()
    conn.close()
    if(result):
        return json.dumps({'updated':'true'})
    else:
        return json.dumps({'updated':'false'})

@app.route('/delete/<id>')
def delete(id):
    conn = mysql.connect()
    cursor = conn.cursor()
    result = cursor.execute("DELETE FROM tbl_user WHERE user_id = %s",int(id))
    conn.commit()
    conn.close()
    if(result):
        return json.dumps({'delete':'true'})
    else:
        return json.dumps({'delete':'false'})

@app.route('/insert/<id>',methods=['POST'])
def insert(id):
    conn = mysql.connect()
    cursor = conn.cursor()
    result = cursor.execute("INSERT INTO tbl_user VALUES (%s,%s, %s, %s, %s,%s)",(int(id),request.form['username'],request.form['password'],request.form['fullname'],request.form['city'],request.form['status']))
    conn.commit()
    conn.close()
    if(result):
        return json.dumps({'inserted':'true'})
    else:
        return json.dumps({'inserted':'false'})

@app.route('/search/username/<username>', methods=['GET'])
def searchUsername(username):
    likeString = username + "%"
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("""SELECT * FROM tbl_user WHERE username LIKE %s;""",(likeString))
    data = cursor.fetchall()
    dataList = []
    if data is not None:
        for item in data:
            dataTempObj = {
                'id'        : item[0],
                'username'  : item[1],
                'password'  : item[2],
                'fullname'  : item[3],
                'city'      : item[4],
                'status'    : item[5]
            }
            dataList.append(dataTempObj)
        return json.dumps(dataList)
    else:
        return 'data kosong'

@app.route('/user', defaults={'page':0})
@app.route('/user/page/<page>')
def userpaginate(page):
    perpage=20
    if page == 0:
        startat=int(page)*perpage
    else:
        startat=perpage*(int(page)-1)
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM tbl_user limit %s, %s;', (startat,perpage))    
    data = cursor.fetchall()
    print(data)
    dataList = []
    if data is not None:
        for item in data:
            dataTempObj = {
                'id'        : item[0],
                'username'  : item[1],
                'password'  : item[2],
                'fullname'  : item[3],
                'city'      : item[4],
                'status'    : item[5]
            }
            dataList.append(dataTempObj)
        return json.dumps(dataList)
    else:
        return 'data kosong'

if __name__ == '__main__':
    app.run(debug=True)
