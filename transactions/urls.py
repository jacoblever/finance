from django.conf.urls import url
from django.views.generic import ListView

from transactions.models import BankAccount, Transaction
from transactions.forms import TransactionForm
from transactions.views import TransactionsView, TransactionsDownloadView, PastUploadsView

from . import views

urlpatterns = [
    url(r'^$', TransactionsView.as_view(), name='home'),
    url(r'^download/$', TransactionsDownloadView.as_view()),
    url(r'^save-labels/$', views.save_labels),
    url(r'^accounts/$', ListView.as_view(queryset=BankAccount.objects.all().filter(id__gt=0),
                                template_name="transactions/accounts.html"), name='accounts'),
    url(r'^accounts/new/$', views.edit_account),
    url(r'^accounts/(?P<id_>\w+)/$', views.edit_account),
    url(r'^upload/$', views.upload),
    url(r'^manual/$', views.manual),
    url(r'^manual/(?P<id_>\w+)/$', views.manual),
    url(r'^graph-week-data/$', views.graph),
    url(r'^graph/$', ListView.as_view(queryset=BankAccount.objects.all(),
                                template_name="transactions/graph2.html")),
    url(r'^past-uploads/$', PastUploadsView.as_view()),
    url(r'^past-uploads/delete/$', views.delete_past_uploads)
]
