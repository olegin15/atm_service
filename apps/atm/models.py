from django.db import models
from django.utils.translation import ugettext_lazy as _

RUB = 'RUB'
USD = 'USD'
EUR = 'EUR'

CURRENCY_CHOICES = [
    (RUB, 'Ruble'),
    (USD, 'US Dollar'),
    (EUR, 'Euro'),
]

DEPOSIT = 1
WITHDRAW = 2

TRANSACTION_CHOICES = [
    (DEPOSIT, 'Deposit'),
    (WITHDRAW, 'Withdraw'),
]


class BaseTimestampModel(models.Model):
    """
    Timestamp model
    """
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Deposit(BaseTimestampModel):
    """
    Код валюты
    """
    currency = models.CharField(
        verbose_name=_('Currency'),
        max_length=3,
        choices=CURRENCY_CHOICES
    )

    """
    Номинал купюры
    """
    value = models.PositiveIntegerField(
        verbose_name=_('Value'),
    )

    """
    Количество купюр
    """
    quantity = models.PositiveIntegerField(
        verbose_name=_('Quantity'),
    )


class Transaction(BaseTimestampModel):
    """
    Тип транзакции
    """
    transaction_type = models.PositiveSmallIntegerField(
        verbose_name=_('Transaction Type'),
        choices=TRANSACTION_CHOICES
    )

    """
    Код валюты
    """
    currency = models.CharField(
        verbose_name=_('Currency'),
        max_length=3,
        choices=CURRENCY_CHOICES
    )


class TransactionDetail(BaseTimestampModel):
    """
    Транзакция
    """
    transaction = models.ForeignKey(Transaction,
                                    on_delete=models.PROTECT,
                                    verbose_name=_('Transaction detail'),
                                    related_name='details')

    """
    Номинал купюры
    """
    value = models.PositiveIntegerField(
        verbose_name=_('Value'),
    )

    """
    Количество купюр
    """
    quantity = models.PositiveIntegerField(
        verbose_name=_('Quantity'),
    )
