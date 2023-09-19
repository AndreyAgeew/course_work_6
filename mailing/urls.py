from django.urls import path
from .views import MailingCreateView, MailingDetailView, MessageCreateView, ClientListView, MailingListView, HomeView, \
    DeliveryReportView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('mailing/', MailingListView.as_view(), name='mailing'),
    path('create_mailing/', MailingCreateView.as_view(), name='create_mailing'),
    path('mailing/<int:pk>/', MailingDetailView.as_view(), name='mailing_detail'),
    path('mailing/<int:mailing_pk>/create_message/', MessageCreateView.as_view(), name='create_message'),
    path('clients/', ClientListView.as_view(), name='client_list'),
    path('delivery_report/', DeliveryReportView.as_view(), name='delivery_report'),
]
