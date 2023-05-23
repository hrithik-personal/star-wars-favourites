from django.test import TestCase, override_settings
from rest_framework.test import APIClient
from users.models import User
from utils.redis_core import redis_connection as cache


class PlanetTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Add initial json() for testing
        user = User(
            username="Test_username",
            first_name="Test_first_name",
            last_name="Test_last_name",
            email="Test_email"
        )
        user.save()

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.get(username='Test_username')

    def run(self, result=None):
        ''' Test case fails if exception is raised within code-block '''
        try:
            super().run(result)
        except Exception as e:
            self.fail(f"Test case raised an exception: {e}")


    @override_settings(CACHES={"default": {"BACKEND": "django.core.cache.backends.dummy.DummyCache"}})
    def test_1_get_planet_list_from_api(self):
        # Flush all Redis keys
        cache.flushall()

        # Fetch planet list from SWAPI API
        params = {'user_id': self.user.id}
        response = self.client.get('/planets/', params)
        self.assertEqual(response.status_code, 200)
        planet_list_len = len(response.json())

        # Fetch planet list again, should come from cache and be the same
        response = self.client.get('/planets/', params)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), planet_list_len)


    def test_2_set_planet_favourite_with_custom_name(self):
        params = {'user_id': self.user.id}
        response = self.client.get('/planets/', params)
        self.assertEqual(response.status_code, 200)
        planet = response.json()[0]

        # Set the planet as a favourite with a custom_name
        params = {'user_id': self.user.id, 'swapi_url': planet['url'], 'custom_name': 'My Favorite planet'}
        response = self.client.post('/favourites/planets/add/', params)
        self.assertEqual(response.status_code, 200)

        # Find the favourite planet in the response and check the custom_name
        response = self.client.get('/planets/', params)
        self.assertEqual(response.status_code, 200)
        favourite_planet = next((m for m in response.json() if m['url'] == planet['url']), None)
        self.assertIsNotNone(favourite_planet)
        self.assertTrue(favourite_planet['is_favourite'])
        self.assertEqual(favourite_planet['name'], 'My Favorite planet')

    def test_3_planet_search(self):
        params = {'user_id': self.user.id}
        response = self.client.get('/planets/', params)
        self.assertEqual(response.status_code, 200)
        planet = response.json()[0]

        # Set the planet as a favourite with a custom_name
        params = {'user_id': self.user.id, 'swapi_url': planet['url'], 'custom_name': 'My Favorite planet'}
        response = self.client.post('/favourites/planets/add/', params)
        self.assertEqual(response.status_code, 200)

        # Search for a favourite planet with a custom_name
        params = {'user_id': self.user.id, 'search_name': 'Favorite'}
        response = self.client.get('/planets/', params)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)
