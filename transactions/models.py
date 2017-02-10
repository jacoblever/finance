from django.db import models

types = (('CurrentAccount', 'Current Account'),
    ('ISA', 'ISA'),
    ('CreditCard', 'Credit Card'),)

class BankAccount(models.Model):
    AccountHumanName = models.CharField(max_length=140)
    AccountType = models.CharField(max_length=140, choices=types)
    AccountNumber = models.CharField(
        max_length=8,
        null=True,
        blank=True,)
    SortCode = models.CharField(
        max_length=8,
        null=True,
        blank=True,)
    IsActive = models.BooleanField()

    ColumnDate = models.CharField(max_length=100)
    ColumnDescription = models.CharField(max_length=100)
    ColumnAmount = models.CharField(max_length=100)
    ColumnCurrentBalance = models.CharField(max_length=100)
    ColumnOtherDate1 = models.CharField(max_length=100)
    ColumnOtherString1 = models.CharField(max_length=100)

    OtherDate1Name = models.CharField(
        max_length=100,
        null=True,
        blank=True,)
    OtherString1Name = models.CharField(
        max_length=100,
        null=True,
        blank=True,)

    def __str__(self):
        return self.AccountHumanName

class TransactionLabel(models.Model):

    Name = models.CharField(max_length=255)

    def __str__(self):
        return self.Name

    @classmethod
    def create(cls, name, thisId = None):
        label = cls()
        label.Name = name
        if thisId is not None:
            label.id = thisId
        return label

class BankTransaction(models.Model):
    Account = models.ForeignKey(
        BankAccount,
        on_delete=models.CASCADE,
    )
    Date = models.DateField()
    Description  = models.CharField(max_length=255)
    Amount = models.DecimalField(max_digits=10, decimal_places=2)
    CurrentBalance = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,)
    Label = models.ForeignKey(
        TransactionLabel,
        null=True,
        blank=True,
        on_delete=models.PROTECT,
    )
    DateUploaded = models.DateTimeField()
    Notes = models.CharField(
        max_length=255,
        null=True,
        blank=True,)
    OtherDate1 = models.DateField(
        null=True,
        blank=True,)
    OtherString1 = models.CharField(
        max_length=255,
        null=True,
        blank=True,)

    def __str__(self):
        return self.Description
