from flask import Flask, request, render_template
app = Flask(__name__)

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
    return print (love.name, love.age, love.job)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
