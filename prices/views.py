from django.db.models import Q
from django.shortcuts import render
from django.views.generic import DetailView, ListView
from django.http import JsonResponse
from prices.models import Product, Shop, Category


class HomeListView(ListView):
    model = Product
    template_name = 'hello.html'
    context_object_name = 'products'

    def get_queryset(self):
        return Product.objects.order_by('?')[:10]


def barcode(request):
    return render(request, 'barcode.html')


def get_categories(request):
    shop_id = request.GET.get('shop_id')
    data = []
    categories = Category.objects.filter(shop_id=shop_id).order_by('category_name')
    for category in categories:
        data.append({'id': category.pk, 'categoryName': category.category_name})
    return JsonResponse(data, safe=False)


def get_brands(request):
    category_id = request.GET.get('category_id')
    data = []
    brands = Product.objects.filter(category_id=category_id).distinct('brand_id')
    # print(brands)
    for brand in brands:
        print(brand.brand_id.brand_name)
        data.append({'id': brand.brand_id.pk, 'brandName': brand.brand_id.brand_name})
    print(data)
    return JsonResponse(data, safe=False)


class SearchListView(ListView):
    model = Product
    template_name = 'search.html'
    context_object_name = 'products'
    paginate_by = 20

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['shops'] = Shop.objects.all()
        return context

    def get_queryset(self):
        ean = self.request.GET.get('ean', None)
        if ean:
            return Product.objects.filter(ean__contains=[ean])
        q = self.request.GET.get('q', '')
        shop_id = self.request.GET.get('shop', '')
        category_id = self.request.GET.get('category', '')
        brand_id = self.request.GET.get('brand', '')

        if shop_id and category_id and brand_id:
            return Product.objects.filter(Q(product_name__icontains=q) | Q(brand_id__brand_name__icontains=q),
                                          shop_id=shop_id, category_id=category_id, brand_id=brand_id)
        elif shop_id and category_id:
            return Product.objects.filter(Q(product_name__icontains=q) | Q(brand_id__brand_name__icontains=q),
                                          shop_id=shop_id, category_id=category_id)
        elif shop_id:
            return Product.objects.filter(Q(product_name__icontains=q) | Q(brand_id__brand_name__icontains=q),
                                          shop_id=shop_id, )
        return Product.objects.filter(Q(product_name__icontains=q) | Q(brand_id__brand_name__icontains=q))


class ProductDetailView(DetailView):
    model = Product
    template_name = 'product-detail.html'
    context_object_name = 'product'
