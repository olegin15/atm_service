# coding: utf-8
from django.db import transaction
from django.db.models import Sum, F
from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers

from apps.atm.models import Deposit, Transaction, DEPOSIT, TransactionDetail, WITHDRAW
from apps.atm.utils import get_banknotes


class DepositSerializer(serializers.ModelSerializer):
    class Meta:
        model = Deposit
        fields = ('currency', 'value', 'quantity')

    def validate_value(self, value):
        if value <= 0:
            raise serializers.ValidationError(_("Value must be more than zero"))
        return value

    def validate_quantity(self, value):
        if value <= 0:
            raise serializers.ValidationError(_("Quantity must be more than zero"))
        return value

    def create(self, validated_data):
        currency = validated_data['currency']
        value = validated_data['value']
        quantity = validated_data['quantity']

        with transaction.atomic():
            try:
                deposit = Deposit.objects.get(currency=currency,
                                              value=value)
                deposit.quantity += quantity
                deposit.save()
            except Deposit.DoesNotExist:
                deposit = Deposit.objects.create(currency=currency,
                                                 value=value,
                                                 quantity=quantity
                                                 )

            tran = Transaction.objects.create(transaction_type=DEPOSIT,
                                              currency=currency)

            TransactionDetail.objects.create(transaction=tran,
                                             value=value,
                                             quantity=quantity)

        return deposit


class WithdrawSerializer(serializers.ModelSerializer):
    amount = serializers.IntegerField(write_only=True)

    class Meta:
        model = Deposit
        fields = ('currency', 'amount')

    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError(_("Amount must be more than zero"))

        currency = self.initial_data['currency']
        total = Deposit.objects.filter(currency=currency).aggregate(total=Sum(F('value') * F('quantity')))['total'] or 0
        if total < value:
            raise serializers.ValidationError(_("Insufficient funds"))

        result, rest = get_banknotes(currency, value)

        if rest != 0:
            raise serializers.ValidationError(_("Can’t give change. Enter a different amount"))

        self.banknotes = result
        return value

    def create(self, validated_data):
        currency = validated_data['currency']
        banknotes = self.banknotes

        tran = Transaction.objects.create(transaction_type=WITHDRAW,
                                          currency=currency)
        for item in banknotes:
            deposit = Deposit.objects.get(currency=currency, value=item['value'])
            deposit.quantity -= item['quantity']
            deposit.save()

            TransactionDetail.objects.create(transaction=tran,
                                             value=item['value'],
                                             quantity=item['quantity'])

        return banknotes
