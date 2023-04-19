from flask import Flask, request, jsonify,render_template,redirect
import uuid
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config ['SQLALCHEMY_DATABASE_URI'] = "sqlite:///jupy.db"
app.config ['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db=SQLAlchemy(app)

class Project(db.Model):
    # sno=db.Column(db.Integer,primary_key=True)

    email = db.Column(db.String(100),primary_key=True)
    password = db.Column(db.String(100),nullable=False)
    key = db.Column(db.String(100),nullable=False)  
    
    def __repr__(self) -> str:
        return f"{self.key}-{self.email}--{self.password}"

with app.app_context():
    db.create_all()

@app.route('/',methods = ["GET"])
def api():
    return render_template("index.html")

# Define a dictionary of valid API keys
valid_api_keys = {}

#method to generate an api key
@app.route('/a',methods = ["GET","POST"])
def apikeygen():
  
    #generate an api key
    api_key = str(uuid.uuid4())

    email = request.form["email"]
    
    user = Project.query.filter_by(email = email).first()
    if user is not None:
        return render_template("message.html")
    else:
        
        email = request.form["email"]
        password = request.form["password"]

        key = api_key
        todo = Project(email = email,password=password,key = key)
        db.session.add(todo)
        db.session.commit()

    #store the api key in dict
    valid_api_keys['api_key'] = api_key
    print(valid_api_keys,"valid_api_keys")
    response_data = {
        'api_key' : api_key
    }
   
    #return a json response
    return render_template('test.html',response_data = response_data )

#method to use an api key to authorize
@app.route('/api/data',methods=["GET"])
def authorize():

    return redirect("/")

    args = request.args
    path = args.get("api_key")
    #get the api_key from request headers    
    print(path)
    #check if the api_key is valid,so return the valid response
    #check if the api key is valid
    if path in valid_api_keys.values():
        data = {
            "message" : "Your api key is correct"
        }

        return jsonify(data),200
    else:
        error_message ={
            "message": "not valid"
        }

        return error_message,400

if __name__ == "__main__":
    app.run(debug=True)