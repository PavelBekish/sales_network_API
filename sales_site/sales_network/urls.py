from django.urls import path, include, re_path
from sales_network import views


urlpatterns = [
    path('network_objects/', views.NetworkObjectsAPIList.as_view()),
    path('statistics/', views.StatisticsAPIList.as_view()),
    path('create_network_object/', views.NetworkObjectsAPICreate.as_view()),
    path('delete_network_object/<int:pk>/', views.NetworkObjectsDeleteAPI.as_view()),
    path('update_network_object/<int:pk>/', views.NetworkObjectsUpdateAPI.as_view()),
    path('create_product/', views.ProductAPICreate.as_view()),
    path('delete_product/<int:pk>/', views.ProductAPI.as_view()),
    path('update_product/<int:pk>/', views.ProductAPI.as_view()),
    path('drf-auth/', include('rest_framework.urls')),
    path('auth/', include('djoser.urls')),
]
