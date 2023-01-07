from django.shortcuts import render, get_object_or_404, redirect
from .models import ProductItem, BeatItem, Category, ContactUs, EmailSubscription, Complain
from .forms import ProductForm,ComplainForm

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.mail import BadHeaderError, send_mail
from django.conf import settings
from django.contrib import messages


def pagination(products, page):
    products_paginator = Paginator(products, 10)
    try:
        products = products_paginator.page(page)
    except PageNotAnInteger:
        products = products_paginator.page(1)
    except EmptyPage:
        products = products_paginator.page(products_paginator.num_pages)
    return products


def product_search(search, category, post_type):

    if search:
        products = ProductItem.objects.filter(title__icontains=search,
                                              status=True, post_type=post_type)
    elif category:
        products = ProductItem.objects.filter(category=category,
                                              status=True, post_type=post_type)
    else:
        products = ProductItem.objects.filter(status=True, post_type=post_type)

    return products


def home(request):
    context = {}
    return render(request, 'index.html', context)


def sale_page(request):
    context = {}
    search = request.GET.get('search')
    category = request.GET.get('category')
    page = request.GET.get('page', 1)

    products = product_search(search, category, "FS").order_by('-id')

    context['categories'] = Category.objects.all()

    context['products'] = pagination(products, page)
    return render(request, 'shop.html', context)


def buy_page(request):
    context = {}
    search = request.GET.get('search')
    category = request.GET.get('category')
    page = request.GET.get('page', 1)

    products = product_search(search, category, "FB").order_by('-id')

    context['categories'] = Category.objects.all()

    context['products'] = pagination(products, page)
    return render(request, 'shop.html', context)


def detail(request, id):
    context = {}
    product = get_object_or_404(ProductItem, pk=id)
    context['product'] = product
    context['beats'] = BeatItem.objects.filter(product__id=id).order_by('-id')
    return render(request, 'detail.html', context)


def add_product(request):
    context = {}
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
            instance.save()
            return redirect('userprofile')
    context['form'] = ProductForm()
    return render(request, 'add-product.html', context)


def add_complain(request):
    context = {}
    if request.method == 'POST':
        form = ComplainForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
            instance.save()
            return redirect('userprofile')
    context['form'] = ComplainForm()
    return render(request, 'complain.html', context)


def edit_product(request, id):
    context = {}
    data = ProductItem.objects.get(id=id)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=data)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
            instance.save()
            return redirect('userprofile')
    context['form'] = ProductForm(instance=data)
    return render(request, 'edit-product.html', context)


def delete_product(request, id):
    ProductItem.objects.get(id=id).delete()
    return redirect('userprofile')


def reply(request):
    if request.method == 'POST':
        user = request.user
        product_id = request.POST.get('product_id')
        reply = request.POST.get('reply')
        product = get_object_or_404(ProductItem, pk=product_id)
        BeatItem.objects.create(user=user, product=product, reply=reply)
    return redirect(request.META['HTTP_REFERER'])


def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        if name and email and subject and message:
            ContactUs(name=name, email=email,
                      subject=subject, message=message).save()
            try:
                print("got it", request.META['HTTP_REFERER'])
                from_email = settings.DEFAULT_FROM_EMAIL
                send_mail(subject, message, from_email, [
                          email],  fail_silently=False,)
                messages.success(
                    request, f"Hello {name},\nThanks for contact with us!")
            except BadHeaderError as error:
                messages.error(request, f"{error}")
        else:
            messages.error(
                request, f"Mail Subject or message body or your email error")

    return redirect(request.META['HTTP_REFERER'])


def email_subscribe(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        if email:
            EmailSubscription(email=email).save()
    return redirect(request.META['HTTP_REFERER'])
