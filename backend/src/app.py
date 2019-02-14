import os
import sqlalchemy
from flask import Flask, jsonify, request
from werkzeug.exceptions import HTTPException

from db import Session, bind_session_engine, tables
from models import Beer, InvalidBeerRatingError

app = Flask(__name__)
# The following allows @app.errorhandler(HTTPException) to work
app.config["TRAP_HTTP_EXCEPTIONS"] = True


@app.teardown_request
def shutdown_session(exception=None):
    Session.remove()


@app.errorhandler(HTTPException)
def http_error(error):
    response = jsonify(error=error.description)
    response.status_code = error.code
    return response


@app.errorhandler(sqlalchemy.orm.exc.NoResultFound)
def not_found(error):
    response = jsonify(error="Not found")
    response.status_code = 404
    return response


@app.errorhandler(InvalidBeerRatingError)
def invalid_beer_rating(error):
    response = jsonify(error=str(error))
    response.status_code = 400
    return response


@app.errorhandler(KeyError)
def key_error(error):
    response = jsonify(error=str(error))
    response.status_code = 400
    return response


@app.route("/beers")
def get_beers():
    session = Session()
    beers = session.query(Beer).all()
    resp = {beer.name: beer.to_json() for beer in beers}
    return jsonify(resp)


@app.route("/beer/<beer_name>")
def get_beer(beer_name):
    session = Session()
    beer = session.query(Beer).filter_by(name=beer_name.lower()).one()
    return jsonify(beer.to_json())


@app.route("/beer/<beer_name>", methods=["PUT"])
def add_beer(beer_name):
    session = Session()
    incoming_data = request.get_json()
    beer = session.query(Beer).filter_by(name=beer_name.lower()).first()
    if not beer:
        beer = Beer(
            beer_name,
            int(incoming_data["rating"]),
            incoming_data["brewerydb_id"],
            comment=incoming_data.get("comment")
        )
        session.add(beer)
    else:
        beer.rating = int(incoming_data["rating"])
        beer.brewerydb_id = incoming_data["brewerydb_id"]
        beer.comment = incoming_data.get("comment")
        beer.validate()
    session.commit()
    response = jsonify(ref="/beer/{0}".format(beer.name))
    response.status_code = 201
    return response


@app.route("/beer/<beer_name>", methods=["DELETE"])
def remove_beer(beer_name):
    session = Session()
    beer = session.query(Beer).filter_by(name=beer_name.lower()).one()
    session.delete(beer)
    session.commit()
    response = jsonify()
    response.status_code = 201
    return response


if __name__ == "__main__":

    engine = bind_session_engine(
        "mysql+pymysql://ibeer:super-secret-password@ibeer-db-service/ibeer", encoding="utf-8"
    )

    # Create DB tables
    tables.metadata.create_all(engine)

    app.run(host="0.0.0.0", port=8080)
