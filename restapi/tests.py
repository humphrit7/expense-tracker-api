from datetime import datetime

from django.test import TestCase
from django.utils import timezone

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
