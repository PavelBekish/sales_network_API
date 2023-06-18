from django.db.models import Avg
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from sales_network.permissions import IsOwner
from sales_network.serializers import NetworkObjectListSerializer, StatisticsSerializer, ProductSerializer, \
    NetworkObjectCreateSerializer, NetworkObjectSerializer

from sales_network.models import NetworkObject, Product, Contact
from sales_network.tasks import send_email


class NetworkObjectsAPIList(generics.ListAPIView):
    serializer_class = NetworkObjectListSerializer
    queryset = NetworkObject.objects.select_related('contacts__address').all().prefetch_related('products',
                                                                                                'employees')
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        queryset = super().get_queryset()
        country = self.request.query_params.get('country')
        product_id = self.request.query_params.get('product_id')
        if country is not None:
            queryset = queryset.filter(contacts__address__country=country)
        if product_id is not None:
            queryset = queryset.filter(products__id=product_id)
        return queryset


class StatisticsAPIList(generics.ListAPIView):
    serializer_class = StatisticsSerializer
    permission_classes = (IsAuthenticated,)
    queryset = NetworkObject.objects.select_related('contacts__address', 'parent', 'parent__contacts__address').all()

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(debt__gt=NetworkObject.objects.all().aggregate(avg=Avg('debt'))['avg'])


class NetworkObjectsAPICreate(generics.CreateAPIView):
    queryset = NetworkObject.objects.all()
    serializer_class = NetworkObjectCreateSerializer
    permission_classes = (IsAuthenticated,)


class NetworkObjectsDeleteAPI(generics.DestroyAPIView):
    queryset = NetworkObject.objects.all()
    serializer_class = NetworkObjectSerializer
    permission_classes = (IsOwner,)

    def destroy(self, request, *args, **kwargs):
        self.obj = self.get_object()
        self.check_object_permissions(request, self.obj)
        return super().destroy(request, *args, **kwargs)


class NetworkObjectsUpdateAPI(generics.UpdateAPIView):
    queryset = NetworkObject.objects.all()
    serializer_class = NetworkObjectSerializer
    permission_classes = (IsOwner,)

    def update(self, request, *args, **kwargs):
        self.obj = self.get_object()
        self.check_object_permissions(request, self.obj)
        return super().update(request, *args, **kwargs)


class ProductAPICreate(generics.CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = (IsAuthenticated,)


class ProductAPI(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = (IsAuthenticated,)


class ContactsAPI(APIView):

    permission_classes = (IsAuthenticated,)

    def post(self, request, format=None):
        try:
            pk = request.data.get('id')
            contacts_name = ('name', 'email', 'country', 'city', 'street', 'house_number')
            contacts = Contact.objects.select_related('address',
                                                      'network_objects').values(
                'network_objects__name',
                'email', 'address__country',
                'address__city',
                'address__street',
                'address__house_number').get(network_objects__id=pk)
            contacts_str = '\n'.join(f'{contacts_name[i]}: {value}' for i, value in enumerate(contacts.values()))
            email = request.user.email
            send_email.delay(contacts_str, email)
        except (Exception,) as e:
            return Response({"Error": f"{e}"})
        return Response({"message": "Contact details sent by email"})
