from django.urls import path
from .views import MailingCreateView, MailingDetailView, MessageCreateView, ClientListView, MailingListView

urlpatterns = [
    path('', MailingListView.as_view(), name='main'),
    path('create_mailing/', MailingCreateView.as_view(), name='create_mailing'),
    path('<int:pk>/', MailingDetailView.as_view(), name='mailing_detail'),
    path('<int:mailing_pk>/create_message/', MessageCreateView.as_view(), name='create_message'),
    path('clients/', ClientListView.as_view(), name='client_list'),
]
