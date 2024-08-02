import logging

from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import CategorySerializer, KeywordSerializer, MerchantSerializer, TransactionBulkSerializer

logger = logging.getLogger(__name__)


class CategoryAPIView(APIView):
    permission_classes = (AllowAny,)

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


class MerchantAPIView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        content = {}
        serializer = MerchantSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(content, status=status.HTTP_201_CREATED)
        content["error"] = serializer.errors
        logger.warning("MerchantAPIView.post() -> errores al guardar la categoría:")
        logger.warning(serializer.errors)
        return Response(content, status=status.HTTP_400_BAD_REQUEST)


class KeywordAPIView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        content = {}
        serializer = KeywordSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(content, status=status.HTTP_201_CREATED)
        content["error"] = serializer.errors
        logger.warning("KeywordAPIView.post() -> errores al guardar la categoría:")
        logger.warning(serializer.errors)
        return Response(content, status=status.HTTP_400_BAD_REQUEST)


class TransactionBulkAPIView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        content = {}
        serializer = TransactionBulkSerializer(data=request.data)
        if serializer.is_valid():
            content = serializer.save()
            return Response(content, status=status.HTTP_201_CREATED)
        content["error"] = serializer.errors
        logger.warning("TransactionBulkAPIView.post() -> errores al guardar la categoría:")
        logger.warning(serializer.errors)
        return Response(content, status=status.HTTP_400_BAD_REQUEST)
