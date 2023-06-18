from django.contrib import admin
from django.db.models import QuerySet
from django_mptt_admin.admin import DjangoMpttAdmin
from sales_network.models import Product, NetworkObject, Address, Contact
from sales_network.tasks import clear_debt


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'model', 'release_date']


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ['country', 'city', 'street', 'house_number']


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['email', 'address']


@admin.register(NetworkObject)
class SalesNetworkObjectAdmin(DjangoMpttAdmin):
    list_display = ['name', 'contacts', 'parent', 'debt', 'created']
    list_filter = ['contacts__address__city']
    raw_id_fields = ('parent',)
    actions = ['clean_debts']

    @admin.action(description='Clear Debt')
    def clear_debts(self, request, qs: QuerySet):
        """
        The function clears the debt of the selected trading objects
        """
        if len(qs) < 20:
            qs.update(debt=0)
        else:
            clear_debt.delay([network_object.pk for network_object in qs])

