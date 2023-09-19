from django.conf import settings
from django.core.mail import send_mail

from mailing.models import Mailing, Log


def send_mailings(frequency):
    for mailing in Mailing.objects.filter(frequency=frequency, status='created'):
        emails = [client.email for client in mailing.recipients.all()]
        try:
            send_mail(
                subject=mailing.message.subject,
                message=mailing.message.body,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=emails
            )
            attempt_status = 'success'
            server_response = 'Email sent successfully'
        except Exception as e:
            attempt_status = 'error'
            server_response = str(e)
        Log.objects.create(message=mailing.message,
                           status=attempt_status,
                           response=server_response)
        mailing.status = 'completed'
        mailing.save()
