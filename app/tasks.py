# Standard Library imports

# Core Flask imports
from flask_mail import Message

# Third-party imports
from celery import shared_task

# App imports
from .extensions import mail


@shared_task()
def send_email(subject, sender, recipients):
    msg = Message(subject=subject,
                  sender=sender,
                  recipients=recipients)
    mail.send(msg)
