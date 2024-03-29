from django.db.models import Q
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView

from api.serializers import ShopSerializer, ProductSerializer, ProductWithoutPricesSerializer
from prices.models import Shop, Product


class PingView(APIView):
    """
    Ping a service to wake up
    """

    def get(self, request):
        return Response({"message": "ok"})


class ShopListView(generics.ListAPIView):
    queryset = Shop.objects.all()
    serializer_class = ShopSerializer


class ProductsListView(generics.ListAPIView):
    serializer_class = ProductWithoutPricesSerializer

    def get_queryset(self):
        search = self.request.GET.get('search')
        ean = self.request.GET.get('ean')
        if ean:
            return Product.objects.select_related('shop_id', 'category_id', 'brand_id').filter(ean__contains=[ean])
        if search:
            return Product.objects.select_related('shop_id', 'category_id', 'brand_id').filter(
                Q(product_name__icontains=search) | Q(brand_id__brand_name__icontains=search)).order_by('pk')
        return Product.objects.all()


class ProductDetailView(generics.RetrieveAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        product_id = self.kwargs.get('pk')
        print(product_id)
        qs = Product.objects.filter(pk=product_id)
        print(qs)
        return qs
