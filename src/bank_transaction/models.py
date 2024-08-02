from uuid import uuid4

from django.db import models


class Category(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4)
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=100, choices=(("expense", "expense"), ("income", "income")))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = (("name", "type"),)


class Merchant(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4)
    merchant_name = models.CharField(max_length=100)
    merchant_logo = models.URLField(max_length=255, blank=True, null=True)
    category = models.ForeignKey(Category, models.DO_NOTHING, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = (("merchant_name", "category"),)


class Keyword(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4)
    keyword = models.CharField(max_length=100)
    merchant = models.ForeignKey(Merchant, models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = (("keyword", "merchant"),)


class Transaction(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4)
    description = models.CharField(max_length=255)
    amount = models.FloatField(blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    merchant = models.ForeignKey(Merchant, models.DO_NOTHING, blank=True, null=True)
    category = models.ForeignKey(Category, models.DO_NOTHING, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
