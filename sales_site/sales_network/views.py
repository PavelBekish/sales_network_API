from django.db.models import Avg
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from sales_network.serializers import NetworkObjectListSerializer, StatisticsSerializer, ProductSerializer, \
    NetworkObjectCreateSerializer, NetworkObjectSerializer

from sales_network.models import NetworkObject, Product


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
    queryset = NetworkObject.objects.select_related('contacts__address', 'parent', 'parent__contacts__address').all()

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(debt__gt=NetworkObject.objects.all().aggregate(avg=Avg('debt'))['avg'])


class NetworkObjectsAPICreate(generics.CreateAPIView):
    queryset = NetworkObject.objects.all()
    serializer_class = NetworkObjectCreateSerializer


class NetworkObjectsDeleteAPI(generics.DestroyAPIView):
    queryset = NetworkObject.objects.all()
    serializer_class = NetworkObjectSerializer


class NetworkObjectsUpdateAPI(generics.UpdateAPIView):
    queryset = NetworkObject.objects.all()
    serializer_class = NetworkObjectSerializer


class ProductAPICreate(generics.CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductAPI(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
