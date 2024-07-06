from django.shortcuts import render
from django.http import HttpResponse
from main.models import Product

def about_view(request):
    return HttpResponse('<h1> Hello, World! <h1>')


def main_page_view(request):
    products = Product.objects.all()
    context = {
        'product_list': products
    }
    return render(request, 'index.html', context=context)