# -*- coding: utf-8 -*-
from django.urls import path

from . import viewsets

urlpatterns = [
    path("category", viewsets.CategoryAPIView.as_view(), name="category-api"),
    path("merchant", viewsets.MerchantAPIView.as_view(), name="merchant-api"),
    path("keyword", viewsets.KeywordAPIView.as_view(), name="keyword-api"),
    path("transaction", viewsets.TransactionBulkAPIView.as_view(), name="transaction-bulk-api"),
]
