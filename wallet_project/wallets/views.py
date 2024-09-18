from django.http import HttpResponseNotFound
from django_ratelimit.decorators import ratelimit
from rest_framework import status
from rest_framework.exceptions import NotFound, ValidationError
from rest_framework.generics import GenericAPIView
from rest_framework.request import Request
from rest_framework.response import Response

from .models import Wallet
from .serializers import OperationWalletSerializer, WalletSerializer, UUIDSerializer


def page_not_fount(request, exception):
    """ Основная функция для отображения при ошибке 404. Заглушка для Debug = off """
    return HttpResponseNotFound("<h1>Page not found</h1>")


class WalletView(GenericAPIView):
    """ Updating balance from wallet """

    @staticmethod
    @ratelimit(key='post:valletId', rate='1000/s', block=True)
    def post(request: Request, *args, **kwargs) -> Response:
        try:
            serializer = OperationWalletSerializer(data=request.data)

            if serializer.is_valid():
                wallet = Wallet.objects.get(id=serializer.data.get("valletId"))

                if wallet:

                    if serializer.data.get("operationType").strip().upper() == "DEPOSIT":
                        updated_wallet = wallet.deposit(serializer.data.get("amount"))
                    elif serializer.data.get("operationType").strip().upper() == "WITHDRAW":
                        updated_wallet = wallet.withdraw(serializer.data.get("amount"))
                    else:
                        raise NotFound('Invalid operationType')

                    return Response(
                        WalletSerializer(updated_wallet).data,
                        status=status.HTTP_200_OK,
                    )

                wallet.DoesNotExist('Wallet does not exist')
            raise ValidationError(serializer.errors)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class BalanceView(GenericAPIView):
    """ Getting balance from wallet """

    @staticmethod
    @ratelimit(key='get:WALLET_UUID', rate='1000/s', block=True)
    def get(request: Request, *args, **kwargs) -> Response:
        try:
            serializer = UUIDSerializer(data=kwargs)

            if serializer.is_valid():
                wallet = Wallet.objects.get(id=serializer.data.get("WALLET_UUID"))

                if wallet:
                    return Response(
                        WalletSerializer(wallet).data,
                        status=status.HTTP_200_OK,
                    )

                raise wallet.DoesNotExist('Wallet does not exist')
            raise ValidationError(serializer.errors)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
