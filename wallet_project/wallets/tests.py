from django.test import TestCase
from django.urls import reverse
from rest_framework import status

from rest_framework.test import RequestsClient

from .models import Wallet, Decimal


class WalletTestCase(TestCase):
    """ Testing REST API endpoints """
    @classmethod
    def setUpTestData(cls):
        cls.url = 'http://testserver'
        cls.client = RequestsClient()

    def setUp(self):
        self.wallet, _ = Wallet.objects.get_or_create(
            id="00000000-0000-0000-0000-000000000000",
            balance=Decimal(1000),
        )

    def tearDown(self):
        self.wallet.delete()

    def test_wallet_post_deposit(self):
        url = self.url + reverse('wallets:wallet')
        data = {'valletId': self.wallet.id, 'operationType': "DEPOSIT", 'amount': 1000}

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        keys = response.json().keys()
        self.assertEqual(len(keys), 2)
        self.assertEqual(self.wallet.id, response.json().get("id"))
        self.assertEqual(
            Decimal(data.get("amount")) + self.wallet.balance,
            Decimal(response.json().get("balance")),
        )

    def test_wallet_post_withdraw(self):
        url = self.url + reverse('wallets:wallet')
        data = {'valletId': self.wallet.id, 'operationType': "WITHDRAW", 'amount': 1000}

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        keys = response.json().keys()
        self.assertEqual(len(keys), 2)
        self.assertEqual(self.wallet.id, response.json().get("id"))
        self.assertEqual(
            Decimal(self.wallet.balance) - data.get("amount"),
            Decimal(response.json().get("balance")),
        )

    def test_balance_get(self):
        url = self.url + reverse(
            'wallets:balance',
            kwargs={'WALLET_UUID': self.wallet.id},
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        keys = response.json().keys()
        self.assertEqual(len(keys), 2)
        self.assertEqual(self.wallet.id, response.json().get("id"))
        self.assertEqual(
            Decimal(self.wallet.balance),
            Decimal(response.json().get("balance")),
        )
