from django.contrib.auth.models import User
from django.db import models
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel


class Product(models.Model):
    name = models.CharField(max_length=200, db_index=True, unique=True, verbose_name='Name')
    model = models.CharField(max_length=200, verbose_name='Model')
    release_date = models.DateField(auto_now=False, verbose_name='Release date')

    def __str__(self):
        return f'{self.name}'


class Address(models.Model):
    country = models.CharField(max_length=200, verbose_name='Country')
    city = models.CharField(max_length=200, verbose_name='City')
    street = models.CharField(max_length=200, verbose_name='Street')
    house_number = models.CharField(max_length=5, verbose_name='House number')

    class Meta:
        verbose_name = 'Address'
        verbose_name_plural = 'Addresses'

    def __str__(self):
        return f"{self.country}, {self.city}, {self.street}, {self.house_number}"


class Contact(models.Model):
    email = models.EmailField(verbose_name='Email', unique=True)
    address = models.ForeignKey(Address, related_name='contacts', on_delete=models.PROTECT)

    def __str__(self):
        return f"{self.email}"


class NetworkObject(MPTTModel):
    name = models.CharField(max_length=200, db_index=True, unique=True, verbose_name='Name')
    contacts = models.OneToOneField(Contact, related_name='network_objects', on_delete=models.PROTECT)
    products = models.ManyToManyField(Product, related_name='network_objects', blank=True)
    employees = models.ManyToManyField(User, related_name='network_objects', blank=True)
    debt = models.DecimalField(max_digits=15, decimal_places=2, verbose_name='Debt')
    created = models.DateTimeField(auto_now=True, verbose_name='Time of creation')
    parent = TreeForeignKey('self', blank=True, null=True, on_delete=models.PROTECT, related_name='children',
                            verbose_name='Purveyor')

    def __str__(self):
        return f'{self.name}'
