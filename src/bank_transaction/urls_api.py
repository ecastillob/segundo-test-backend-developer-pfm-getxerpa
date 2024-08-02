# -*- coding: utf-8 -*-
from django.urls import path

from . import viewsets

urlpatterns = [
    path("category", viewsets.CategoryAPIView.as_view(), name="category-api"),
    path("category/<uuid:category_id>/", viewsets.CategoryIdAPIView.as_view(), name="category-id-api"),
    path("merchant", viewsets.MerchantAPIView.as_view(), name="merchant-api"),
    path("merchant/<uuid:merchant_id>/", viewsets.MerchantIdAPIView.as_view(), name="merchant-id-api"),
    path("keyword", viewsets.KeywordAPIView.as_view(), name="keyword-api"),
    path("keyword/<uuid:keyword_id>/", viewsets.KeywordIdAPIView.as_view(), name="keyword-id-api"),
    path("transaction", viewsets.TransactionBulkAPIView.as_view(), name="transaction-bulk-api"),
    path("transaction/<uuid:transaction_id>/", viewsets.TransactionIdAPIView.as_view(), name="transaction-id-api"),
]
