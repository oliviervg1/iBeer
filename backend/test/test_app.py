import unittest
import json

from db import Session, tables, bind_session_engine
from models import Beer
from app import app


class AppTestCase(unittest.TestCase):

    def setUp(self):
        app.config["TESTING"] = True
        self.app = app.test_client()

        engine = bind_session_engine("sqlite:///:memory:")
        metadata = tables.metadata
        metadata.create_all(bind=engine)
        self.session = Session()

        # Fixture data
        self.leffe = Beer("Leffe", 8, "url_to_beer", comment="Good beer!")
        self.brooklyn = Beer("Brooklyn Lager", 6, "url_to_beer")
        self.session.add_all([self.leffe, self.brooklyn])
        self.session.commit()

    def tearDown(self):
        Session.remove()

    def test_routing_error(self):
        r = self.app.get("/this/api/does/not/exist/yet")
        self.assertEqual(r.status_code, 404)
        self.assertEqual(
            json.loads(r.data),
            {
                "error": "The requested URL was not found on the server. "
                         " If you entered the URL manually please check your "
                         "spelling and try again."
            }
        )

    def test_get_beers(self):
        r = self.app.get("/beers")
        self.assertEqual(r.status_code, 200)
        self.assertEqual(
            json.loads(r.data),
            {
                "brooklyn lager": {
                    "brewerydb_id": "url_to_beer",
                    "rating": 6
                },
                "leffe": {
                    "brewerydb_id": "url_to_beer",
                    "comment": "Good beer!",
                    "rating": 8
                }
            }
        )

    def test_get_beer_without_comment(self):
        r = self.app.get("/beer/brooklyn lager")
        self.assertEqual(r.status_code, 200)
        self.assertEqual(
            json.loads(r.data),
            {"rating": 6, "brewerydb_id": "url_to_beer"}
        )

    def test_get_beer_with_comment(self):
        r = self.app.get("/beer/leffe")
        self.assertEqual(r.status_code, 200)
        self.assertEqual(
            json.loads(r.data),
            {
                "comment": "Good beer!",
                "rating": 8,
                "brewerydb_id": "url_to_beer"
            }
        )

    def test_add_beer_invalid_json_fails(self):
        r = self.app.put(
            "/beer/my-beer",
            content_type="application/json",
            data="THIS IS NOT JSON"
        )
        self.assertEqual(r.status_code, 400)
        self.assertEqual(
            json.loads(r.data),
            {
                "error": "The browser (or proxy) sent a request that this "
                         "server could not understand."
            }
        )

    def test_add_beer_invalid_rating_fails(self):
        r = self.app.put(
            "/beer/my-beer",
            content_type="application/json",
            data=json.dumps({"rating": 20, "brewerydb_id": "url_to_beer"})
        )
        self.assertEqual(r.status_code, 400)
        self.assertEqual(
            json.loads(r.data),
            {"error": "Beer ratings should be a number between 0 and 10."}
        )

    def test_add_beer_success(self):
        r = self.app.put(
            "/beer/my-beer",
            content_type="application/json",
            data=json.dumps({"rating": 8, "brewerydb_id": "url_to_beer"})
        )
        self.assertEqual(r.status_code, 201)
        self.assertEqual(json.loads(r.data), {"ref": "/beer/my-beer"})

        # Check beer has been added
        Session.remove()
        new_session = Session()
        self.assertTrue(
            new_session.query(
                Beer
            ).filter_by(name="my-beer").first() is not None
        )

    def test_update_beer_invalid_rating_fails(self):
        r = self.app.put(
            "/beer/leffe",
            content_type="application/json",
            data=json.dumps({"rating": 20, "brewerydb_id": "url_to_beer"})
        )
        self.assertEqual(r.status_code, 400)
        self.assertEqual(
            json.loads(r.data),
            {"error": "Beer ratings should be a number between 0 and 10."}
        )

        # Check beer hasn't been updated
        Session.remove()
        new_session = Session()
        leffe = new_session.query(Beer).filter_by(name="leffe").one()
        self.assertEqual(leffe.rating, 8)

    def test_update_beer_success(self):
        r = self.app.put(
            "/beer/leffe",
            content_type="application/json",
            data=json.dumps({"rating": 10, "brewerydb_id": "url_to_beer"})
        )
        self.assertEqual(r.status_code, 201)
        self.assertEqual(json.loads(r.data), {"ref": "/beer/leffe"})

        # Check beer has been updated
        Session.remove()
        new_session = Session()
        leffe = new_session.query(Beer).filter_by(name="leffe").one()
        self.assertEqual(leffe.rating, 10)

    def test_remove_beer_doesnt_exist(self):
        r = self.app.delete(
            "/beer/non-existant-beer",
            content_type="application/json",
            data=json.dumps({})
        )
        self.assertEqual(r.status_code, 404)
        self.assertEqual(json.loads(r.data), {"error": "Not found"})

    def test_remove_beer_success(self):
        r = self.app.delete(
            "/beer/leffe",
            content_type="application/json",
            data=json.dumps({})
        )
        self.assertEqual(r.status_code, 201)
        self.assertEqual(json.loads(r.data), {})

        # Check beer has been deleted
        Session.remove()
        new_session = Session()
        self.assertTrue(
            new_session.query(
                Beer
            ).filter_by(name="leffe").first() is None
        )
