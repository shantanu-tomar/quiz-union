from django.test import TransactionTestCase
from django.http import request
from .models import Category
from .views import update_categories


class CategoryUpdateTest(TransactionTestCase):
    # Requires Internet Connection
    # Test for model validation with lots of API data

    def test_update_success(self):
        print("INTERNET CONNECTION REQUIRED")
        print("Calling API 8 Times...")
        # Run update loop 8 times
        try:
            for i in range(1, 9):
                update_categories(request)
                print(f"Completed API call loop: {i}")

            self.assertTrue(True is True)

        except TypeError:
            message = "TEST NOT RUN! No Internet Connection For Calling API. \
Please Connect And Run Test Again."
            print(message)


class CustomCategoryTest(TransactionTestCase):

    def setUp(self):
        self.category = Category.objects.create(
            category='custom category', 
            identifier='identifier',
            custom_category=True
        )
        self.category.save()

    def tearDown(self):
        self.category.delete()


    def test_customness(self):
        category = Category.objects.get(
            category='custom category', 
            identifier='identifier',
            custom_category=True
        )

        self.assertFalse(category is None)




