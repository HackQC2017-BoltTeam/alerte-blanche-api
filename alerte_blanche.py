import os

from flask import Flask
from flask import jsonify
from flask import request


app = Flask(__name__)


FLASK_DEBUG = os.environ.get('FLASK_DEBUG', False)


@app.route("/version")
def ping():
    version_dict = {
        "version": "0.0.1",
        "debug": bool(FLASK_DEBUG),
    }
    return jsonify(version_dict)


if __name__ == "__main__":
    app.run(debug=FLASK_DEBUG, host='0.0.0.0', port=5000)
