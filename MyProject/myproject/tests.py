import unittest

from pyramid import testing

class HomeViewTest(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()

    def tearDown(self):
        testing.tearDown()

    def test_home(self):
        from views import home
        request = testing.DummyRequest()
        response = home(request)
        self.assertEqual(response.status_code, 200)


