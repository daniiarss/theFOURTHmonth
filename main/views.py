from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from main.models import Product, Review
from main.forms import ProductForm, UserRegistrationForm, UserLoginForm
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .constants import PAGE_SIZE
from django.views import View
from django.views.generic import ListView, DetailView

def logout_view(request):
    logout(request)
    return redirect('/')

class AuthorizationView(View):
    def get(self, request, *args, **kwargs):
        form = UserRegistrationForm()
        return render(request, 'authorization.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('/')
        return render(request, 'authorization.html', {'form': form})


def authorization_view(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('/')
    else:
        form = UserLoginForm()
    return render(request, 'authorization.html', context={'form': form})

def registration_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            User.objects.create_user(username=username, password=password)
            return redirect('/authorization/')
    else:
        form = UserRegistrationForm()
    return render(request, 'registration.html', context={'form': form})

@login_required(login_url='/authorization/')
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

class ProductDetailView(DetailView):
    model = Product
    template_name = 'product_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product_id = kwargs['object'].id
        context['reviews'] = Review.objects.filter(product_id=product_id)
        return context


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
    return render(request,'product_detail.html', context)
def about_view(request):
    return HttpResponse('<h1> Hello, World! <h1>')

class ProductListView(ListView):
    model = Product
    template_name = 'index.html'
    paginate_by = PAGE_SIZE

    def get_queryset(self):
        search_word = self.request.GET.get('search', '')
        queryset = super().get_queryset()
        queryset = queryset.filter(tittle__icontains=search_word)
        try:
            price_from = int(self.request.GET.get('price_from', 0))
        except:
            price_from = 0
        try:
            price_to = int(self.request.GET.get('price_to', 0))
        except:
            price_to = None
        if price_from:
            queryset = queryset.filter(price__gte=price_from)
        if price_from:
            queryset = queryset.filter(price__lte=price_to)
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset = super().get_queryset()
        total_amount = queryset.count()
        buttons = total_amount // PAGE_SIZE
        if total_amount % PAGE_SIZE > 0:
            buttons += 1
        context['price_from'] = self.request.GET.get('price_from', '')
        context['price_to'] = self.request.GET.get('price_to', '')
        context['search_word'] = self.request.GET.get('search', '')
        context['button_list'] = [str(i) for i in range(1, buttons+1)]
        context['page'] = self.request.GET.get('page', '1')
        return context






def main_page_view(request):
    search_word = (request.GET.get('search', ''))
    try:
        page = int(request.GET.get('page', 1))
    except:
        page = 1

    try:
        price_from = int(request.GET.get('price_from', 0))
    except:
        price_from = 0
    try:
        price_to = int(request.GET.get('price_to', 0))
    except:
        price_to = None
    products = Product.objects.filter(
        tittle__icontains=search_word,
        price__gte=price_from,
    )
    if price_to:
        products = products.filter(
            price__lte=price_to,
        )
    products = products.order_by('-price', '-updated')
    total_amount = len(products)
    buttons = total_amount // PAGE_SIZE
    if total_amount % PAGE_SIZE > 0:
        buttons += 1
    context = {
        'product_list': products[PAGE_SIZE * (page -1):PAGE_SIZE * page],
        'search_word': search_word,
        'price_from': price_from if price_from != 0 else '',
        'price_to': price_to,
        'button_list': [i for i in range(1, buttons+1)],
        'page': page
    }
    return render(request, 'index.html', context=context)