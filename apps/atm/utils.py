from apps.atm.models import Deposit


def get_banknotes(currency, amount):
    deposit = Deposit.objects.filter(currency=currency, quantity__gt=0).order_by('-value')

    result = []

    for item in deposit:
        if amount >= item.value:
            quantity = amount // item.value
            if quantity > item.quantity:
                quantity = item.quantity

            amount = amount - quantity * item.value

            result.append(
                {
                    'value': item.value,
                    'quantity': quantity
                }
            )

    return result, amount
