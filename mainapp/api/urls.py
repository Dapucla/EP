from django.urls import path

from .api_views import (CategoryListCreateApiView,
                        SmartphoneListAPIView,
                        SmartphoneDetailAPIView,
                        CustomersListAPIView
                        )

urlpatterns = [
    path('categories/<str:id>/', CategoryListCreateApiView.as_view(), name='categories'),
    path('customers/', CustomersListAPIView.as_view(), name='customers_list'),
    path('smartphones/', SmartphoneListAPIView.as_view(), name='smartphones_list'),
    path('smartphones/<str:id>/', SmartphoneDetailAPIView.as_view(), name='smartphone_detail'),
]