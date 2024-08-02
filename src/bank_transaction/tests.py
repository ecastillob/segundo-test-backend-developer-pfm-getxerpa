import json
from pathlib import Path

from django.urls import reverse
from rest_framework.test import APISimpleTestCase


class BaseTest(APISimpleTestCase):
    databases = "__all__"

    def load_filecontent(self, filename: str):
        fixture_folder = Path(__file__).resolve().parent / "fixtures"
        with open(fixture_folder / filename, encoding="utf8") as file:
            examples = json.load(file)
        return examples


class T1CreateEntitiesTest(BaseTest):

    def test_01_add_categories(self):
        url = reverse("category-api")
        for body in self.load_filecontent("categories.json"):
            response = self.client.post(url, body, format="json")
            self.assertEqual(response.status_code, 201)

    def test_02_try_to_add_invalid_categories(self):
        url = reverse("category-api")
        for body in self.load_filecontent("categories.json"):
            response = self.client.post(url, body, format="json")
            self.assertEqual(response.status_code, 400)
        for payload in self.load_filecontent("invalid_categories.json"):
            response = self.client.post(url, payload["input"], format="json")
            self.assertEqual(response.status_code, 400)
            self.assertEqual(json.loads(response.content), payload["output"])

    def test_03_add_merchants(self):
        url = reverse("merchant-api")
        for body in self.load_filecontent("merchants.json"):
            response = self.client.post(url, body, format="json")
            self.assertEqual(response.status_code, 201)

    def test_04_try_to_add_invalid_merchants(self):
        url = reverse("merchant-api")
        for filename in ["merchants.json", "invalid_merchants.json"]:
            for body in self.load_filecontent(filename):
                response = self.client.post(url, body, format="json")
                self.assertEqual(response.status_code, 400)

    def test_05_add_keywords(self):
        url = reverse("keyword-api")
        for payload in self.load_filecontent("keywords.json"):
            response = self.client.post(url, payload["input"], format="json")
            self.assertEqual(response.status_code, 201)
            response = self.client.post(url, payload["input"], format="json")
            self.assertEqual(response.status_code, 400)


class T2CreateTransactionsTest(BaseTest):

    def test_01_add_transactions(self):
        url = reverse("transaction-bulk-api")
        for payload in self.load_filecontent("transactions.json"):
            response = self.client.post(url, payload["input"], format="json")
            self.assertEqual(response.status_code, 201)
            self.assertEqual(response.json(), payload["output"])

    def test_02_try_to_add_invalid_transactions(self):
        url = reverse("transaction-bulk-api")
        for payload in self.load_filecontent("invalid_transactions.json"):
            response = self.client.post(url, payload["input"], format="json")
            self.assertEqual(response.status_code, 400)
            self.assertEqual(response.json(), payload["output"])
