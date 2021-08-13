from flask import Flask, render_template, jsonify
import firebase_admin
from firebase_admin import firestore
import datetime

app = Flask(__name__)

firebase_admin.initialize_app()
SUPERHEROES = firestore.client().collection('superheroes')


@app.route("/", methods=["GET"])
def hello():
    """ Return a friendly HTTP greeting. """

    hero = SUPERHEROES.document()
    req = {
        "name": "Friso",
        "power": "Speed",
        "created": datetime.datetime.now()
    }
    hero.set(req)
    return jsonify({'id': hero.id}), 201

    # who = flask.request.args.get("who", "World")
    # return f"Hello {who}!\n"


@app.route("/list", methods=["GET"])
def show_list():
    """ Return a friendly HTTP greeting. """

    response = []
    docs = SUPERHEROES.stream()
    for doc in docs:
        response.append(doc.to_dict())
    return jsonify(response), 201


@app.route("/test", methods=["GET"])
def test():
    docs = SUPERHEROES.stream()
    response = []
    for doc in docs:
        response.append(doc.to_dict())
    return render_template('plain.html', my_string="Test Ruben", my_list=[0, 1, 2, 3, 4, 5], heroes=response)


if __name__ == "__main__":
    # Used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    app.run(host="localhost", port=8080, debug=True)
