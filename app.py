from flask import Flask, request, jsonify,redirect
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from datetime import datetime

from databse import db, User,ParkingLot,ParkingSpot,Reserve

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
@app.route("/login", methods=["POST","GET","OPTIONS"])

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
             "redirect": f"/user/{user.id}"   
        })

    return jsonify({"error": "Invalid username or password"}), 401
@app.route("/get_user/<int:user_id>")
def get_user(user_id):
    user = User.query.get(user_id)
    if user:
        return jsonify({
            "id": user.id,
            "name": user.username,
            "type": user.type
        })
    return jsonify({"error": "User not found"}), 404
@app.route("/parkinglot", methods=["POST"])
def parkinglot():
    data = request.json
    if ParkingLot.query.filter_by(name=data["name"]).first():
        return jsonify({"error": "Parking Lot already exists"}), 400

    if data.get("spots", 0) <= 0:
        return jsonify({"error": "There must be at least one spot"}), 400

    user = ParkingLot(
        name=data["name"],
        price=data["price"],
        address=data.get("address", ""),
        pincode=data["pincode"],
        spots=data["spots"]
    )

    db.session.add(user)
    db.session.commit()

  
    for i in range(1, data["spots"] + 1):
        spot = ParkingSpot(
            spot_number=i,
            status='F', 
            parking_lot_id=user.id
        )
        db.session.add(spot)

    db.session.commit()

    return jsonify({"message": "Parking lot added successfully with spots"}), 201

@app.route("/get_parkinglots", methods=["GET"])
def get_parkinglots():
    parkinglots = ParkingLot.query.all()
    result = []
    for lot in parkinglots:
        result.append({
            "id": lot.id,
            "name": lot.name,
            "price": lot.price,
            "address": lot.address,
            "pincode": lot.pincode,
            "spots": lot.spots
        })
    return jsonify(result)
@app.route('/parkinglot/<int:id>', methods=['PUT'])
def update_parking_lot(id):
    data = request.json
    lot = ParkingLot.query.get_or_404(id)

    
    lot.name = data['name']
    lot.price = data['price']
    lot.address = data['address']
    lot.pincode = data['pincode']


    new_spot_count = data['spots']
    current_spots = ParkingSpot.query.filter_by(parking_lot_id=lot.id).order_by(ParkingSpot.spot_number).all()
    current_count = len(current_spots)

    if new_spot_count > current_count:
        
        for i in range(current_count + 1, new_spot_count + 1):
            new_spot = ParkingSpot(
                spot_number=i,
                status='F', 
                parking_lot_id=lot.id
            )
            db.session.add(new_spot)

    elif new_spot_count < current_count:
       
        to_delete = current_spots[new_spot_count:]
        for spot in to_delete:
            has_reservations = Reserve.query.filter_by(parking_spot_id=spot.id).first()
            if has_reservations:
                return jsonify({'error': f"Cannot delete spot {spot.spot_number}, it has reservations."}), 400
            db.session.delete(spot)

    lot.spots = new_spot_count
    db.session.commit()

    return jsonify({'message': 'Updated successfully'})

    

@app.route('/edit_user/<int:id>', methods=['PUT'])
def edit_user(id):
    data = request.json
    lot = User.query.get_or_404(id)
    lot.name = data['name']
    lot.phonenumber = data['phonenumber']
    lot.address = data['address']
   
    db.session.commit()
    return jsonify({'message': 'Updated successfully'})




@app.route('/get_enrolled_users', methods=['GET'])
def get_enrolled_users():
    users = User.query.filter(User.username != "admin").all()
    user_list = []

    for user in users:
        user_list.append({
            'id': user.id,
            'name': user.name,
            'username': user.username,
            'address': user.address,
            'phonenumber': user.phonenumber,
            'type': user.type
        })

    return jsonify(user_list)
@app.route("/parkinglot/<int:lot_id>/spots", methods=["GET"])
def get_spots_for_lot(lot_id):
   
    lot = ParkingLot.query.get_or_404(lot_id)

   
    spots = ParkingSpot.query.filter_by(parking_lot_id=lot_id).all()

    spots_data = [
        {
            "id": spot.id,
            "spot_number": spot.spot_number,
            "status": spot.status
        } for spot in spots
    ]

    
    lot_data = {
        "id": lot.id,
        "name": lot.name,
        "spots": spots_data
    }

    return jsonify({"lot": lot_data})





@app.route("/spot/<int:spot_id>", methods=["PUT"])
def update_spot_status(spot_id):
    data = request.json
    spot = ParkingSpot.query.get_or_404(spot_id)

    if data.get("status") not in ["F", "R"]:
        return jsonify({"error": "Invalid status"}), 400

    spot.status = data["status"]
    db.session.commit()
    return jsonify({"message": "Spot status updated"})
@app.route('/search_parking_spots', methods=['GET'])
def search_parking_spots():
    query = request.args.get('q', '').strip()

    if not query:
        return jsonify([])

    
    try:
        query_int = int(query)
    except ValueError:
        query_int = None

    results = db.session.query(ParkingSpot).join(ParkingLot).filter(
        (ParkingLot.name.ilike(f"%{query}%")) |
        (ParkingLot.address.ilike(f"%{query}%")) |
        (ParkingLot.pincode == query_int) |
        (ParkingLot.price == query_int) |
        (ParkingLot.spots == query_int)
    ).all()

    return jsonify([
        {

            'parking_lot': {
                'id': spot.parking_lot.id,
                'name': spot.parking_lot.name,
                'address': spot.parking_lot.address,
                'pincode': spot.parking_lot.pincode,
                'price': spot.parking_lot.price,
                'spots': spot.parking_lot.spots
            }
        }
        for spot in results
    ])


@app.route('/parkinglot/search')
def parkinglot_search():
    q = request.args.get('q', '').strip()
    if not q:
        return jsonify([])

    
    filters = []
    if q.isdigit():
        filters = (ParkingLot.name.ilike(f'%{q}%')) | (ParkingLot.pincode == int(q))
    else:
        filters = ParkingLot.name.ilike(f'%{q}%')

    results = ParkingLot.query.filter(filters).all()

    return jsonify([
        {
            'id': p.id,
            'name': p.name,
            'price': p.price,
            'address': p.address,
            'pincode': p.pincode,
            'spots': p.spots
        } for p in results
    ])





if __name__ == "__main__":
    app.run(debug=True)
