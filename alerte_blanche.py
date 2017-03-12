import datetime
import os
import re

from functools import wraps

import requests

from peewee import CharField
from peewee import DateTimeField
from peewee import DoesNotExist
from peewee import DoubleField
from peewee import ForeignKeyField
from peewee import Model
from peewee import PrimaryKeyField
from peewee import SqliteDatabase

from flask import Flask
from flask import jsonify
from flask import request
from flask import session


#
# Database init
#

db_name = 'alerte_blanche.db'
db = SqliteDatabase(db_name)

class BaseModel(Model):
    class Meta:
        database = db

class User(BaseModel):
    id = PrimaryKeyField()
    first_name = CharField()
    last_name = CharField()
    telephone_number = CharField()
    email = CharField(unique=True)

    def to_json(self):
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'telephone_number': self.telephone_number,
            'email': self.email,
            'plates': [p.to_json() for p in self.plates],
            'signaling_count': self.signalings.count(),
        }

class LicensePlate(BaseModel):
    id = PrimaryKeyField()
    number = CharField()
    user_id = ForeignKeyField(User, related_name='plates')

    def to_json(self):
        return {
            'id': self.id,
            'number': self.number,
        }

class AuthToken(BaseModel):
    id = PrimaryKeyField()
    token = CharField()
    user_id = ForeignKeyField(User, unique=True, related_name='token')

class Signaling(BaseModel):
    id = PrimaryKeyField()
    plate_number = CharField()
    latitude = DoubleField(null=True)
    longitude = DoubleField(null=True)
    timestamp = DateTimeField(default=datetime.datetime.now)
    user_id = ForeignKeyField(User, related_name='signalings')

    def to_json(self):
        return {
            'plate_number': self.plate_number,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'timestamp': self.timestamp.isoformat(),
            'user_id': self.user_id.id
        }


db.connect()
tables = [
    AuthToken,
    LicensePlate,
    Signaling,
    User,
]
db.create_tables(tables, safe=True)

#
# App init
#

app = Flask(__name__)

app.secret_key = b'\xb5\xf2v\xba\x8d\x1b\x86\xabO\xc9\x8e\x1a<m\x17mC1\xf4<\x18\xbeR\xd1'

FLASK_DEBUG = os.environ.get('FLASK_DEBUG', False)
GCM_API_KEY = os.environ.get('GCM_API_KEY', False)

def login_required(func):
    @wraps(func)
    def inner(*args, **kwargs):
        if not session.get('user_id'):
            return ('unauthenticated', 401)
        return func(*args, **kwargs)
    return inner

def gcm_push(recipient, title, message, action, payload):
    if not GCM_API_KEY:
        return None
    headers = {'Authorization': 'key=' + GCM_API_KEY}
    gcm_payload = {
        'to': recipient,
        'data': {
            'title': title,
            'message': message,
            'action': action,
            'payload': payload,
        },
    }
    r = requests.post('https://gcm-http.googleapis.com/gcm/send',
                      headers=headers, json=gcm_payload)
    return r.json()

def normalize_plate_number(plate_number):
    return re.sub(r'[^a-zA-Z0-9]+', '', plate_number).upper()


@app.route("/version")
def version():
    version_dict = {
        "version": "0.0.1",
        "debug": bool(FLASK_DEBUG),
    }
    return jsonify(version_dict)


@app.route("/users", methods=['POST'])
def register():
    email = request.json['email']
    telephone_number = request.json.get('telephone_number', '')
    first_name = request.json.get('first_name', '')
    last_name = request.json.get('last_name', '')
    user = User(email=email, telephone_number=telephone_number,
                first_name=first_name, last_name=last_name)
    user.save()
    plate_number = request.json.get('plate_number')
    if plate_number is not None:
        plate_number = normalize_plate_number(plate_number)
        plate = LicensePlate(user_id=user.id, number=plate_number)
        plate.save()
    return jsonify(user.to_json())


@app.route("/license-plates", methods=['POST'])
@login_required
def register_license_plate():
    user_id = session['user_id']
    number = request.json['number']
    plate = LicensePlate(user_id=user_id, number=number)
    plate.save()
    return jsonify(plate.to_json())


@app.route("/users/me")
@login_required
def get_user():
    user_id = session['user_id']
    user = User.get(id=user_id)
    return jsonify(user.to_json())


@app.route("/users/me/token", methods=['PUT'])
@login_required
def register_auth_token():
    user_id = session['user_id']
    token = request.json['token']
    AuthToken.insert(token=token, user_id=user_id).upsert().execute()
    return ('', 204)


@app.route("/signal", methods=['POST'])
@login_required
def signal_license_plate():
    """Find the user that owns license plate, if any, then notify him."""
    plate_number = request.json['plate_number']

    signaling = Signaling(plate_number=plate_number, user_id=session['user_id'],
                          latitude=request.json.get('latitude'),
                          longitude=request.json.get('longitude'))
    signaling.save()
    payload = signaling.to_json()
    try:
        plate = LicensePlate.get(number=plate_number)
        token = plate.user_id.token.get().token
        r = gcm_push(recipient=token,
                 title="Attention! Remorquage imminent!",
                 message="Votre voiture a été repérée en zone de déneigement." +
                         "Touchez pour afficher les stationnements les plus près.",
                 action="towing_alert",
                 payload=payload)
        print(r)
    except DoesNotExist as e:
        pass

    return jsonify(payload)


@app.route("/login", methods=['POST'])
def login():
    """Secure, PCI-compliant login"""
    email = request.json['email']
    try:
        user = User.get(email=email)
    except DoesNotExist as e:
        return ('No such user', 400)
    else:
        session['email'] = user.email
        session['user_id'] = user.id
        return jsonify(user.to_json())


@app.route('/logout', methods=['POST'])
def logout():
    session.pop('email', None)
    session.pop('user_id', None)
    return ('', 204)


if __name__ == "__main__":
    app.run(debug=FLASK_DEBUG, host='0.0.0.0', port=5000)
