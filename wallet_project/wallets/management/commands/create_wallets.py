from django.core.management import BaseCommand
from django.db import transaction

from wallets.models import Wallet


class Command(BaseCommand):
    """ Creating several test wallets. """
    @transaction.atomic
    def handle(self, *args, **options):
        self.stdout.write("Creates wallets...")

        for i in range(1, 10):
            wallet, _ = Wallet.objects.get_or_create(
                id=f"00000000-0000-0000-0000-00000000000{i}",
            )
            self.stdout.write(f"Created wallet: {wallet.id}")

        self.stdout.write(self.style.SUCCESS("Wallets creating completed."))
