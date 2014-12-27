import unittest
from mock import sentinel

from db import bind_session_engine, tables, Session
from models import Beer, InvalidBeerRatingError


class BeerTestCase(unittest.TestCase):

    def test_properties_uses_defaults(self):
        beer = Beer("my-beer", 5, sentinel.brewerydb_id)
        self.assertEquals(beer.name, "my-beer")
        self.assertEquals(beer.rating, 5)
        self.assertEquals(beer.brewerydb_id, sentinel.brewerydb_id)
        self.assertEquals(beer.comment, None)

    def test_properties_overwrites_defaults(self):
        beer = Beer(
            "my-beer", 5, sentinel.brewerydb_id, sentinel.comment
        )
        self.assertEquals(beer.name, "my-beer")
        self.assertEquals(beer.rating, 5)
        self.assertEquals(beer.brewerydb_id, sentinel.brewerydb_id)
        self.assertEquals(beer.comment, sentinel.comment)

    def test_properties_names_are_lowercased(self):
        beer = Beer(
            "MY-BEER", 5, sentinel.brewerydb_id, sentinel.comment
        )
        self.assertEquals(beer.name, "my-beer")
        self.assertEquals(beer.rating, 5)
        self.assertEquals(beer.brewerydb_id, sentinel.brewerydb_id)
        self.assertEquals(beer.comment, sentinel.comment)

    def test_properties_raises_error_if_invalid_rating(self):
        self.assertRaises(
            InvalidBeerRatingError,
            # constructor to test
            Beer,
            # arguments for constructor
            "my-beer", sentinel.rating, sentinel.brewerydb_id, sentinel.comment
        )

    def test_to_json_without_comments(self):
        beer = Beer("my-beer", 5, sentinel.brewerydb_id)
        self.assertEquals(
            beer.to_json(),
            {
                "rating": 5,
                "brewerydb_id": sentinel.brewerydb_id,
            }
        )

    def test_to_json_with_comments(self):
        beer = Beer(
            "my-beer", 5, sentinel.brewerydb_id, sentinel.comment
        )
        self.assertEquals(
            beer.to_json(),
            {
                "rating": 5,
                "brewerydb_id": sentinel.brewerydb_id,
                "comment": sentinel.comment
            }
        )


class TableMappingsTestCase(unittest.TestCase):

    def setUp(self):
        engine = bind_session_engine("sqlite:///:memory:", echo=False)
        tables.metadata.create_all(engine)
        self.session = Session()

    def test_beer_relations_without_comments(self):
        self.session.add(Beer("Leffe", 8, "url_to_beer"))
        self.session.commit()
        self.session.expunge_all()

        b = self.session.query(Beer).one()
        self.assertTrue(isinstance(b, Beer))
        self.assertTrue(b.name, "Leffe")
        self.assertTrue(b.rating, 8)
        self.assertTrue(b.brewerydb_id, "url_to_beer")

    def test_beer_relations_with_comments(self):
        self.session.add(Beer("Leffe", 8, "url_to_beer", comment="Good beer!"))
        self.session.commit()
        self.session.expunge_all()

        b = self.session.query(Beer).one()
        self.assertTrue(isinstance(b, Beer))
        self.assertTrue(b.name, "Leffe")
        self.assertTrue(b.rating, 8)
        self.assertTrue(b.brewerydb_id, "url_to_beer")
        self.assertTrue(b.comment, "Good beer!")
