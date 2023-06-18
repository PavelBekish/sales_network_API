import os
import uuid
from email.mime.image import MIMEImage

import qrcode
from celery import shared_task
from django.core.mail import EmailMultiAlternatives

from sales_site.celery import app
from sales_network.models import NetworkObject
from random import randint as rnd

from sales_site.settings import BASE_DIR


@app.task
def increase_debt():
    """
    The function increases the debt by a random number from 1 to 500.
    """
    network_objects = NetworkObject.objects.all()
    for network_object in network_objects:
        network_object.debt = network_object.debt + rnd(1, 500)
        network_object.save(update_fields=['debt'])


@app.task
def reduce_debt():
    """
    The function reduces the debt by a random number from 100 to 10000.
    """
    network_objects = NetworkObject.objects.all()
    for network_object in network_objects:
        network_object.debt = network_object.debt - rnd(100, 10000)
        if network_object.debt >= 0:
            network_object.save(update_fields=['debt'])


@app.task
def clear_debt(pk):
    """
    The function clears the debt.
    """
    NetworkObject.objects.filter(pk__in=pk).update(debt=0)


@shared_task
def send_email(contacts, email):
    """
    The function sends a QR code with contact details to the user's email.
    """
    image = qrcode.make(contacts)
    file_name = str(uuid.uuid4())[:12]
    complete_file_name = "%s.%s" % (file_name, '.png',)
    if not os.path.exists(os.path.join(BASE_DIR, 'media')):
        os.mkdir(os.path.join(BASE_DIR, 'media'))
    path = os.path.join(BASE_DIR, f'media\{complete_file_name}')
    image.save(path)
    subject = 'Контактные данные'
    body_html = '<html><body><img src="cid:{file_name}" width=250 height=250/></body></html>'\
        .format(file_name=file_name)
    msg = EmailMultiAlternatives(
        subject,
        body_html,
        from_email='testdjangobp@gmail.com',
        to=[email]
    )
    msg.mixed_subtype = 'related'
    msg.attach_alternative(body_html, "text/html")
    with open(path, 'rb') as f:
        img = MIMEImage(f.read())
        img.add_header('Content-ID', f'<{file_name}>')
    msg.attach(img)

    mail_sent = msg.send()
    os.remove(path)
    return mail_sent

