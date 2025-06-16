from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    type = db.Column(db.String(50), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)
    address = db.Column(db.String(50))
    phonenumber = db.Column(db.String(10), nullable=False)

    reservations = db.relationship('Reserve', back_populates='user', cascade="all, delete", passive_deletes=True)

class ParkingLot(db.Model):
    __tablename__ = "parkinglot"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Integer)
    address = db.Column(db.String(50), nullable=False)
    pincode = db.Column(db.Integer, nullable=False)
    spots = db.Column(db.Integer, nullable=False)

    parking_spots = db.relationship('ParkingSpot', back_populates='parking_lot', cascade="all, delete", passive_deletes=True)
    reservations = db.relationship('Reserve', back_populates='parking_lot', cascade="all, delete", passive_deletes=True)

class ParkingSpot(db.Model):
    __tablename__ = "parkingspot"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    status = db.Column(db.String(2), nullable=False)
    parking_lot_id = db.Column(db.Integer, db.ForeignKey("parkinglot.id", ondelete='CASCADE'))

    parking_lot = db.relationship('ParkingLot', back_populates='parking_spots', passive_deletes=True)
    reservations = db.relationship('Reserve', back_populates='parking_spot', cascade="all, delete", passive_deletes=True)

class Reserve(db.Model):
    __tablename__ = "reserve"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    parking_spot_id = db.Column(db.Integer, db.ForeignKey("parkingspot.id", ondelete='CASCADE'))
    user_id = db.Column(db.Integer, db.ForeignKey("user.id", ondelete='CASCADE'))
    parking_lot_id = db.Column(db.Integer, db.ForeignKey("parkinglot.id", ondelete='CASCADE'))

    vehicle_no = db.Column(db.String(15), nullable=False)
    startdate = db.Column(db.Date, nullable=False)
    enddate = db.Column(db.Date)
    starttime = db.Column(db.Time)
    endtime = db.Column(db.Time)
    cost = db.Column(db.Integer)

    user = db.relationship("User", back_populates="reservations", passive_deletes=True)
    parking_spot = db.relationship("ParkingSpot", back_populates="reservations", passive_deletes=True)
    parking_lot = db.relationship("ParkingLot", back_populates="reservations", passive_deletes=True)
