from datetime import datetime

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework_api_key.models import APIKey
from rest_framework.test import APIClient

from restapi import models


class TestModels(TestCase):
    def test_expense(self):
        expense = models.Expense.objects.create(
            amount=249.99,
            merchant="Amazon",
            description="anc headphones",
            category="music",
        )
        inserted_expense = models.Expense.objects.get(pk=expense.id)
        self.assertEqual(expense.amount, inserted_expense.amount)
        self.assertEqual(expense.merchant, inserted_expense.merchant)
        self.assertEqual(expense.description, inserted_expense.description)
        self.assertEqual(expense.category, inserted_expense.category)
        self.assertEqual(249.99, inserted_expense.amount)
        self.assertEqual("Amazon", inserted_expense.merchant)
        self.assertEqual("anc headphones", inserted_expense.description)
        self.assertEqual("music", inserted_expense.category)
        self.assertEqual(
            datetime.now(tz=timezone.utc).minute, inserted_expense.date_created.minute
        )
        self.assertEqual(
            datetime.now(tz=timezone.utc).minute, inserted_expense.date_updated.minute
        )


class TestViews(TestCase):
    def setUp(self):
        api_key, key = APIKey.objects.create_key(name="expense-service")
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION=f"Api-Key {key}")

    def test_expense_create(self):
        payload = {
            "amount": 50.0,
            "merchant": "AT&T",
            "description": "phone subscription",
            "category": "utilities",
        }
        result = self.client.post(
            reverse("restapi:expense-list-create"), payload, format="json"
        )
        self.assertEqual(201, result.status_code)
        json_result = result.json()
        self.assertEqual(json_result["amount"], payload["amount"])
        self.assertEqual(json_result["merchant"], payload["merchant"])
        self.assertEqual(json_result["description"], payload["description"])
        self.assertEqual(json_result["category"], payload["category"])
        self.assertIsInstance(json_result["id"], int)

    def test_expense_list(self):
        result = self.client.get(reverse("restapi:expense-list-create"), format="json")
        self.assertEqual(result.status_code, 200)
        json_result = result.json()
        self.assertIsInstance(json_result, list)
        expenses = models.Expense.objects.all()
        self.assertEqual(len(expenses), len(json_result))

    def test_expense_create_required_fields_missing(self):
        payload = {
            "merchant": "AT&T",
            "description": "phone subscription",
            "category": "utilities",
        }
        result = self.client.post(
            reverse("restapi:expense-list-create"), payload, format="json"
        )
        self.assertEqual(result.status_code, 400)

    def test_expense_retrieve(self):
        expense = models.Expense.objects.create(
            amount=300.0, merchant="George", description="loan", category="transfer"
        )
        result = self.client.get(
            reverse("restapi:expense-retrieve-delete", args=[expense.id]), format="json"
        )
        self.assertEqual(200, result.status_code)
        json_result = result.json()
        self.assertEqual(300.0, json_result["amount"])
        self.assertEqual("George", json_result["merchant"])
        self.assertEqual("loan", json_result["description"])
        self.assertEqual("transfer", json_result["category"])
        self.assertEqual(expense.id, json_result["id"])

    def test_expense_delete(self):
        expense = models.Expense.objects.create(
            amount=400.0, merchant="John", description="loan", category="transfer"
        )
        result = self.client.delete(
            reverse("restapi:expense-retrieve-delete", args=[expense.id]), format="json"
        )
        self.assertEqual(204, result.status_code)
        self.assertFalse(models.Expense.objects.filter(pk=expense.id).exists())

    def test_list_expense_filter_by_merchant(self):
        expense_john = models.Expense.objects.create(
            amount=400.0, merchant="John", description="loan", category="transfer"
        )
        expense_george = models.Expense.objects.create(
            amount=300.0, merchant="George", description="gift", category="card"
        )
        url = "/api/expenses?merchant=John"
        result = self.client.get(url, format="json")
        self.assertEqual(200, result.status_code)
        json_result = result.json()
        self.assertEqual(1, len(json_result))
        self.assertEqual(json_result[0]["amount"], expense_john.amount)
        self.assertEqual(json_result[0]["merchant"], expense_john.merchant)
        self.assertEqual(json_result[0]["description"], expense_john.description)
        self.assertEqual(json_result[0]["category"], expense_john.category)
