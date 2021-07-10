from django.urls import path
from django.contrib.auth.decorators import login_required

from .views import (
    BaseView,
    ProductDetailView,
    CategoryDetailView,
    CartView,
    AddToCartView,
    DeleteFromCartView,
    ChangeQTYView,
    CheckoutView,
    MakeOrderView,
    registerPage,
    loginPage,
    logoutUser,
    userPage,
    charts,
    react
)


urlpatterns = [
    path('', login_required(BaseView.as_view()), name='base'),
    path('products/<str:ct_model>/<str:slug>/', login_required(ProductDetailView.as_view()), name='product_detail'),
    path('category/<str:slug>/', login_required(CategoryDetailView.as_view()), name='category_detail'),
    path('cart/', login_required(CartView.as_view()), name='cart'),
    path('add-to-cart/<str:ct_model>/<str:slug>/', login_required(AddToCartView.as_view()), name='add_to_cart'),
    path('remove-from-cart/<str:ct_model>/<str:slug>/', login_required(DeleteFromCartView.as_view()), name='delete_from_cart'),
    path('change-quantity/<str:ct_model>/<str:slug>/', login_required(ChangeQTYView.as_view()), name='change_quantity'),
    path('checkout/', login_required(CheckoutView.as_view()), name='checkout'),
    path('make-order/', login_required(MakeOrderView.as_view()), name='make_order'),
    path('register/', registerPage, name='register'),
    path('login/', loginPage, name='login'),
    path('logout/', logoutUser, name='logout'),
    path('user/', userPage, name='user'),
    path('charts/', charts, name='charts'),
    path('front/', react, name="front")
]


