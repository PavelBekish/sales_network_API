from django.contrib.auth.models import User
from django.core.validators import EmailValidator
from drf_writable_nested import WritableNestedModelSerializer
from rest_framework import serializers

from sales_network.models import Product, Address, Contact, NetworkObject


class EmployeesSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'model', 'release_date']


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['id', 'country', 'city', 'street', 'house_number']


class ContactSerializer(WritableNestedModelSerializer):
    address = AddressSerializer(read_only=False)
    email = serializers.EmailField(validators=[EmailValidator(message='Invalid email format.')])

    class Meta:
        model = Contact
        fields = ['email', 'address']

    def update(self, instance, validated_data):
        email = validated_data.get('email', instance.email)
        if Contact.objects.filter(email=email).exclude(id=instance.id).exists():
            raise serializers.ValidationError('Contact with this Email already exists.')

        instance.email = email
        contacts_address = validated_data.get('address', instance.address)
        address = Address.objects.filter(country=contacts_address.get('country'), city=contacts_address.get('city'),
                                         street=contacts_address.get('street'),
                                         house_number=contacts_address.get('house_number')).first()
        if address:
            instance.address_id = address.id
        else:
            new_address = Address.objects.create(country=contacts_address.get('country'),
                                                 city=contacts_address.get('city'),
                                                 street=contacts_address.get('street'),
                                                 house_number=contacts_address.get('house_number'))
            instance.address_id = new_address.id
        instance.save()
        return instance


class NetworkObjectListSerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True, read_only=True)
    employees = EmployeesSerializer(many=True, read_only=True)
    contacts = ContactSerializer(read_only=True)

    class Meta:
        model = NetworkObject
        fields = ['id', 'name', 'contacts', 'employees', 'debt',
                  'created', 'parent', 'level', 'products']


class ParentSerializer(serializers.ModelSerializer):
    contacts = ContactSerializer(read_only=True)

    class Meta:
        model = NetworkObject
        fields = ['name', 'contacts']


class StatisticsSerializer(serializers.ModelSerializer):
    parent = ParentSerializer(read_only=True)

    class Meta:
        model = NetworkObject
        fields = ['name', 'parent', 'debt', 'created']


class NetworkObjectCreateSerializer(serializers.ModelSerializer):
    contacts = ContactSerializer(read_only=False)

    class Meta:
        model = NetworkObject
        fields = ['id', 'name', 'contacts',
                  'debt', 'created', 'parent']

    def create(self, validated_data):
        contacts = validated_data.get('contacts')
        contacts_address = contacts.get('address')
        address = Address.objects.filter(country=contacts_address.get('country'), city=contacts_address.get('city'),
                                         street=contacts_address.get('street'),
                                         house_number=contacts_address.get('house_number')).first()
        if not address:
            address = Address.objects.create(country=contacts_address.get('country'),
                                             city=contacts_address.get('city'),
                                             street=contacts_address.get('street'),
                                             house_number=contacts_address.get('house_number'))
        network_object_contacts = Contact.objects.create(email=contacts.get('email'),
                                                         address=address)
        network_object = NetworkObject.objects.create(name=validated_data.get('name'),
                                                      contacts=network_object_contacts,
                                                      debt=validated_data.get('debt'),
                                                      parent=validated_data.get('parent'))
        return network_object


class NetworkObjectSerializer(serializers.ModelSerializer):
    contacts = ContactSerializer()

    class Meta:
        model = NetworkObject
        read_only_fields = ['debt']
        fields = ['id', 'name', 'contacts', 'employees',
                  'debt', 'created', 'parent', 'products']

    def update(self, instance, validated_data):
        contacts_data = validated_data.pop('contacts', None)
        if contacts_data is not None:
            contacts_serializer = self.fields['contacts']
            contacts_serializer.update(instance.contacts, contacts_data)
        return super().update(instance, validated_data)
