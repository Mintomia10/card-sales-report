from django.db import models


class CardSale(models.Model):

    OPERATOR_CHOICES = [
        ('MD. Minto Mia', 'MD. Minto Mia'),
        ('Sompa Rani', 'Sompa Rani'),
        ('Proxy Operator', 'Proxy Operator'),
    ]

    TYPE_CHOICES = [
        ('Sale', 'Card Sale'),
        ('Replace', 'Replace'),
        ('Damage', 'Damage'),
    ]

    operator_name = models.CharField(
        max_length=100,
        choices=OPERATOR_CHOICES
    )

    transaction_type = models.CharField(
        max_length=20,
        choices=TYPE_CHOICES
    )

    card_quantity = models.PositiveIntegerField(default=1)

    price_per_card = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=50
    )

    total_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    date = models.DateField(auto_now_add=True)

    time = models.TimeField(auto_now_add=True)

    def save(self, *args, **kwargs):

        if self.transaction_type == 'Damage':
            self.price_per_card = 0
        else:
            self.price_per_card = 50

        self.total_amount = self.card_quantity * self.price_per_card

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.operator_name} - {self.transaction_type} - {self.card_quantity}"
# Create your models here.
