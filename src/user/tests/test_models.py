from django.test import TestCase
from django.contrib.auth import get_user_model


class UserModelTests(TestCase):
    def test_create_user_with_email_successful(self):
        email = 'user_1@test.com'
        password = 'test_passwd'
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        # assert
        # assert user.email == email
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalize(self):
        email = 'user_1@TEST.com'
        user = get_user_model().objects.create_user(
            email=email,
            password='password123'
        )

        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(
                email=None,
                password='password123'
            )
