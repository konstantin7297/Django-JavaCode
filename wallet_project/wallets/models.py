from decimal import Decimal

from django.db import models
from django.db import transaction
from uuid import UUID


class Wallet(models.Model):
    """ Table model for wallet operations """
    id = models.UUIDField(
        primary_key=True,
        default=UUID('00000000-0000-0000-0000-000000000000'),
    )
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    @transaction.atomic
    def deposit(self, amount: Decimal):
        wallet = Wallet.objects.select_for_update().get(pk=self.id)
        wallet.balance += Decimal(amount)
        wallet.save()
        return wallet

    @transaction.atomic
    def withdraw(self, amount: Decimal):
        wallet = Wallet.objects.select_for_update().get(pk=self.id)

        if wallet.balance < Decimal(amount):
            raise ValueError("Insufficient funds")

        wallet.balance -= Decimal(amount)
        wallet.save()
        return wallet
