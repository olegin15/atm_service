from django.db import transaction
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response

from apps.atm.serializers import DepositSerializer, WithdrawSerializer


class DepositView(CreateAPIView):
    """
    Принять в банкомат несколько монет/купюр
    """
    serializer_class = DepositSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response({"success": True}, status=status.HTTP_201_CREATED)


class WithdrawView(CreateAPIView):
    """
    Выдать из банкомата определенную сумму денег в определенной валюте
    """
    serializer_class = WithdrawSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        with transaction.atomic():
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            return Response({'success': True, 'result': serializer.banknotes}, status=status.HTTP_200_OK)

