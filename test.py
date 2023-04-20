import unittest
import csv
from  app import app
'''
python -m unittest test.py 

coverage run -m unittest discover

coverage report


'''

class bp_general(unittest.TestCase):

    def test_index(self):
        tester = app.test_client(self)
        response = tester.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'<title>Home</title>', response.data)


class bp_feestdag(unittest.TestCase):

    def test_feestdag(self):
        tester = app.test_client(self)
        response = tester.get("/feestdag")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'<h1>Feestdagen</h1>', response.data)

    #def test_toevoegen(self):
        #tester = app.test_client(self)
        #response = tester.get("/toevoegen", follow_redirects=True)
        #self.assertEqual(response.status_code, 200)
        #self.assertIn(b'<h1>Feestdagen</h1>',response.data)

    def test_edit(self):
        tester = app.test_client(self)
        response = tester.get("/feestdag/edit")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'<h1>Bewerk feestdagen</h1>', response.data)


    def test_bevestig(self):
        tester = app.test_client(self)
        response = tester.get("/bevestigen")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'<h1>Feestdagen die nog moeten worden bevestigd</h1>', response.data)

    def test_verwijder(self):
        tester= app.test_client(self)
        response = tester.get('/verwijder-feestdag/<datum>',follow_redirects=True)
        self.assertEqual(response.status_code,405)
        self.assertIn(b'<h1>Bewerk feestdagen</h1>', response.data)


    






class bp_profile(unittest.TestCase):
    #auth file
    def test_login(self):
        tester = app.test_client(self)
        response = tester.get('/login')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'  <h1>Login</h1>', response.data)


    def test_logout(self):
        tester = app.test_client(self)
        response = tester.get('/logout', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'  <h1>Login</h1>', response.data)

    #views_profile file
    def test_add_profile(self):
        tester = app.test_client(self)
        response = tester.get('/add_profile', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'<h1>Add Profile</h1>', response.data)

    def test_show_profile(self):
        tester = app.test_client(self)
        response = tester.get('/show_profiles')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'<h1>profielen</h1>', response.data)
    
    def test_show_profile(self):
        tester = app.test_client(self)
        response = tester.get('/show_profiles')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'<h1>profielen</h1>', response.data)






