from django.urls import path

from . import views
from .views import ProductDetailView, SearchListView

urlpatterns = [
    path('', views.home, name="home"),
    path('barcode', views.barcode, name="barcode"),
    path('search/', SearchListView.as_view(), name="search"),
    path('product/<int:pk>', ProductDetailView.as_view(), name="product"),
]
