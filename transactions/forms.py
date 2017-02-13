from django import forms
from transactions.models import BankAccount, BankTransaction, TransactionLabel
from django.contrib.admin.widgets import AdminDateWidget
from django.conf import settings
from django.db.utils import OperationalError

class UploadForm(forms.Form):
    account = forms.ModelChoiceField(queryset=BankAccount.objects.all())
    file = forms.FileField()

    def getAccount(self):
        return self['account'].value()

    def getFile(self):
        return self['file'].value()

    def actuallyUpload(self):
        return self.request.get('actually-upload') == "true"

class TransactionForm(forms.ModelForm):

    class Meta:
        model = BankTransaction
        fields = ('Label','Notes')

class TransactionFilterForm(forms.Form):

    @staticmethod
    def getLabelOptions():
        try:
            return [(x.id,x.Name) for x in ([TransactionLabel.create("(Blank)",0)]+list(TransactionLabel.objects.all()))]
        except OperationalError:
            # When running makemigrations for the first time this will raise a OperationalError
            # We should ignore it
            return []

    account = forms.ModelMultipleChoiceField(
        queryset=BankAccount.objects.all(),
        required=False,)
    label = forms.MultipleChoiceField(
        choices=getLabelOptions.__func__(),
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

    def getAccount(self):
        return self['account'].value()
    def getLabel(self):
        return self['label'].value()
    def getDateFrom(self):
        return self['date_from'].value()
    def getDateTo(self):
        return self['date_to'].value()
    def getText(self):
        return self['text'].value()
    def getPage(self):
        return int(self.data.get('page')) if self.data.get('page') != None else 1
    def isPaged(self):
        return self.data.get('page') != "all"

class ManualForm(forms.ModelForm):
    class Meta:
        model = BankTransaction
        fields = ('Date','Description','Amount','Label','Notes')
        widgets = {
            'Date': forms.DateInput(attrs={'class':'datepicker'}),
        }
