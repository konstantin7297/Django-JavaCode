from rest_framework import serializers
from .models import Wallet


class OperationWalletSerializer(serializers.Serializer):
    """ Serializer for the operation data validation """
    valletId = serializers.UUIDField()
    operationType = serializers.ChoiceField(choices=['DEPOSIT', 'WITHDRAW'])
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)


class WalletSerializer(serializers.ModelSerializer):
    """ Serializer for the wallet model validation """
    class Meta:
        model = Wallet
        fields = '__all__'


class UUIDSerializer(serializers.Serializer):
    """ Serializer for the wallet UUID validation """
    WALLET_UUID = serializers.UUIDField()
