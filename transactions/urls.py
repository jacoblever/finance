from django.conf.urls import url
from django.views.generic import ListView

from transactions.models import BankAccount, BankTransaction
from transactions.forms import TransactionForm
from transactions.views import TransactionsView, TransactionsDownloadView, PastUploadsView



from . import views

urlpatterns = [
    url(r'^$', TransactionsView.as_view()),
    url(r'^download/$', TransactionsDownloadView.as_view()),
    url(r'^save-labels/$', views.saveLabels, name='same-labels'),
    url(r'^accounts/$', ListView.as_view(queryset=BankAccount.objects.all(),
                                template_name="transactions/accounts.html")),
    url(r'^upload/$', views.upload, name='upload-s'),
    url(r'^graph-week-data/$', views.graph, name='graph'),
    url(r'^graph/$', ListView.as_view(queryset=BankAccount.objects.all(),
                                template_name="transactions/graph2.html")),
    url(r'^past-uploads/$', PastUploadsView.as_view()),
    url(r'^past-uploads/delete/$', views.deletePastUploads, name='delete-past-uploads')
]
