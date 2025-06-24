from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from datetime import datetime

from databse import db, User,ParkingLot,ParkingSpot

app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///D:/vt/database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)  
bcrypt = Bcrypt(app)
CORS(app)

with app.app_context():
    db.create_all()

@app.route("/register", methods=["POST"])
def register():
    data = request.json
    if User.query.filter_by(username=data["username"]).first():
        return jsonify({"error": "Username already exists"}), 400

    hashed_password = bcrypt.generate_password_hash(data["password"]).decode('utf-8')

    user = User(
        name=data["name"],
        username=data["username"],
        password=hashed_password,
        type=data["type"],
        address=data.get("address", ""),
        phonenumber=data["phonenumber"]
    )

    db.session.add(user)
    db.session.commit()
    return jsonify({"message": "User registered successfully"}), 201

@app.route("/login", methods=["POST", "OPTIONS"])
def login():
    if request.method == "OPTIONS":
        return '', 204 

    data = request.get_json(force=True)  

    if data["username"] == "admin" and data["password"] == "123":
        return jsonify({
            "message": "Login successful",
            "type": "admin",
            "redirect": "/admin"
        })

    user = User.query.filter_by(username=data["username"]).first()

    if user and bcrypt.check_password_hash(user.password, data["password"]):
        return jsonify({
            "message": "Login successful",
            "type": user.type,
            "redirect": "/user"  
        })

    return jsonify({"error": "Invalid username or password"}), 401




if __name__ == "__main__":
    app.run(debug=True)
