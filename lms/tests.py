from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.db.models import Count
from django.contrib.auth.models import User
from lms.models import Product, Lesson, Subscription
from lms.serializers import ProductSerializer, LessonSerializer


class ProductStatisticsAPITest(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.user1 = User.objects.create(username="user1")
        self.user2 = User.objects.create(username="user2")
        self.product = Product.objects.create(
            name="Test Product",
            author=self.user1,
            price=500,
            min_group_size=2,
            max_group_size=5,
        )

        self.lesson1 = Lesson.objects.create(name="Lesson 1", product=self.product)
        self.lesson2 = Lesson.objects.create(name="Lesson 2", product=self.product)

        self.subscription1 = Subscription.objects.create(
            user=self.user1, product=self.product
        )
        self.subscription2 = Subscription.objects.create(
            user=self.user2, product=self.product
        )

    def test_get_product_statistics(self):
        url = "/api/products/statistics/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertIn("results", response.data)
        self.assertNotEqual(len(response.data["results"]), 0)
        first_product = response.data["results"][0]
        self.assertIn("id", first_product)
        self.assertIn("name", first_product)
        self.assertIn("students_count", first_product)
        self.assertIn("groups_fill_percentage", first_product)
        self.assertIn("purchase_percentage", first_product)


class ProductListAPITest(APITestCase):

    def setUp(self):
        self.client = APIClient()

    def test_get_product_list(self):
        url = "/api/product-lst/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        products = Product.objects.annotate(lessons_count=Count("lessons")).order_by(
            "-date_start"
        )
        serializer = ProductSerializer(products, many=True)
        self.assertEqual(response.data["results"], serializer.data)


class ProductLessonsAPITest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user1 = User.objects.create(username="user1")
        self.product = Product.objects.create(
            name="Test Product",
            author=self.user1,
            price=500,
            min_group_size=2,
            max_group_size=5,
        )

    def test_get_product_lessons(self):
        url = f"/api/product-lessons/{self.product.id}/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        lessons = self.product.lessons.all()
        serializer = LessonSerializer(lessons, many=True)
        self.assertEqual(response.data, {"lessons": serializer.data})

    def test_get_non_existent_product_lessons(self):
        non_existent_id = 999
        url = f"/api/product-lessons/{non_existent_id}/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
