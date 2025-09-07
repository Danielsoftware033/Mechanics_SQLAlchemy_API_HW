from app import create_app
from app.models import Mechanic, db
import unittest 
from werkzeug.security import check_password_hash, generate_password_hash
from app.util.auth import encode_token

#Run Script: python -m unittest discover tests  

class TestMechanic(unittest.TestCase):

    def setUp(self):
        self.app = create_app('TestingConfig')
        self.mechanic = Mechanic(first_name="Thomas", last_name="Smith", email="thomas@email.com", password=generate_password_hash("123"), salary=75000.00, address="123 Fun St.")
        with self.app.app_context():
            db.drop_all()
            db.create_all()
            db.session.add(self.mechanic)
            db.session.commit()

        self.client = self.app.test_client()
        self.token = encode_token(1)

    def test_create_mechanic(self):
        mechanic_payload = {
            "address": "21 Fun St",
            "email": "test@email.com",
            "first_name": "Thomas",
            "last_name": "Smith",
            "password": "123",
            "salary": 75000.00
        }

        response = self.client.post('/mechanics', json=mechanic_payload)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json['first_name'], "Thomas")
        self.assertTrue(check_password_hash(response.json['password'], "123"))


    #negative check
    def test_invalid_create(self): #missing email which is required
        mechanic_payload = { 
            "address": "21 Fun St",
            "first_name": "Thomas",
            "last_name": "Smith",
            "password": "123",
            "salary": 75000.00
        }

        response = self.client.post('/mechanics', json=mechanic_payload)
        self.assertEqual(response.status_code, 400)
        self.assertIn('email', response.json)


    def test_get_mechanics(self):
        response = self.client.get('/mechanics')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json[0]['first_name'], 'Thomas')

    
    def test_login(self):
        login_creds = {
            "email": "thomas@email.com",
            "password": "123"
        }

        response = self.client.post('/mechanics/login', json=login_creds)
        self.assertEqual(response.status_code, 200)
        self.assertIn('token', response.json)


    def test_delete(self):
        headers = {"Authorization": "Bearer " + self.token}

        response = self.client.delete('/mechanics', headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['message'], "Successfully deleted mechanic 1")


    #negative check
    def test_unauthorized_delete(self):
        
        response = self.client.delete('/mechanics')
        self.assertEqual(response.status_code, 401)


    def test_update(self):
        headers = {"Authorization": "Bearer " + self.token}

        update_payload = {
            "address": "21 Fun St",
            "email": "NEW_EMAIL@email.com",
            "first_name": "Thomas",
            "last_name": "Smith",
            "password": "123",
            "salary": 75000.00
        }

        response = self.client.put('/mechanics', headers=headers, json=update_payload)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['email'], "NEW_EMAIL@email.com")


    #negative check, missing email
    def test_invalid_update(self):
        headers = {"Authorization": "Bearer " + self.token}

        update_payload = {
            "address": "21 Fun St",
            "first_name": "Thomas",
            "last_name": "Smith",
            "password": "123",
            "salary": 75000.00
        }

        response = self.client.put('/mechanics', headers=headers, json=update_payload)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json['email'], "NEW_EMAIL@email.com")