from django.db.models import Q
from django.shortcuts import render
from django.views.generic import DetailView, ListView

from prices.models import Product


# Create your views here.
def home(request):
    return render(request, 'hello.html')


def barcode(request):
    return render(request, 'barcode.html')


class SearchListView(ListView):
    model = Product
    template_name = 'search.html'
    context_object_name = 'products'
    paginate_by = 20

    def get_queryset(self):
        ean = self.request.GET.get('ean', None)
        if ean:
            return Product.objects.filter(ean__contains=[ean])
        q = self.request.GET.get('q', None)
        return Product.objects.filter(Q(product_name__icontains=q) | Q(brand_id__brand_name__icontains=q))


class ProductDetailView(DetailView):
    model = Product
    template_name = 'product-detail.html'
    context_object_name = 'product'
