from django.conf import settings
from django.core.mail import send_mail


def mail_managers(subject, html):
    send_mail(
        subject=subject.strip(),
        message='',
        fail_silently=True,
        from_email=settings.DEFAULT_FROM_EMAIL,
        html_message=html,
        recipient_list=[manager[1] for manager in settings.MANAGERS])
