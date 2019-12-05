from django.test import TestCase, Client
from users.models import CustomUser
from users.views import is_valid_uuid
from uuid import uuid4


class ParentAccessLoggedinTest(TestCase):

    def setUp(self):
        """
        setup for testing logged in user
        """
        self.user = CustomUser(
            first_name='UserA', email='private@gmail.com')
        self.user.save()
        self.second_user = CustomUser(
            first_name='UserB',
            email='public@gmail.com',
            parental_key='test-key'
        )
        # self.second_user.save()
        # login
        self.client = Client()
        self.client.force_login(user=self.user)

    def test_index(self):
        """
        user can get to index with code 200
        """
        response = self.client.get(path='')
        status_code = response.status_code
        self.assertEqual(status_code, 200)

    def test_get_request_page(self):
        """
        test if logged in user can get to request page
        """
        response = self.client.get(path='')
        status_code = response.status_code
        self.assertEqual(status_code, 200)

    def test_post_valid_uuid_request_page(self):
        """
        test if logged in user can post to request page
        """
        response = self.client.post(
            path='/users/request_user/',
            data={'uuid': self.second_user.parental_key},
            follow=True)
        status_code = response.status_code
        self.assertEqual(status_code, 200)

    def test_post_invalid_uuid_request_page(self):
        """
        test if logged in user can post to request page
        """
        response = self.client.post(
            path='/users/request_user/',
            data={'uuid': 'totally-valid-uuid4'},
        )
        status_code = response.status_code
        self.assertEqual(status_code, 302)


class ParentAccessNotLoggedinTest(TestCase):

    def setUp(self):
        """
        setup for testing not logged in user
        """
        self.client = Client()

    def test_index(self):
        """
        not logged in user can get to index with code 200
        """
        response = self.client.get(path='')
        status_code = response.status_code
        self.assertEqual(status_code, 200)

    def test_get_request_page(self):
        """
        test if logged in not logged in user can't get to request page
        -> get redirected to index page
        """
        response = self.client.get(path='/users/request_user/')
        status_code = response.status_code
        self.assertEqual(status_code, 302)

    def test_post_request_page(self):
        """
        test if logged in not logged in user can't post to request page
        -> get redirected to index page
        """
        response = self.client.post(
            path='/users/request_user/',
            data={'uuid': 'totally-valid-uuid4'})
        status_code = response.status_code
        self.assertEqual(status_code, 302)


class is_valid_uuidTest(TestCase):
    def setUp(self):
        pass

    def test_random_string(self):
        self.case = "asdasdasd"
        self.assertFalse(is_valid_uuid(self.case))

    def test_random_number(self):
        self.case = 123123123
        with self.assertRaises(TypeError):
            is_valid_uuid(self.case)

    def test_random_number_to_str(self):
        self.case = 123123123
        self.assertFalse(is_valid_uuid(str(self.case)))
