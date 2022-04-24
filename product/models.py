
# from django.Acheamponginc import File
from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.shortcuts import reverse
from datetime import datetime, date
#from django_countries.fields import CountryField
# Create your models here


class Category(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category')


class Section(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('section')


class Sizes(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('sizes')


class Product(models.Model):
    category = models.ManyToManyField(Category, related_name='category')
    section = models.ManyToManyField(Section, related_name='section')
    sizes = models.ManyToManyField(Sizes, related_name='sizes')
    image = models.ImageField(upload_to='', blank=True, null=True)
    image_1 = models.ImageField(upload_to='', blank=True, null=True)
    image_2 = models.ImageField(upload_to='', blank=True, null=True)
    title = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    discount_price = models.DecimalField(
        max_digits=12, decimal_places=2, blank=True, null=True)
    stocks = models.IntegerField()
    sold = models.IntegerField()
    date_added = models.DateField(auto_now_add=True)
    discription = models.TextField()
    likes = models.ManyToManyField(User, related_name='product_posts')

    def total_likes(self):
        return self.likes.count()

    class Meta:
        ordering = ['date_added']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('product', kwargs={'pk': self.pk
                                          })

    def get_add_to_cart_url(self):
        return reverse('add_to_cart', kwargs={'pk': self.pk
                                              })

    def get_remove_from_cart_url(self):
        return reverse("remove-from-cart", kwargs={
            "pk": self.pk
        })


class OrderProduct(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity}of{self.product.title}"

    def get_total_product_price(self):
        return self.quantity * self.product.price

    def get_discount_product_price(self):
        return self.quantity * self.product.discount_price

    def get_amount_saved(self):
        return self.get_total_product_price() - self.get_discount_product_price()

    def get_final_price(self):
        if self.product.discount_price:
            return self.get_discount_product_price()
        return self.get_total_product_price()


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    products = models.ManyToManyField(OrderProduct)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)
    billing_address = models.ForeignKey(
        'BillingAddress', on_delete=models.SET_NULL, blank=True, null=True)
    payment = models.ForeignKey(
        'Payment', on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.user.username

    def get_total(self):
        total = 0
        for order_product in self.products.all():
            total += order_product.get_final_price()
        return total


class BillingAddress(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    street_address = models.CharField(max_length=100)
    apartment_address = models.CharField(max_length=100)
    #country = CountryField(multiple=False)
    zip = models.CharField(max_length=100)

    def __str__(self):
        return self.user.username


class Payment(models.Model):
    stripe_id = models.CharField(max_length=50)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.SET_NULL, blank=True, null=True)
    amount = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username
