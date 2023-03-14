from django.db.models import Q
from django.shortcuts import render
from django.views.generic import DetailView, ListView

from prices.models import Product, Price


# Create your views here.
def home(request):
    return render(request, 'hello.html')


class SearchListView(ListView):
    model = Product
    template_name = 'search.html'
    context_object_name = 'products'
    paginate_by = 20

    #
    # def get(self, request, *args, **kwargs):
    #     print(request)

    def get_queryset(self):
        q = self.request.GET.get('q', None)
        return Product.objects.filter(Q(product_name__icontains=q) | Q(brand_id__brand_name__icontains=q))


class ProductDetailView(DetailView):
    model = Product
    template_name = 'product-detail.html'
    context_object_name = 'product'

    # def get_context_data(self, **kwargs):
    #     # Call the base implementation first to get a context
    #     context = super().get_context_data(**kwargs)
    #     # Add in a QuerySet of all the books
    #     context['price_list'] = Price.objects.filter(product_id=)
    #     return context
