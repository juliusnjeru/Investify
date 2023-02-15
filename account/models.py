from django.contrib.auth.models import User
from django.db import models
from datetime import datetime, timedelta


class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=19, decimal_places=2, default=0)
    last_deposit_date = models.DateField(null=True, blank=True)
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0.05)

    def deposit(self, amount):
        self.balance += amount
        self.last_deposit_date = datetime.now().date()
        self.save()

    def withdraw(self, amount):
        self.balance -= amount
        today = datetime.now().date()
        if self.last_deposit_date and self.last_deposit_date == today:
            self.last_deposit_date = None
        self.save()

    def add_interest(self):
        if self.last_deposit_date:
            days_since_last_deposit = (datetime.now().date() - self.last_deposit_date).days
            interest = (self.balance * self.interest_rate) * days_since_last_deposit
            self.balance += interest
            self.last_deposit_date = datetime.now().date()
        self.save()

    def __str__(self):
        return f"{self.user.username} - {self.balance}"


class Record(models.Model):
    TRANSACTION_TYPE_CHOICES = [
        ('Deposit', 'Deposit'),
        ('Withdraw', 'Withdraw'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_time = models.DateTimeField(auto_now_add=True)
    amount = models.DecimalField(max_digits=19, decimal_places=2)
    transaction_type = models.CharField(max_length=8, choices=TRANSACTION_TYPE_CHOICES)
    description = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.user.username} - {self.transaction_type} - {self.amount}"
