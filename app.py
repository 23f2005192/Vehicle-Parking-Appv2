from flask import Flask, request, jsonify,redirect
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from datetime import datetime
from sqlalchemy import func

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

@app.route('/parkinglot/search')
def parkinglot_search():
    q = request.args.get('q', '').strip()
    if not q:
        return jsonify([])

    
    if q.isdigit():
        filters = (ParkingLot.name.ilike(f'%{q}%')) | (ParkingLot.pincode == int(q))
    else:
        filters = ParkingLot.name.ilike(f'%{q}%')

    
    parking_lots = ParkingLot.query.filter(filters).all()

    
    result = []
    for lot in parking_lots:
        free_spots_count = (
            db.session.query(func.count(ParkingSpot.id))
            .filter(ParkingSpot.parking_lot_id == lot.id, ParkingSpot.status == 'F')
            .scalar()
        )

        result.append({
            'id': lot.id,
            'name': lot.name,
            'price': lot.price,
            'address': lot.address,
            'pincode': lot.pincode,
            'spots': free_spots_count
        })

    return jsonify(result)
@app.route('/reserve_spot', methods=['POST'])
def reserve_spot():
    data = request.json
    user_id = data['user_id']
    lot_id = data['parking_lot_id']
    vehicle_no = data['vehicle_no']
    start_date = datetime.utcnow().date()
    start_time = datetime.utcnow().time()

    try:
        with db.session.begin_nested(): 
           
            spot = db.session.execute(
                db.select(ParkingSpot)
                .with_for_update()
                .filter_by(parking_lot_id=lot_id, status='F')
                .order_by(ParkingSpot.id)
                .limit(1)
            ).scalar_one_or_none()

            if not spot:
                return jsonify({"message": "No available spots"}), 400

   
            spot.status = 'reserved'

     
            reservation = Reserve(
                parking_spot_id=spot.id,
                parking_lot_id=lot_id,
                user_id=user_id,
                vehicle_no=vehicle_no,
                startdate=start_date,
                starttime=start_time,
                status='T'
            )
            db.session.add(reservation)
        db.session.commit()
        return jsonify({"message": "Reservation successful", "spot_id": spot.id}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "Error during reservation", "error": str(e)}), 500


@app.route('/get_reservations/<int:user_id>', methods=['GET'])
def get_reservations(user_id):
    reservations = Reserve.query.filter_by(user_id=user_id).all()

    result = []
    for r in reservations:
        result.append({
            'id': r.id,
            'vehicle_no': r.vehicle_no,
            'start_date': r.startdate.isoformat() if r.startdate else None,
            
            'parking_lot_name': r.parking_lot.name if r.parking_lot else 'Unknown',
            'status':r.status
        })

    return jsonify(result)
@app.route('/api/reservations/<int:reservation_id>', methods=['GET'])
def get_reservation(reservation_id):
    reservation = Reserve.query.filter_by(id=reservation_id).first()

    
 

   
    return jsonify({
        'id': reservation.id,
        'vehicle_no': reservation.vehicle_no,
        'start_date': reservation.startdate.strftime('%Y-%m-%d'),
        
        'parking_lot_name': reservation.parking_lot.name,
        'parking_spot_id':reservation.parking_spot_id ,
        'cost': reservation.parking_lot.price
    })

@app.route('/release_spot', methods=['POST'])
def release_spot():
    data = request.get_json()
    reserve_id = data.get('reserve_id')
    spot_id = data.get('spot_id')

    try:
        reservation = Reserve.query.get(reserve_id)
        if not reservation:
            return jsonify({'message': 'Reservation not found'}), 404

        
        now = datetime.now()
        start_datetime = datetime.combine(reservation.startdate, reservation.starttime)
        duration_hours = max(1, int((now - start_datetime).total_seconds() // 3600))

      
        parking_lot = ParkingLot.query.get(reservation.parking_lot_id)
        if not parking_lot:
            return jsonify({'message': 'Parking lot not found'}), 404

        cost = duration_hours * parking_lot.price

      
        reservation.enddate = now.date()
        reservation.endtime = now.time()
        reservation.cost = cost
        reservation.status = 'F'  

   
        spot = ParkingSpot.query.get(spot_id)
        if spot:
            spot.status = 'F'

        db.session.commit()

        return jsonify({'message': 'Spot released successfully', 'cost': cost}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Error: {str(e)}'}), 500




if __name__ == "__main__":
    app.run(debug=True)
