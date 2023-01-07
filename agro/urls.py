from django.urls import path
from .views import (home, add_product, add_complain, edit_product, delete_product,
                    sale_page, buy_page, detail, reply, contact, email_subscribe)

urlpatterns = [
    path('', home, name='home'),
    path('add-product/', add_product, name='add_product'),
    path('edit-product/<int:id>/', edit_product, name='edit_product'),
    path('delete-product/<int:id>/', delete_product, name='delete_product'),
    path('sale-page/', sale_page, name='sale_page'),
    path('buy-page/', buy_page, name='buy_page'),
    path('reply/', reply, name='reply'),
    path('detail/<int:id>/', detail, name='detail'),
    path('contact/', contact, name='contact'),
    path('email-subscribe/', email_subscribe, name='email_subscribe'),
    path('add-complain/', add_complain, name='add_complain'),
]
