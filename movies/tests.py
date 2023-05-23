from django.test import TestCase, override_settings
from rest_framework.test import APIClient
from users.models import User
from utils.redis_core import redis_connection as cache


class MovieTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Add initial data for testing
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
    def test_1_get_movie_list_from_api(self):
        # Flush all Redis keys
        cache.flushall()

        # Fetch movie list from SWAPI API
        params = {'user_id': self.user.id}
        response = self.client.get('/movies/', params)
        self.assertEqual(response.status_code, 200)
        movie_list_len = len(response.data)

        # Fetch movie list again, should come from cache and be the same
        response = self.client.get('/movies/', params)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), movie_list_len)


    def test_2_set_movie_favourite_with_custom_title(self):
        params = {'user_id': self.user.id}
        response = self.client.get('/movies/', params)
        self.assertEqual(response.status_code, 200)
        movie = response.data[0]

        # Set the movie as a favourite with a custom_title
        params = {'user_id': self.user.id, 'swapi_url': movie['url'], 'custom_title': 'My Favorite Movie'}
        response = self.client.post('/favourites/movies/add/', params)
        self.assertEqual(response.status_code, 200)

        # Find the favourite movie in the response and check the custom_title
        response = self.client.get('/movies/', params)
        self.assertEqual(response.status_code, 200)
        favourite_movie = next((m for m in response.data if m['url'] == movie['url']), None)
        self.assertIsNotNone(favourite_movie)
        self.assertTrue(favourite_movie['is_favourite'])
        self.assertEqual(favourite_movie['title'], 'My Favorite Movie')

    def test_3_movie_search(self):
        params = {'user_id': self.user.id}
        response = self.client.get('/movies/', params)
        self.assertEqual(response.status_code, 200)
        movie = response.data[0]

        # Set the movie as a favourite with a custom_title
        params = {'user_id': self.user.id, 'swapi_url': movie['url'], 'custom_title': 'My Favorite Movie'}
        response = self.client.post('/favourites/movies/add/', params)
        self.assertEqual(response.status_code, 200)

        # Search for a favourite movie with a custom_name
        params = {'user_id': self.user.id, 'search_title': 'Favorite'}
        response = self.client.get('/movies/', params)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

        # Search for an original movie name
        params = {'user_id': self.user.id, 'search_title': 'The empire'}
        response = self.client.get('/movies/', params)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
