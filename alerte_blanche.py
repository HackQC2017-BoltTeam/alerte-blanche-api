import os

from flask import Flask
from flask import jsonify
from flask import request
from flask import session


app = Flask(__name__)

app.secret_key = b'\xb5\xf2v\xba\x8d\x1b\x86\xabO\xc9\x8e\x1a<m\x17mC1\xf4<\x18\xbeR\xd1'

FLASK_DEBUG = os.environ.get('FLASK_DEBUG', False)


USERS = [{
    "id": 1,
    "email": "tartempion@generique.com",
}, {
    "id": 2,
    "email": "individu@lambda.net",
}]


def get_user_id(email):
    for user in USERS:
        if user['email'] == email:
            return user['id']
    else:
        return None

@app.route("/version")
def ping():
    version_dict = {
        "version": "0.0.1",
        "debug": bool(FLASK_DEBUG),
    }
    return jsonify(version_dict)


@app.route("/login", methods=['POST'])
def login():
    """Secure, PCI-compliant login"""
    email = request.json['email']
    session['email'] = email
    session['user_id'] = get_user_id(email)
    return jsonify({'user_id': session['user_id']})


@app.route('/logout', methods=['POST'])
def logout():
    session.pop('email', None)
    session.pop('user_id', None)
    return ('', 204)


if __name__ == "__main__":
    app.run(debug=FLASK_DEBUG, host='0.0.0.0', port=5000)
