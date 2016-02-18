from flask import Flask, request, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_migrate import Migrate

app = Flask(__name__)
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./test.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:kwang2143@localhost/kwanghyunpark'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)
admin = Admin(app)
migrate = Migrate(app, db)


@app.route('/')
def hello():
    return "Hello World! Demacia!"

@app.route("/hello/")
@app.route("/hello/<to>")
def hellodouble(to="basic"):
    return "Hello %s" % (to,)

@app.route("/calc/<a>/<b>")
def calc(a,b):
    return "Answer is %d" % (int(a)+int(b),)

@app.route("/test", methods= ["GET", "POST"])
def testfunc():
    print((request.args, request.form))
    return "%s World" % (request.method,)

@app.route("/test_html/")
@app.route("/test_html/<to>")
def testhtml(to="initialized answer"):
    return render_template("index.html", test=to)

class Person(object):
    def __init__(self, name, age, job):
        self.name = name
        self.age = age
        self.job = job

@app.route("/objecttest/<ins>")
def objecttest(ins = "", age = 21, job = "선생님"):
    love = Person(ins, age, job)
    return str (love.name, love.age, love.job)

testlist = []               #리스트를 만든다!
testlist.append(1)          #리스트에 푸쉬하는것!

class DBtest(db.Model):
    __tablename__="DBtest"
    id = db.Column(db.Integer, primary_key = True)
    user = db.Column(db.String(10))#, primary_key = True)
    name = db.Column(db.String(10))#, unique = True)  #고유값을 지정하는데 고유한 값이 
    age = db.Column(db.Integer)                     #아니라면 DB에 추가가 안된다

admin.add_view(ModelView(DBtest, db.session))

'''
kwang = DBtest()
kwang.user = "박광현"
kwang.name = "광현박"
kwang.age = 26
db.session.add(kwang)
db.session.commit()
'''

#testlist.append(kwang)

@app.route("/dbtest/<user>/<name>/<age>")           #$rm test.db
def dbwrite (user, name, age):                      #$python
    kwang2 = DBtest()                               #>>>import test from db
    kwang2.user = user                              #>>>db.create_all()
    kwang2.name = name                              #>>>exit()
    kwang2.age = age
    db.session.add(kwang2)
    db.session.commit()
    return "회원가입 끝!"

@app.route("/login/<user>/<pwd>")
def LogIn(user, pwd):
    found = DBtest.query.filter(DBtest.user == user, DBtest.age == pwd).first()
    if found:
        return "안녕핫요  %s님 :)" % (found.name)
    else:
        return "누구세요"

@app.route("/json")
def JSON():
    a = {
            "dinner" : "Hungry",
            "광현" : "학생 ",
            "민호" : "선생님 ",
            "kwangkwang" : "student"
            }
    return jsonify(a)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
