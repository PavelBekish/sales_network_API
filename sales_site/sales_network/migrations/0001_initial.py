# Generated by Django 4.2 on 2023-05-01 12:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import mptt.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('country', models.CharField(max_length=200, verbose_name='Country')),
                ('city', models.CharField(max_length=200, verbose_name='City')),
                ('street', models.CharField(max_length=200, verbose_name='Street')),
                ('house_number', models.CharField(max_length=5, verbose_name='House number')),
            ],
        ),
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254, verbose_name='Email')),
                ('address', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='contacts', to='sales_network.address')),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=200, unique=True, verbose_name='Name')),
                ('model', models.CharField(max_length=200, verbose_name='Model')),
                ('release_date', models.DateField(verbose_name='Release date')),
            ],
        ),
        migrations.CreateModel(
            name='NetworkObject',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=200, unique=True, verbose_name='Name')),
                ('debt', models.DecimalField(decimal_places=2, max_digits=15, verbose_name='Debt')),
                ('created', models.DateTimeField(auto_now=True, verbose_name='Time of creation')),
                ('lft', models.PositiveIntegerField(editable=False)),
                ('rght', models.PositiveIntegerField(editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(editable=False)),
                ('contacts', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, related_name='network_objects', to='sales_network.contact')),
                ('employees', models.ManyToManyField(blank=True, related_name='network_objects', to=settings.AUTH_USER_MODEL)),
                ('parent', mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='children', to='sales_network.networkobject', verbose_name='Purveyor')),
                ('products', models.ManyToManyField(blank=True, related_name='network_objects', to='sales_network.product')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]