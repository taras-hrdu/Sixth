from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from os import abort

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://myuser:230902@localhost:3306/studentdb'
db = SQLAlchemy(app)
ma = Marshmallow(app)


class Devices(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    brand = db.Column(db.String(10)) 
    price = db.Column(db.Integer)
    name = db.Column(db.String(10))
    items_for_cake = db.Column(db.String(20))
    weight_in_kg = db.Column(db.Integer)
    color = db.Column(db.String(10))
    power = db.Column(db.Integer)
    guarantee = db.Column(db.Integer)


    def __init__(self, brand, price, name, items_for_cake, weight_in_kg, color, power, guarantee):
        self.brand = brand
        self.price = price
        self.name = name
        self.items_for_cake = items_for_cake
        self.weight_in_kg = weight_in_kg
        self.color = color
        self.power = power
        self.guarantee = guarantee


class DevicesSchema(ma.Schema):
    class Meta:
        fields = ('brand', 'price', 'name', 'items_for_cake', 'weight_in_kg', 'color','power','guarantee')


device_schema = DevicesSchema()
devices_schema = DevicesSchema(many=True)


@app.route("/devices", methods=["GET"])
def get_devices():
    devices = Devices.query.all()
    result = devices_schema.dump(devices)
    return jsonify(result)


@app.route("/devices/<id>", methods=["GET"])
def get_device(id):
    device = Devices.query.get(id)
    if device is None:
        abort(404)
    return device_schema.jsonify(device)


@app.route("/devices", methods=["POST"])
def add_device():
    new_device = Devices(request.json['brand'], request.json['price'], request.json['name'], 
    request.json['items_for_cake'], request.json['weight_in_kg'], request.json['color'], 
    request.json['power'], request.json['guarantee'])
    db.session.add(new_device)
    db.session.commit()
    return device_schema.jsonify(new_device)


@app.route("/devices/<id>", methods=["PUT"])
def update_device(id):
    device = Devices.query.get(id)
    if device is None:
        abort(404)
    device.brand = request.json['brand']
    device.price = request.json['price']
    device.name = request.json['name']
    device.items_for_cake = request.json['items_for_cake']
    device.weight_in_kg = request.json['weight_in_kg']
    device.color = request.json['color']
    device.power =  request.json['power']
    device.guarantee = request.json['guarantee']
    db.session.commit()
    return device_schema.jsonify(device)


@app.route("/devices/<id>", methods=["DELETE"])
def delete_device(id):
    device = Devices.query.get(id)
    if device is None:
        abort(404)
    db.session.delete(device)
    db.session.commit()
    return device_schema.jsonify(device)


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)