from django import forms
from transactions.models import BankAccount, Transaction, TransactionLabel, BankAccountTemplate
from django.contrib.admin.widgets import AdminDateWidget
from django.conf import settings
from django.db.utils import OperationalError


class ImportForm(forms.Form):
    account = forms.ModelChoiceField(queryset=BankAccount.objects.all())
    file = forms.FileField()

    def get_account(self):
        return self['account'].value()

    def get_file(self):
        return self['file'].value()

    def actually_import(self):
        return self.request.get('actually-import') == "true"


class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ('transaction_label','notes')


class TransactionFilterForm(forms.Form):
    @staticmethod
    def get_label_options():
        try:
            return [(x.id, x.name) for x in ([TransactionLabel.create("(Blank)",0)]+list(TransactionLabel.objects.all()))]
        except OperationalError:
            # When running makemigrations for the first time this will raise an OperationalError
            # We should ignore it
            return []

    account = forms.ModelMultipleChoiceField(
        queryset=BankAccount.objects.all().filter(is_active__exact=True),
        required=False,)
    label = forms.MultipleChoiceField(
        choices=get_label_options.__func__(),
        required=False,)
    date_from = forms.DateField(
        widget = AdminDateWidget,
        input_formats=settings.DATE_INPUT_FORMATS,
        required=False,)
    date_to = forms.DateField(
        widget = AdminDateWidget,
        input_formats=settings.DATE_INPUT_FORMATS,
        required=False,)
    text = forms.CharField(
        required=False,)

    def get_account(self):
        return self['account'].value()

    def get_label(self):
        return self['label'].value()

    def get_date_from(self):
        return self['date_from'].value()

    def get_date_to(self):
        return self['date_to'].value()

    def get_text(self):
        return self['text'].value()

    def get_page(self):
        return int(self.data.get('page')) if self.data.get('page') != None else 1

    def is_paged(self):
        return self.data.get('page') != "all"


class ManualForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ('date','description','amount','transaction_label','notes')
        widgets = {
            'date': forms.DateInput(attrs={'class':'datepicker'}),
        }


class BankAccountForm(forms.ModelForm):
    @staticmethod
    def get_account_template_options():
        try:
            return [('',"---------")]\
                   +[(x.id, x.name) for x in BankAccountTemplate.objects.all().filter(is_built_in__exact=True)] \
                   +[('custom',"Custom...")]
        except OperationalError:
            # When running makemigrations for the first time this will raise an OperationalError
            # We should ignore it
            return []

    template = forms.ChoiceField(
        choices=get_account_template_options.__func__())

    class Meta:
        model = BankAccount
        fields = ('name', 'account_type', 'more_details', 'is_active', 'template')


class AccountTemplateForm(forms.ModelForm):
    has_balance = forms.BooleanField(required=False)
    has_custom_date_1 = forms.BooleanField(required=False)
    has_custom_text_1 = forms.BooleanField(required=False)

    class Meta:
        model = BankAccountTemplate
        fields = (
            'get_date',
            'get_description',
            'get_amount',
            'has_balance',
            'get_current_balance',
            'has_custom_date_1',
            'custom_date_1_name',
            'get_custom_date_1',
            'has_custom_text_1',
            'custom_text_1_name',
            'get_custom_text_1',
        )
        widgets = {
            'get_current_balance': forms.TextInput(attrs={'required': ''}),
            'custom_date_1_name': forms.TextInput(attrs={'required': ''}),
            'get_custom_date_1': forms.TextInput(attrs={'required': ''}),
            'custom_text_1_name': forms.TextInput(attrs={'required': ''}),
            'get_custom_text_1': forms.TextInput(attrs={'required': ''}),
        }
