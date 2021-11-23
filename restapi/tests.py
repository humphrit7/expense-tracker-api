from datetime import datetime

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

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
        self.assertEqual(float(json_result["amount"]), payload["amount"])
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
