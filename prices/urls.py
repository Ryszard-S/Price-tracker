from django.urls import path

from . import views
from .views import ProductDetailView, SearchListView, HomeListView

urlpatterns = [
    path('', HomeListView.as_view(), name="home"),
    path('barcode', views.barcode, name="barcode"),
    path('categories', views.get_categories, name="categories"),
    path('brands', views.get_brands, name="brands"),
    path('search', SearchListView.as_view(), name="search"),
    path('product/<int:pk>', ProductDetailView.as_view(), name="product"),
]
