from flask import Flask,jsonify,request             #pip install flask
from flask_cors import CORS                         #pip install flask-cors
from flask_pymongo import PyMongo                   #pip install flask-pymongo
#pip install flask-jwt-extended
from dotenv import load_dotenv
import os

app = Flask(__name__)
CORS(app)

load_dotenv()

uri = os.getenv("uri")


#Mongo Connection
app.config["MONGO_URI"] = uri
mongo = PyMongo(app)

try:
    mongo.cx.admin.command('ping')  # Pinging MongoDB to check the connection
    print("Successfully connected to MongoDB")
except:
    print("Failed to connect to MongoDB")



#User Signup - Store plain text password in DB :: For Employees
@app.route("/SignUpEmployee", methods=["POST"])
def SignUpEmployee():
    try:
        '''
        Sample Request:
        {
            "email": "johndoe@gmail.com",
            "password": "johndoe"
        }
        '''
        data = request.json
        email = data["email"]
        password = data["password"]  

        # Check if user already exists
        existing_user = mongo.db.users.find_one({"email": email})
        if existing_user:
            return jsonify({"error": "User already exists"}), 400

        # Insert user into the database
        mongo.db.users.insert_one({"email": email, "password": password})

        return jsonify({"message": "User registered successfully"}), 201

    except Exception as e:
        return jsonify({"error": f"Signup failed: {str(e)}"}), 500
    
# User Login - Plain Text Password Verification :: For Employees
@app.route("/LoginEmployee", methods=["POST"])
def LoginEmployee():
    try:
        '''
        sample request:
        {
            "email": "johndoe@gmail.com",
            "password": "johndoe"
        }

        '''
        data = request.json
        email = data["email"]
        password = data["password"]

        # Find user by email
        user = mongo.db.users.find_one({"email": email})

        if not user or user["password"] != password:
            return jsonify({"error": "Invalid email or password"}), 401

        return jsonify({"message": "Login successful", "email": email}), 200

    except KeyError:
        return jsonify({"error": "Missing email or password in request"}), 400

    except Exception as e:
        return jsonify({"error": f"Login failed: {str(e)}"}), 500
    








'''
Below is the code for the user signup and confirmation for the clients.
The password is stored in plain text in the database.
'''

    
#User Signup - Store plain text password in DB :: For Clients
@app.route("/SignUpClient", methods=["POST"])
def SignUpClient():

    '''
    Sample Request:
    {
        "username": "Jane Doe",
        "DOB": "1990-01-01",
        "policy_number": "12345678",
        "email": "janedoe@gmail.com",
        "password": "janedoe"
    }
    '''
    try:
        data = request.json
        username = data["username"]
        dob = data["DOB"]
        policy_number = data["policy"]
        email = data["email"]
        password = data["password"]

        # Check if policy number exists
        existing_policy = mongo.db.clients.find_one({"policy_number": policy_number})
        if existing_policy:
            return jsonify({"error": "Policy number already exists"}), 400

        # Check if a user with the same username, email, and DOB exists
        existing_user = mongo.db.clients.find_one({"username": username, "email": email, "dob": dob})
        if existing_user:
            return jsonify({"error": "User with this username, email, and DOB already exists"}), 400

        # Insert user into the database
        mongo.db.clients.insert_one({
            "username": username,
            "dob": dob,
            "policy_number": policy_number,
            "email": email,
            "password": password
        })

        return jsonify({"message": "User registered successfully"}), 201

    except Exception as e:
        return jsonify({"error": f"Signup failed: {str(e)}"}), 500
    
# Confirms User Exist - DOB and Policy Number or - Email DOB Username
'''
Add different options for user to confirm their idenity :: This is just a base line functionality
This is the normal user confirmation process
'''
@app.route("/confirmUser", methods=["POST"])
def confirmUser():
    try:
        data = request.json
        dob = data["DOB"]
        policy_number = str(data["policy_number"]) 
        email = data["email"]

        # Check if user exists
        existing_user = mongo.db.clients.find_one({
            "email": email,
            "dob": dob,
            "policy_number": policy_number  # Ensure key matches DB
        })

        if existing_user:
            print(f"User Found: {existing_user}")  
            return jsonify({"message": "User exists"}), 200

        print("User Not Found")  
        return jsonify({"error": "User does not exist"}), 404

    except Exception as e:
        return jsonify({"error": f"User confirmation failed: {str(e)}"}), 500









# GET Method to Access User Information - No Authentication Required -- Place Holder to withdraw user information
'''
@app.route("/profile/<email>", methods=["GET"])
def profile(email):
    try:
        user = mongo.db.users.find_one({"email": email}, {"_id": 0, "password": 0})  # Exclude password

        if user:
            return jsonify({"message": "User Profile Data", "data": user}), 200
        else:
            return jsonify({"error": "User not found"}), 404

    except Exception as e:
        return jsonify({"error": f"Profile retrieval failed: {str(e)}"}), 500

'''

if __name__ == "__main__":
    app.run(port=5000, debug=True)
    


'''
Run Server:
flask --app app run
flask --app app run --port=5000 --debug5

Python main.py
Python3 main.py 

'''