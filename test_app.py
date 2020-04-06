import os
import unittest
import json

from app import app
from models import set_up_db, Movie, Actor
from flask_sqlalchemy import SQLAlchemy

EXECUTIVE_PRODUCER = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik5VRkNSRVUxTmpFeE1EZzNNekZETlVJNVJqTkdOekpCTmtGQ09FVkdPVFUyTTBOR1JUZ3dRZyJ9.eyJpc3MiOiJodHRwczovL2NvZmZlZXNob3AtbmcuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVlOGEyYmE4NjU5NTExMGMxMGNmZjkxZCIsImF1ZCI6ImNhcHN0b25lLW1vdmllLWFwaSIsImlhdCI6MTU4NjExNjY0NSwiZXhwIjoxNTg2MjAzMDQ1LCJhenAiOiJDWTFRaUdRQnZ4U1poUDlLRFFuTm5OSDlpa2xYQkp4eiIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmFjdG9ycyIsImRlbGV0ZTptb3ZpZXMiLCJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyIsInBhdGNoOmFjdG9ycyIsInBhdGNoOm1vdmllcyIsInBvc3Q6YWN0b3JzIiwicG9zdDptb3ZpZXMiXX0.sHwrqNPgEYUljFOOSwe4sHhP7XXNFrvSTJITsWBBZoQZhJ992-f811Q6o_FxTORypAgmAnQphNuyUkhV8ol6jIunBOu3yAMj7hU6_Tpi-Ql2sGXtz2ssIuCW4T7dISsRql2qJdeR9nst4lqnK4uor8vP2LPVEFMEbPamH8mqLUGWbkw2rAWiPpkIVrM-gVjNSKrtF2RmymHnBZGp_w7Z_AmJrNBaXGPltLyA72n3zOF2jdLMDIT0_zamL027CTHke8Z7JsEJ8TSuaGqNqGbSTw8SXWjqkqqEdRnRnwAMdBHMm8wun0nDk-usLVPwFHpGw75FdtjDL8hp2q-1G41VSw'

CASTING_DIRECTOR = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik5VRkNSRVUxTmpFeE1EZzNNekZETlVJNVJqTkdOekpCTmtGQ09FVkdPVFUyTTBOR1JUZ3dRZyJ9.eyJpc3MiOiJodHRwczovL2NvZmZlZXNob3AtbmcuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVlOGEyZDE4ODVkZDk4MGM2OGU0Yjg2OCIsImF1ZCI6ImNhcHN0b25lLW1vdmllLWFwaSIsImlhdCI6MTU4NjExODk4NSwiZXhwIjoxNTg2MjA1Mzg1LCJhenAiOiJDWTFRaUdRQnZ4U1poUDlLRFFuTm5OSDlpa2xYQkp4eiIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmFjdG9ycyIsImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIiwicGF0Y2g6YWN0b3JzIiwicGF0Y2g6bW92aWVzIiwicG9zdDphY3RvcnMiXX0.twQDo4TXDpVTulpGOQE-PIRRvtr5-tYYwNqgFDGI3ZFopldnRhBCn-VV3o6w1Ow_0LT5q28TfhN6PUZnj9cNLL4VUCfoxNhtqKT1KHnLU6pDkzk7JO0oCEGNgB-1gEcpudtfT6b5WEZjx06w11aFTVLYvAJbOu8SNFx9UYVmF1viInkzQis-I1d0JYDaZigzaZ7rbCbt16g27bjkME1Frl5vgEP7yLEGGCILJHDNfYPzBcKi8sdspDRelCj-HadK3eAtBslcQ5HDQHylcjwky_5aC-tej2QKlrxgORxXQH7ni9vc-3sIBRz0_ZiHDMQTmhP41XsIMkFC8sHsgSd87w'

CASTING_ASSISTANT = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik5VRkNSRVUxTmpFeE1EZzNNekZETlVJNVJqTkdOekpCTmtGQ09FVkdPVFUyTTBOR1JUZ3dRZyJ9.eyJpc3MiOiJodHRwczovL2NvZmZlZXNob3AtbmcuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVlOGEyZGVlNjU5NTExMGMxMGQwMDllMSIsImF1ZCI6ImNhcHN0b25lLW1vdmllLWFwaSIsImlhdCI6MTU4NjEyMTk1MiwiZXhwIjoxNTg2MjA4MzUyLCJhenAiOiJDWTFRaUdRQnZ4U1poUDlLRFFuTm5OSDlpa2xYQkp4eiIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiXX0.Ld2w7g6g3_6QOMTvc5JAp4-ub__WiUypYNwASx2fx8AFE5WQ933JIpibfbzKequzV1VQQllDS1DMbm9iO6NFK1dKiWWnqKYmaSY3QPDJ-m_OmfoQYTHyOu21_NVoYEoRuBoKYC76FGixoMG2TojAZAEAljz8xhnGNS6VyM3qDjG6pPB_2hpwlDLnhjeAryqFXOMz-QoDx_YCGg9uIKJWgwapvbym5jXh8wpFMp5mEAKDGH_1_OOgouYFD5shNFu4UDS67sevzzkVzsSoh6QoWat7l01957hJpoO6aE6AOtIYBgIcBXBlRer1Y2FA2FxodrbcI8gvYDXQ1Lu-836XhQ'


class MHTestCase(unittest.TestCase):
    """This class represents the capstone test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = app
        self.client = self.app.test_client
        self.database_path = os.environ['TEST_DB_URL']

        set_up_db(self.app, self.database_path)
        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    # ####################    MOVIE TEST STARTS #################################################

    #  GET /movies
    def test_get_movies(self):
        response = self.client().get(
            '/movies',
            headers={"Authorization": "Bearer " + CASTING_ASSISTANT}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movies'])

    # GET /movies/id
    def test_get_movie_byId(self):
        response = self.client().get(
            '/movies/1',
            headers={"Authorization": "Bearer " + CASTING_ASSISTANT}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movie'])
        self.assertEqual(data['movie']['title'], 'Nikita')

    def test_get_movie_byId_404(self):
        response = self.client().get(
            '/movies/333333',
            headers={"Authorization": "Bearer " + CASTING_ASSISTANT}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])
        self.assertEqual(data['message'], 'Resource not found')

    # POST /movies
    def test_post_movie(self):
        response = self.client().post(
            '/movies',
            json={'title': 'Sigidi', 'release_date': "2017-02-19"},
            headers={"Authorization": "Bearer " + EXECUTIVE_PRODUCER}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['message'], 'Movie added')
        self.assertEqual(data['movie']['title'], 'Sigidi')

    def test_post_movie_400(self):
        response = self.client().post(
            '/movies',
            json={'title': '', 'release_date': ""},
            headers={"Authorization": "Bearer " + EXECUTIVE_PRODUCER}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Bad Request, pls check your inputs')

    def test_post_movie_401(self):
        response = self.client().post(
            '/movies',
            json={'title': 'Unauthorize movie', 'release_date': "2019-12-23"},
            headers={"Authorization": "Bearer " + CASTING_ASSISTANT}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['message']['code'], 'unauthorized')

    # PATCH /movies
    def test_edit_movie(self):
        response = self.client().patch(
            '/movies/2',
            json={'title': 'The Squash', 'release_date': "2000-10-19"},
            headers={"Authorization": "Bearer " + CASTING_DIRECTOR}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['message'], 'Movie updated')
        self.assertEqual(data['movie']['title'], 'The Squash')

    def test_edit_movie_400(self):
        response = self.client().patch(
            '/movies/1',
            json={'title': '', 'release_date': ""},
            headers={"Authorization": "Bearer " + CASTING_DIRECTOR}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Bad Request, pls check your inputs')

    def test_edit_movie_404(self):
        response = self.client().patch(
            '/movies/4444444',
            json={'title': 'New Life', 'release_date': "2003-09-16"},
            headers={"Authorization": "Bearer " + CASTING_DIRECTOR}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource not found')

    # DELETE /movies/id
    def test_delete_movie(self):
        response = self.client().delete(
            '/movies/3',
            headers={"Authorization": "Bearer " + EXECUTIVE_PRODUCER}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['message'], 'Movie deleted successfully')

    def test_delete_movie_404(self):
        response = self.client().delete(
            '/movies/11111111',
            headers={"Authorization": "Bearer " + EXECUTIVE_PRODUCER}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource not found')

    def test_delete_movie_401(self):
        response = self.client().delete(
            '/movies/1',
            headers={"Authorization": "Bearer " + CASTING_ASSISTANT}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['message']['code'], 'unauthorized')

    #####################    MOVIE TEST ENDS #################################################

    #####################    ACTORS TEST START #################################################
    #  GET /actors
    def test_get_actors(self):
        response = self.client().get(
            '/actors',
            headers={"Authorization": "Bearer " + CASTING_ASSISTANT}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actors'])

    # GET /actors/id
    def test_get_actor_byId(self):
        response = self.client().get(
            '/actors/1',
            headers={"Authorization": "Bearer " + CASTING_ASSISTANT}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actor'])
        self.assertEqual(data['actor']['name'], 'Arnold Swaztnigger')

    def test_get_actor_byId_404(self):
        response = self.client().get(
            '/actors/121234',
            headers={"Authorization": "Bearer " + CASTING_ASSISTANT}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])
        self.assertEqual(data['message'], 'Resource not found')

    # POST /actors
    def test_post_actor(self):
        response = self.client().post(
            '/actors',
            json={'name': 'Julius', 'age': 24, "gender": "male"},
            headers={"Authorization": "Bearer " + CASTING_DIRECTOR}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['message'], 'Actor added')
        self.assertEqual(data['actor']['name'], 'Julius')

    def test_post_actor_400(self):
        response = self.client().post(
            '/actors',
            json={'name': '', 'age': '', "gender": ""},
            headers={"Authorization": "Bearer " + CASTING_DIRECTOR}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Bad Request, pls check your inputs')

    def test_post_actor_401(self):
        response = self.client().post(
            '/actors',
            json={'name': 'Czar', 'age': 14, "gender": "female"},
            headers={"Authorization": "Bearer " + CASTING_ASSISTANT}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['message']['code'], 'unauthorized')

    # PATCH /actors
    def test_edit_actor(self):
        response = self.client().patch(
            '/actors/2',
            json={'name': 'Emily', 'age': 37, "gender": "male"},
            headers={"Authorization": "Bearer " + CASTING_DIRECTOR}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['message'], 'Actor updated')
        self.assertEqual(data['actor']['name'], 'Emily')

    def test_edit_actor_400(self):
        response = self.client().patch(
            '/actors/2',
            json={'name': '', 'age': '', "gender": ""},
            headers={"Authorization": "Bearer " + CASTING_DIRECTOR}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Bad Request, pls check your inputs')

    def test_edit_actor_404(self):
        response = self.client().patch(
            '/actors/9999999',
            json={'name': 'Mike', 'age': 65, "gender": "male"},
            headers={"Authorization": "Bearer " + CASTING_DIRECTOR}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource not found')

    # DELETE /actors/id
    def test_delete_actor(self):
        response = self.client().delete(
            '/actors/3',
            headers={"Authorization": "Bearer " + CASTING_DIRECTOR}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['message'], 'Actor deleted successfully')

    def test_delete_actor_401(self):
        response = self.client().delete(
            '/actors/2',
            headers={"Authorization": "Bearer " + CASTING_ASSISTANT}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['message']['code'], 'unauthorized')

    def test_delete_actor_404(self):
        response = self.client().delete(
            '/actors/545432',
            headers={"Authorization": "Bearer " + CASTING_DIRECTOR}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource not found')


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
