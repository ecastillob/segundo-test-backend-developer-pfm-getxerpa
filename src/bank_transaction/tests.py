import json
from pathlib import Path

from django.urls import reverse
from rest_framework.test import APISimpleTestCase

from .models import Category, Keyword, Merchant, Transaction


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


class T3GetModifyDeleteEntitiesTest(BaseTest):

    def test_01_get_entities(self):
        for url in [
            reverse("category-api"),
            reverse("merchant-api"),
            reverse("keyword-api"),
            reverse("transaction-bulk-api"),
        ]:
            response = self.client.get(url, {}, format="json")
            self.assertEqual(response.status_code, 200)
            self.assertTrue(len(response.json()) > 0)
        category_id = Category.objects.all()[0].id
        merchant_id = Merchant.objects.all()[1].id
        keyword_id = Keyword.objects.all()[0].id
        transaction_id = Transaction.objects.all()[0].id
        for object_id, url in [
            [category_id, reverse("category-id-api", kwargs={"category_id": category_id})],
            [merchant_id, reverse("merchant-id-api", kwargs={"merchant_id": merchant_id})],
            [keyword_id, reverse("keyword-id-api", kwargs={"keyword_id": keyword_id})],
            [transaction_id, reverse("transaction-id-api", kwargs={"transaction_id": transaction_id})],
        ]:
            response = self.client.get(url, {}, format="json")
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json()["id"], str(object_id))

    def test_02_patch_entities(self):
        # modify category
        url = reverse("category-id-api", kwargs={"category_id": Category.objects.all()[0].id})
        body = {"name": "nuevo nombre"}
        response = self.client.patch(url, body, format="json")
        self.assertEqual(response.status_code, 200)
        # modify merchant
        url = reverse("merchant-id-api", kwargs={"merchant_id": Merchant.objects.all()[1].id})
        body = {"merchant_logo": "http://unaurl.cl"}
        response = self.client.patch(url, body, format="json")
        self.assertEqual(response.status_code, 200)

    def test_03_patch_entities(self):
        # modify category
        url = reverse("category-id-api", kwargs={"category_id": Category.objects.all()[0].id})
        body = {"name": "nuevo nombre" * 100}
        response = self.client.patch(url, body, format="json")
        self.assertEqual(response.status_code, 400)
        # modify merchant
        url = reverse("merchant-id-api", kwargs={"merchant_id": Merchant.objects.all()[1].id})
        body = {"merchant_logo": "unaurlinvalida"}
        response = self.client.patch(url, body, format="json")
        self.assertEqual(response.status_code, 400)

    def test_04_delete_entities(self):
        for url in [
            reverse("category-id-api", kwargs={"category_id": Category.objects.all()[0].id}),
            reverse("merchant-id-api", kwargs={"merchant_id": Merchant.objects.all()[1].id}),
            reverse("keyword-id-api", kwargs={"keyword_id": Keyword.objects.all()[0].id}),
            reverse("transaction-id-api", kwargs={"transaction_id": Transaction.objects.all()[0].id}),
        ]:
            response = self.client.delete(url, {}, format="json")
            self.assertEqual(response.status_code, 200)
