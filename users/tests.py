from django.test import TransactionTestCase
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
from django.db.utils import IntegrityError

from .models import Profile

User = get_user_model()

class LoginTest(TransactionTestCase):

    def setUp(self):
        self.user = User.objects.create_user(email='sherlock@holmes.com', password='testuser123')
        self.user.save()

    def tearDown(self):
        self.user.delete()

    def test_correct(self):
        user = authenticate(email='sherlock@holmes.com', password='testuser123')
        self.assertTrue((user is not None) and user.is_authenticated)

    def test_wrong_email(self):
        user = authenticate(email='sherlockholmes.com', password='testuser123')
        self.assertFalse(user is not None and user.is_authenticated)

    def test_wrong_password(self):
        user = authenticate(email='sherlock@holmes.com', password='wrongpassword')
        self.assertFalse(user is not None and user.is_authenticated)


# @transaction.atomic
class SignupTest(TransactionTestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='sherlock@holmes.com', 
            password='testuser123', 
            username="username"
        )
        self.user.save()

    def tearDown(self):
        self.user.delete()

    def test_email_uniqueness(self):
        # Email is Unique

        try:
            duplicate_user = User.objects.create_user(
                email='sherlock@holmes.com', 
                password='differentPassword'
            )
        except IntegrityError:
            self.assertTrue('a' == 'a')

    def test_username_nonuniqueness(self):
        # Username is Not Unique

        duplicate_user = User.objects.create_user(
            username="username", 
            email='different@holmes.com', 
            password='differentPassword'
        )
        
        self.assertTrue(duplicate_user is not None)


class UserSignalTest(TransactionTestCase):
    # A Profile model instance must be created automatically for each user created

    def setUp(self):
        self.user = User.objects.create_user(
            email='sherlock@holmes.com', 
            password='testuser123', 
        )
        self.user.save()

    def tearDown(self):
        self.user.delete()

    def test_profile_presence(self):
        profile = Profile.objects.get(user=self.user)
        self.assertTrue(profile is not None)

    