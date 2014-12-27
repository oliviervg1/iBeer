from db import tables
from sqlalchemy.orm import mapper


class Beer(object):

    def __init__(self, name, rating, brewerydb_id, comment=None):
        self.name = name.lower()
        self.rating = rating
        self.brewerydb_id = brewerydb_id
        self.comment = comment
        self.validate()

    def validate(self):
        if not (0 <= self.rating <= 10):
            raise InvalidBeerRatingError(
                "Beer ratings should be a number between 0 and 10."
            )

    def to_json(self):
        json_response = {
            "rating": self.rating,
            "brewerydb_id": self.brewerydb_id
        }
        if self.comment:
            json_response["comment"] = self.comment
        return json_response


class InvalidBeerRatingError(Exception):
    pass


mapper(Beer, tables.beers)
