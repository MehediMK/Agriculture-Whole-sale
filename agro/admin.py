from django.contrib import admin
from .models import (ProductItem, Category, BeatItem,
                     Complain, ContactUs, EmailSubscription)

admin.site.register(Category)
admin.site.register(BeatItem)
admin.site.register(Complain)
admin.site.register(ContactUs)
admin.site.register(EmailSubscription)


@admin.register(ProductItem)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['pk', 'user', 'title',
                    'price', 'category', 'unit', 'quantity']
    search_fields = ('title', 'price', 'category', 'unit', 'quantity')
    list_editable = ['title', 'price', 'category', 'unit', 'quantity']
    list_display_links = ['pk', 'user']
