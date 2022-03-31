from flask import Flask, flash, render_template, send_from_directory,request,redirect
from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/wad"
mongo = PyMongo(app)

if mongo.db.userHW2.count_documents({"username":'admin'})==0:
    mongo.db.userHW2.insert_one({"username":'admin',"password":generate_password_hash('admin')})


@app.route('/', methods=['GET','POST'])
def home():
    messages=mongo.db.blog.find()
    return render_template("home.html",messages=messages)


@app.route('/authenticate',methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return render_template("authentication.html")
    else:
        username = request.form.get("username")
        password = request.form.get("password")
        user = mongo.db.userHW2.find_one({"username":username})
        if user and check_password_hash(user['password'],password):
          return render_template('profile2.html',username=username,password=password)  
        else:
            return render_template("authentication.html")

@app.route('/signup',methods=["GET", "POST"])
def signup():
    if request.method == "GET":
        return render_template("signUp.html")
    else:
        username = request.form.get("username")
        password = request.form.get("password")
        if mongo.db.userHW2.count_documents({'username':username})!=0:
            flash('This username is not avalaible. Please, choose another one')
            return redirect('/signup')
        else:
            mongo.db.userHW2.insert_one({"username":username,"password":generate_password_hash(password)})
            return redirect('/authenticate')

@app.route('/story',methods=['GET'])
def story():
    if request.method == 'GET':
        posts=list(mongo.db.blog.find())
        for data in posts:
            print(data)
        return render_template('story.html',posts=posts)


@app.route('/profile2',methods=['POST'])
def profile():
    if request.method == 'POST':
        return render_template("profile2.html")

@app.route('/postpage', methods=['POST'])
def postblog():
    if request.method == "POST":
        return render_template('postmessage.html')


@app.route('/postmessage', methods=['POST'])
def postmessage():
    if request.method == "POST":
        message=request.form.get("message")
        datetime=request.form.get("datetime")
        mongo.db.blog.insert_one({"message":message,"datetime":datetime})
        return render_template('home.html')


if __name__ == "__main__":
    app.secret_key="secret"
    app.run(host='localhost', port=5000, debug=True)