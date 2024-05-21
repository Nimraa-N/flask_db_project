from flask import Flask,jsonify,request,render_template,session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='postgresql://postgres:root@localhost/friends_db'
db=SQLAlchemy(app)
app.secret_key='secret_key'

class Friend(db.Model):
    name = db.Column(db.String(100), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    contact = db.Column(db.String(100), unique=True, primary_key=True)

with app.app_context():
     db.create_all()

@app.route("/records")
def get_records():
     friends=Friend.query.all()
     friend_list = [{'name':friend.name, 'city':friend.city,'contact':friend.contact} for friend in friends]
     return jsonify({'friends':friend_list})


data =[
    {"name":"Nimra","city":"peshawar","contact":+9231234566},
    {"name":"wajeeha","city":"peshawar","contact":+9231234567},
    {"name":"sana","city":"peshawar","contact":+9231234568},
    {"name":"bushra","city":"peshawar","contact":+9231234569},


]

@app.route("/")
def home():
    return "<h1> we  are making Api home page</h1>"

@app.route("/api_response")
def response():
    return jsonify(data)



@app.route("/record", methods=["GET", "POST"])
def add_record():
        # if request.method == "POST":
        #     data_recv = request.get_json()
        #     record = {'name': data_recv['name'], 'city': data_recv['city'], 'contact': data_recv['contact']}
        #     data.append(record)
        #     return "Record Added successfully"
        # else:
        #     return "This endpoint only supports POST requests."
        if request.method =="POST":
             record = {'name':request.form['name'], 'city':request.form['city'],'contact':request.form['contact']}
             data.append(record)
             return "Record Added successfully"
        else:
             return render_template('response.html')
        
@app.route("/db_record", methods=["GET", "POST"])
def add_db_record():
            if request.method=='POST':
                data = request.get_json()
                new_friend =Friend(name=data['name'],city=data['city'],contact=data['contact']) 
                db.session.add(new_friend)
                db.session.commit()
                return jsonify({'msg':'Friend Added'})
            else:
                 return "please add new friend via postman in json format"
            
       
        
        
    

if __name__ == "__main__":
    app.run(debug=True)


