from django.shortcuts import render
from django.http import HttpResponse, Http404
from main.models import Product

def product_detail_view(request, id):
    try:
        product = Product.objects.get(id=id, is_active=True)
    except Product.DoesNotExist:
        raise Http404
    context = {
        'product': product
    }
    return render(request,'product.html', context)
def about_view(request):
    return HttpResponse('<h1> Hello, World! <h1>')


def main_page_view(request):
    products = Product.objects.filter(is_active=True)
    context = {
        'product_list': products
    }
    return render(request, 'index.html', context=context)