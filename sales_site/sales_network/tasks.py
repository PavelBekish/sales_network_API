from sales_site.celery import app
from sales_network.models import NetworkObject
from random import randint as rnd


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

