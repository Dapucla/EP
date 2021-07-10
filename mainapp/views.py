from django.db import transaction
from django.shortcuts import render, redirect
from django.contrib.contenttypes.models import ContentType
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.views.generic import DetailView, View
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from .models import (
    NoteBook,
    Smartphone,
    Category,
    LatestProducts,
    Customer,
    Cart,
    CartProduct,
    Smartwatches,
    Headphones,
    Product,
    TV
)

# from .filters import ProductFilter
from .mixins import CategoryDetailMixin, CartMixin
from .forms import OrderForm, CreateUserForm
from .utils import recalc_cart
from .decorators import unauthenticated_user, allowed_users


@unauthenticated_user
def registerPage(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request, 'Аккаунт сделан! Добро пожаловать ' + user)
            return redirect('login')

    context = {'form': form}
    return render(request, 'register.html', context)


@unauthenticated_user
def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('base')
        else:
            messages.info(request, 'Неверное имя пользователя или пароль')
    context = {}
    return render(request, 'login.html', context)


def logoutUser(request):
    logout(request)
    return redirect('login')


def userPage(request):
    context = {}
    return render(request, 'user.html', context)


def react(request):
    return render(request, 'index.html')


def charts(request):
    labels = []
    data = []

    queryset = LatestProducts.objects.get_products_for_main_page(
            'notebook', 'smartphone', 'smartwatches', 'headphones', 'tv' )
    for product in queryset:
        labels.append(product.title)
        data.append(product.objects)
    return render(request, 'chart.html', {
        'labels': labels,
        'data': data
    })


class BaseView(CartMixin, View):
    @method_decorator(allowed_users(allowed_roles=['admin', 'customer', 'operator']))
    def get(self, request, *args, **kwargs):
        categories = Category.objects.get_categories_for_left_sidebar()
        # products_all = Product.objects.all()
        # myFilter = ProductFilter(request.GET, queryset=products_all)
        # products_all = myFilter.qs
        products = LatestProducts.objects.get_products_for_main_page(
            'notebook', 'smartphone', 'smartwatches', 'headphones', 'tv', with_respect_to='notebook'
        )
        context = {
            'categories': categories,
            'products': products,
            # 'myFilter': myFilter,
            # 'products_all': products_all,
            'cart': self.cart,
        }

        return render(request, 'base.html', context)


class ProductDetailView(CartMixin, CategoryDetailMixin, DetailView):

    CT_MODEL_MODEL_CLASS = {
        'notebook': NoteBook,
        'smartphone': Smartphone,
        'smartwatches': Smartwatches,
        'headphones': Headphones,
        'tv': TV,
    }

    @method_decorator(allowed_users(allowed_roles=['admin', 'customer', 'operator']))
    def dispatch(self, request, *args, **kwargs):
        self.model = self.CT_MODEL_MODEL_CLASS[kwargs['ct_model']]
        self.queryset = self.model._base_manager.all()
        return super().dispatch(request, *args, **kwargs)

    # model = Modeml
    # queryset = Model.objects.all()
    context_object_name = 'product'
    template_name = 'product_detail.html'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ct_model'] = self.model._meta.model_name
        context['cart'] = self.cart
        return context


class CategoryDetailView(CartMixin, CategoryDetailMixin, DetailView):

    model = Category
    queryset = Category.objects.all()
    context_object_name = 'category'
    template_name = 'category_detail.html'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cart'] = self.cart
        return context


class AddToCartView(CartMixin, View):
    @method_decorator(allowed_users(allowed_roles=['admin', 'customer', 'operator']))
    def get(self, request, *args, **kwargs):
        ct_model, product_slug = kwargs.get('ct_model'), kwargs.get('slug')
        content_type = ContentType.objects.get(model=ct_model)
        product = content_type.model_class().objects.get(slug=product_slug)
        cart_product, created = CartProduct.objects.get_or_create(
            user=self.cart.owner, cart=self.cart, content_type=content_type, object_id=product.id
        )
        if created:
            self.cart.products.add(cart_product)
        recalc_cart(self.cart)
        messages.add_message(request, messages.INFO, "Товар добавлен")
        return HttpResponseRedirect('/cart/')


class DeleteFromCartView(CartMixin, View):
    @method_decorator(allowed_users(allowed_roles=['admin', 'customer', 'operator']))
    def get(self, request, *args, **kwargs):
        ct_model, product_slug = kwargs.get('ct_model'), kwargs.get('slug')
        content_type = ContentType.objects.get(model=ct_model)
        product = content_type.model_class().objects.get(slug=product_slug)
        cart_product = CartProduct.objects.get(
            user=self.cart.owner, cart=self.cart, content_type=content_type, object_id=product.id
        )
        self.cart.products.remove(cart_product)
        cart_product.delete()
        recalc_cart(self.cart)
        messages.add_message(request, messages.INFO, "Товар удален")
        return HttpResponseRedirect('/cart/')


class ChangeQTYView(CartMixin, View):
    @method_decorator(allowed_users(allowed_roles=['admin', 'customer', 'operator']))
    def post(self, request, *args, **kwargs):
        ct_model, product_slug = kwargs.get('ct_model'), kwargs.get('slug')
        content_type = ContentType.objects.get(model=ct_model)
        product = content_type.model_class().objects.get(slug=product_slug)
        cart_product = CartProduct.objects.get(
            user=self.cart.owner, cart=self.cart, content_type=content_type, object_id=product.id
        )
        quantity = int(request.POST.get('quantity'))
        cart_product.quantity = quantity
        cart_product.save()
        recalc_cart(self.cart)
        messages.add_message(request, messages.INFO, "Количество товара изменено")
        return HttpResponseRedirect('/cart/')


class CartView(CartMixin, View):
    @method_decorator(allowed_users(allowed_roles=['admin', 'customer', 'operator']))
    def get(self, request, *args, **kwargs):
        categories = Category.objects.get_categories_for_left_sidebar()
        context = {
            'cart': self.cart,
            'categories': categories
        }
        return render(request, 'cart.html', context)


class CheckoutView(CartMixin, View):
    @method_decorator(allowed_users(allowed_roles=['admin', 'customer', 'operator']))
    def get(self, request, *args, **kwargs):
        categories = Category.objects.get_categories_for_left_sidebar()
        form = OrderForm(request.POST or None)
        context = {
            'cart': self.cart,
            'categories': categories,
            'form': form
        }
        return render(request, 'checkout.html', context)


class MakeOrderView(CartMixin, View):

    @transaction.atomic
    @method_decorator(allowed_users(allowed_roles=['admin', 'customer', 'operator']))
    def post(self, request, *args, **kwargs):
        form = OrderForm(request.POST or None)
        customer = Customer.objects.get(user=request.user)
        if form.is_valid():
            new_order = form.save(commit=False)
            new_order.customer = customer
            new_order.first_name = form.cleaned_data['first_name']
            new_order.last_name = form.cleaned_data['last_name']
            new_order.phone = form.cleaned_data['phone']
            new_order.address = form.cleaned_data['address']
            new_order.buying_type = form.cleaned_data['buying_type']
            new_order.order_date = form.cleaned_data['order_date']
            new_order.comment = form.cleaned_data['comment']
            new_order.save()
            self.cart.in_order = True
            self.cart.save()
            new_order.cart = self.cart
            new_order.save()
            customer.orders.add(new_order)
            messages.add_message(request, messages.INFO, 'Спасибо за заказ! Менеджер с Вами свяжется')
            return HttpResponseRedirect('/')
        return HttpResponseRedirect('/checkout/')


