import logging

from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Category, Keyword, Merchant, Transaction
from .serializers import (
    CategorySerializer,
    KeywordSerializer,
    MerchantSerializer,
    TransactionBulkSerializer,
    TransactionResponseSerializer,
    TransactionSerializer,
)

logger = logging.getLogger(__name__)


class CategoryAPIView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, *args, **kwargs):
        content = list(Category.objects.all().values())
        return Response(content)

    @extend_schema(
        request=CategorySerializer,
    )
    def post(self, request, *args, **kwargs):
        content = {}
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(content, status=status.HTTP_201_CREATED)
        content["error"] = serializer.errors
        logger.warning("CategoryAPIView.post() -> errores al guardar la categoría:")
        logger.warning(serializer.errors)
        return Response(content, status=status.HTTP_400_BAD_REQUEST)


class CategoryIdAPIView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, *args, **kwargs):
        category = get_object_or_404(Category, pk=kwargs["category_id"])
        content = CategorySerializer(category).data
        return Response(content)

    @extend_schema(
        request=CategorySerializer(edit=True),
    )
    def patch(self, request, *args, **kwargs):
        content = {}
        category = get_object_or_404(Category, pk=kwargs["category_id"])
        serializer = CategorySerializer(category, data=request.data, edit=True, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(content, status=status.HTTP_200_OK)
        content["error"] = serializer.errors
        logger.warning("CategoryIdAPIView.post() -> errores al modificar la categoría:")
        logger.warning(serializer.errors)
        return Response(content, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        category = get_object_or_404(Category, pk=kwargs["category_id"])
        category.delete()
        return Response({})


class MerchantAPIView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, *args, **kwargs):
        content = list(Merchant.objects.all().values())
        return Response(content)

    @extend_schema(
        request=MerchantSerializer,
    )
    def post(self, request, *args, **kwargs):
        content = {}
        serializer = MerchantSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(content, status=status.HTTP_201_CREATED)
        content["error"] = serializer.errors
        logger.warning("MerchantAPIView.post() -> errores al guardar el comercio:")
        logger.warning(serializer.errors)
        return Response(content, status=status.HTTP_400_BAD_REQUEST)


class MerchantIdAPIView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, *args, **kwargs):
        merchant = get_object_or_404(Merchant, pk=kwargs["merchant_id"])
        content = MerchantSerializer(merchant).data
        return Response(content)

    @extend_schema(
        request=MerchantSerializer(edit=True),
    )
    def patch(self, request, *args, **kwargs):
        content = {}
        merchant = get_object_or_404(Merchant, pk=kwargs["merchant_id"])
        serializer = MerchantSerializer(merchant, data=request.data, edit=True, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(content, status=status.HTTP_200_OK)
        content["error"] = serializer.errors
        logger.warning("MerchantIdAPIView.patch() -> errores al modificar el comercio:")
        logger.warning(serializer.errors)
        return Response(content, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        merchant = get_object_or_404(Merchant, pk=kwargs["merchant_id"])
        merchant.delete()
        return Response({})


class KeywordAPIView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, *args, **kwargs):
        content = list(Keyword.objects.all().values())
        return Response(content)

    @extend_schema(
        request=KeywordSerializer,
    )
    def post(self, request, *args, **kwargs):
        content = {}
        serializer = KeywordSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(content, status=status.HTTP_201_CREATED)
        content["error"] = serializer.errors
        logger.warning("KeywordAPIView.post() -> errores al guardar una keyword:")
        logger.warning(serializer.errors)
        return Response(content, status=status.HTTP_400_BAD_REQUEST)


class KeywordIdAPIView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, *args, **kwargs):
        keyword = get_object_or_404(Keyword, pk=kwargs["keyword_id"])
        content = KeywordSerializer(keyword).data
        return Response(content)

    def delete(self, request, *args, **kwargs):
        keyword = get_object_or_404(Keyword, pk=kwargs["keyword_id"])
        keyword.delete()
        return Response({})


class TransactionBulkAPIView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, *args, **kwargs):
        content = list(Transaction.objects.all().values())
        return Response(content)

    @extend_schema(
        request=TransactionBulkSerializer,
        responses={201: TransactionResponseSerializer},
    )
    def post(self, request, *args, **kwargs):
        content = {}
        serializer = TransactionBulkSerializer(data=request.data)
        if serializer.is_valid():
            content = serializer.save()
            return Response(content, status=status.HTTP_201_CREATED)
        content["error"] = serializer.errors
        logger.warning("TransactionBulkAPIView.post() -> errores al guardar las transacciones:")
        logger.warning(serializer.errors)
        return Response(content, status=status.HTTP_400_BAD_REQUEST)


class TransactionIdAPIView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, *args, **kwargs):
        transaction = get_object_or_404(Transaction, pk=kwargs["transaction_id"])
        content = TransactionSerializer(transaction).data
        return Response(content)

    def delete(self, request, *args, **kwargs):
        transaction = get_object_or_404(Transaction, pk=kwargs["transaction_id"])
        transaction.delete()
        return Response({})
