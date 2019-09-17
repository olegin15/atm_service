from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from apps.atm.models import Deposit, RUB, USD, Transaction, DEPOSIT, WITHDRAW


class TestDepositView(TestCase):
    def test_success_deposit(self):
        client = APIClient()
        url = reverse('atm:deposit')

        data = {
            'currency': 'RUB',
            'value': 100,
            'quantity': 10}

        response = client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED,
                         response.data)

        self.assertEqual(response.data['success'], True)

        deposits = Deposit.objects.all()

        self.assertEqual(len(deposits), 1)

        self.assertEqual(deposits[0].currency, data['currency'])
        self.assertEqual(deposits[0].value, data['value'])
        self.assertEqual(deposits[0].quantity, data['quantity'])

        transactions = Transaction.objects.all()
        self.assertEqual(len(transactions), 1)

        self.assertEqual(transactions[0].currency, data['currency'])
        self.assertEqual(transactions[0].transaction_type, DEPOSIT)

        details = transactions[0].details.all()
        self.assertEqual(len(details), 1)

        self.assertEqual(details[0].value, data['value'])
        self.assertEqual(details[0].quantity, data['quantity'])

    def test_fail_deposit(self):
        client = APIClient()
        url = reverse('atm:deposit')

        data = {
            'currency': 'USB',
            'value': 100,
            'quantity': -5}

        response = client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST,
                         response.data)


class WithdrawView(TestCase):
    def test_success_withdraw(self):
        client = APIClient()
        url = reverse('atm:withdraw')

        Deposit.objects.create(currency=RUB, value=1000, quantity=10)
        Deposit.objects.create(currency=RUB, value=100, quantity=5)
        Deposit.objects.create(currency=RUB, value=10, quantity=500)
        Deposit.objects.create(currency=RUB, value=2, quantity=1000)
        Deposit.objects.create(currency=USD, value=100, quantity=20)

        data = {
            'currency': 'RUB',
            'amount': 3522
        }

        response = client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK,
                         response.data)

        self.assertEqual(response.data['success'], True)

        result = response.data['result']

        self.assertEqual(result[0]['value'], 1000)
        self.assertEqual(result[0]['quantity'], 3)

        self.assertEqual(result[1]['value'], 100)
        self.assertEqual(result[1]['quantity'], 5)

        self.assertEqual(result[2]['value'], 10)
        self.assertEqual(result[2]['quantity'], 2)

        self.assertEqual(result[3]['value'], 2)
        self.assertEqual(result[3]['quantity'], 1)

        deposit = Deposit.objects.get(currency=RUB, value=1000)
        self.assertEqual(deposit.quantity, 7)

        deposit = Deposit.objects.get(currency=RUB, value=100)
        self.assertEqual(deposit.quantity, 0)

        deposit = Deposit.objects.get(currency=RUB, value=10)
        self.assertEqual(deposit.quantity, 498)

        deposit = Deposit.objects.get(currency=RUB, value=2)
        self.assertEqual(deposit.quantity, 999)

        transactions = Transaction.objects.all()
        self.assertEqual(len(transactions), 1)

        self.assertEqual(transactions[0].currency, data['currency'])
        self.assertEqual(transactions[0].transaction_type, WITHDRAW)

        details = transactions[0].details.all()
        self.assertEqual(len(details), 4)

        self.assertEqual(details[0].value, 1000)
        self.assertEqual(details[0].quantity, 3)

        self.assertEqual(details[1].value, 100)
        self.assertEqual(details[1].quantity, 5)

        self.assertEqual(details[2].value, 10)
        self.assertEqual(details[2].quantity, 2)

        self.assertEqual(details[3].value, 2)
        self.assertEqual(details[3].quantity, 1)

    def test_fail_withdraw(self):
        client = APIClient()
        url = reverse('atm:withdraw')

        Deposit.objects.create(currency=RUB, value=1000, quantity=2)
        Deposit.objects.create(currency=RUB, value=100, quantity=5)
        Deposit.objects.create(currency=RUB, value=10, quantity=500)
        Deposit.objects.create(currency=RUB, value=2, quantity=1000)
        Deposit.objects.create(currency=USD, value=100, quantity=20)

        data = {
            'currency': 'RUB',
            'amount': 9522
        }

        response = client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST,
                         response.data)
