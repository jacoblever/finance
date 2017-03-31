from django.db import models

types = (('CurrentAccount', 'Current Account'),
    ('ISA', 'ISA'),
    ('CreditCard', 'Credit Card'),)


class BankAccountTemplate(models.Model):
    name = models.CharField(max_length=140)
    is_built_in = models.BooleanField(
        default=False,
    )

    get_date = models.CharField(max_length=100)
    get_description = models.CharField(max_length=100)
    get_amount = models.CharField(max_length=100)

    get_current_balance = models.CharField(
        max_length=100,
        null=True,
        blank=True,
    )

    custom_date_1_name = models.CharField(
        max_length=100,
        null=True,
        blank=True,
    )
    get_custom_date_1 = models.CharField(
        max_length=100,
        null=True,
        blank=True,
    )

    custom_text_1_name = models.CharField(
        max_length=100,
        null=True,
        blank=True,
    )
    get_custom_text_1 = models.CharField(
        max_length=100,
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.name


class BankAccount(models.Model):
    name = models.CharField(max_length=140)
    account_type = models.CharField(max_length=140, choices=types)
    more_details = models.CharField(
        max_length=100,
        null=True,
        blank=True,
    )
    is_active = models.BooleanField(default=True)
    bank_account_template = models.ForeignKey(
        BankAccountTemplate,
        on_delete=models.PROTECT,
    )

    def __str__(self):
        return self.name


class TransactionLabel(models.Model):

    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    @classmethod
    def create(cls, name, id_ = None):
        label = cls()
        label.name = name
        if id_ is not None:
            label.id = id_
        return label


class Transaction(models.Model):
    bank_account = models.ForeignKey(
        BankAccount,
        on_delete=models.PROTECT,
    )
    date = models.DateField()
    description  = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    current_balance = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
    )
    transaction_label = models.ForeignKey(
        TransactionLabel,
        null=True,
        blank=True,
        on_delete=models.PROTECT,
    )
    date_imported = models.DateTimeField()
    notes = models.CharField(
        max_length=255,
        null=True,
        blank=True,
    )
    custom_date_1 = models.DateField(
        null=True,
        blank=True,
    )
    custom_text_1 = models.CharField(
        max_length=255,
        null=True,
        blank=True,
    )

    def __str__(self):
        return "{0}: {1} - {2}".format(self.bank_account, self.description, self.amount)
