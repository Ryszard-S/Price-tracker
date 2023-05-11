from django.urls import path

from . import views

urlpatterns = [
    path('shop', views.ShopListView.as_view()),
    path('products', views.ProductsListView.as_view()),
    path('product/<int:pk>', views.ProductDetailView.as_view()),
    path('ping', views.PingView.as_view()),
]
