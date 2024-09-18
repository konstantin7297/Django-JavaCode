from django.urls import path

from .views import WalletView, BalanceView

app_name = 'wallets'

urlpatterns = [
    path('wallet/', WalletView.as_view(), name="wallet"),
    path('wallets/<uuid:WALLET_UUID>/', BalanceView.as_view(), name="balance"),
]
