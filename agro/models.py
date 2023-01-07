from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

POST_TYPE = (
    ("FS", "For Sale"),
    ("FB", "For Buy"),
)


class Category(models.Model):
    category_name = models.CharField(max_length=20, blank=False)

    class Meta:
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.category_name


class ProductItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, blank=False, null=False)
    price = models.DecimalField(max_digits=20, decimal_places=2,
                                blank=False, null=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE,
                                 blank=False)
    unit = models.CharField(max_length=20, blank=True, null=True)
    quantity = models.FloatField()
    description = models.TextField()
    image = models.ImageField(upload_to='productImage', blank=False,
                              null=False)
    post_type = models.CharField(max_length=20, choices=POST_TYPE)
    status = models.BooleanField(default=True)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def short_desc(self):
        return self.description[:200]

    def get_absolute_url(self):
        return reverse('detail', args=[str(self.id)])


class BeatItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(ProductItem, on_delete=models.CASCADE)
    reply = models.CharField(max_length=500, blank=False)
    status = models.BooleanField(default=True)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.reply


class Complain(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=300)
    description = models.TextField()
    status = models.BooleanField(default=False)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.subject


class ContactUs(models.Model):
    name = models.CharField(max_length=40, blank=False)
    email = models.EmailField(max_length=60, blank=False, null=False)
    subject = models.CharField(max_length=300)
    message = models.TextField()
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'ContactUs'

    def __str__(self):
        return self.email

class EmailSubscription(models.Model):
    email = models.EmailField(max_length=50)
    create_date = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return str(self.email)