from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from main.models import Product, Review
from main.forms import ProductForm

def create_product_view(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    context = {
        'form': ProductForm()
    }
    return render(request, 'add.html', context=context)
def product_detail_view(request, id):
    try:
        product = Product.objects.get(id=id, is_active=True)
    except Product.DoesNotExist:
        raise Http404
    reviews = Review.objects.filter(product_id=id)
    context = {
        'product': product,
        'reviews': reviews
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