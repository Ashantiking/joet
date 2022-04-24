from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.shortcuts import render, get_object_or_404
from django.urls.base import reverse, reverse_lazy
from django.shortcuts import redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView,  View
from django.utils import timezone
#from shopping_cart.models import Order
from .models import Product, OrderProduct, Order, BillingAddress
#from category.models import Category
from .forms import ProductForm, CheckoutForm, EditForm
# Create your views here.


# def product_list(request):
#    object_list = Product.objects.all()
#    filtered_orders = Order.objects.filter(owner=request.user.profile, is_ordered)
#    current_order_products = []
#    if filtered_orders.exists():
#        user_order = filtered_orders[0]
#        user_order_items = user_order.all()
#        current_order_products = [product.product for product in product user_order_items]

#    context = {
#        'object_list': object_list,
#        'current_order_products': current_order_products
#    }
#    return render(request, "products/pro", context)

class HomeView(ListView):
    model = Product
    template_name = 'product/index.html'
    paginate_by = 4
    ordering = ['-date_added']
    success_url = reverse_lazy('product')


class ProductView(ListView):
    model = Product
    template_name = 'product/shop-grid.html'
    paginate_by = 12
    ordering = ['-date_added']
    success_url = reverse_lazy('product')



class ProductDetailView(DetailView):
    model = Product
    template_name = 'product/shop-details.html'
    success_url = reverse_lazy('product')

    def get_context_data(self, *args, **kwargs):
        #        cat_menu = Category.objects.all()
        context = super(ProductDetailView, self).get_context_data()

        stuff = get_object_or_404(Product, id=self.kwargs['pk'])
        total_likes = stuff.total_likes()
        #context["cat_menu"] = cat_menu
        context["total_likes"] = total_likes
        return context


def add_to_cart(request, pk):
    product = get_object_or_404(Product, pk=pk)
    order_product, created = OrderProduct.objects.get_or_create(
        product=product,
        user=request.user,
        ordered=False
    )
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
# check if the order item is in the order
        if order.products.filter(product__pk=product.pk).exists():
            order_product.quantity += 1
            order_product.save()
            messages.info(request, "Product \"" +
                          order_product.product.title+"\" was updated.")
            return redirect("order-summary")
        else:
            messages.info(request, "Product \"" +
                          order_product.product.title+"\" Added to your cart")
            order.products.add(order_product)
            return redirect("order-summary")
    else:
        order_date = timezone.now()
        order = Order.objects.create(
            user=request.user, ordered_date=order_date)
        order.product.add(order_product)
        messages.info(request, "Product \"" +
                      order_product.product.title+"\" Added to your cart")
        return redirect("order-summary")


def remove_from_cart(request, pk):
    product = get_object_or_404(Product, pk=pk)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
# check if the order item is in the order
        if order.products.filter(product__pk=product.pk).exists():
            order_product = OrderProduct.objects.filter(
                product=product,
                user=request.user,
                ordered=False
            )[0]
            order.products.remove(order_product)
            messages.info(request, "Product \"" +
                          order_product.product.title+"\" removed from your cart")
            return redirect("order-summary")
        else:
            # Add a Message saying the user doesnt have an order
            messages.info(request, "This Item was not in your cart")
            return redirect("order-summary")
    else:
        # Add a Message saying the user doesnt have an order
        messages.info(request, "You do not have an Active Order in your cart")
        return redirect("order-summary")

    return redirect("order-summary")


def remove_single_product_from_cart(request, pk):
    product = get_object_or_404(Product, pk=pk)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
# check if the order item is in the order
        if order.products.filter(product__pk=product.pk).exists():
            order_product = OrderProduct.objects.filter(
                product=product,
                user=request.user,
                ordered=False
            )[0]
            if order_product.quantity > 1:
                order_product.quantity -= 1
                order_product.save()
            else:
                order.products.remove(order_product)
            messages.info(request, "Product \"" +
                          order_product.product.title+"\" quantity was update")
            return redirect("order-summary")
        else:
            # Add a Message saying the user doesnt have an order
            messages.info(request, "This Item was not in your cart")
            return redirect("product", pk=pk)
    else:
        # Add a Message saying the user doesnt have an order
        messages.info(request, "You do not have an Active Order in your cart")
        return redirect("product", pk=pk)

    return redirect("product")


class NewProductView(CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'product/new_product.html'
    #success_url = reverse_lazy('product')

# class AddCategoryView(CreateView):
    #model = Category
    #form_class = ProductForm
    #template_name = 'add_category.html'
    #fields = '__all__'


class UpdateProductView(UpdateView):
    model = Product
    form_class = EditForm
    template_name = 'product/update_product.html'
    success_url = reverse_lazy('product')


class UpdateAddToCartView(UpdateView):
    model = Product
    form_class = EditForm
    template_name = 'product/update_product.html'
    success_url = reverse_lazy('product')


def wishlist(request):
    return render(request, 'product/wishlist.html', {})


class OrderSummaryView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            context = {
                'object': order
            }
            return render(self.request, 'product/order_summary.html', context)
        except ObjectDoesNotExist:
            messages.error(self.request, "You do not have an active order")
            return redirect("/")


class CheckoutView(View):
    def get(self, *args, **kwargs):
        form = CheckoutForm()
        order = Order.objects.get(user=self.request.user, ordered=False)
        context = {
            'form': form,
            #            'order': order
        }
        return render(self.request, 'product/checkout.html', context)

    def post(self, *args, **kwargs):
        form = CheckoutForm(self.request.POST or None)
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            if form.is_valid():
                street_address = form.cleaned_data.get('street_address')
                apartment_address = form.cleaned_data.get('apartment_address')
                country = form.cleaned_data.get('country')
                zip = form.cleaned_data.get('zip')
                # TODO: add functionaly for these fields
                #same_billing_address = form.cleaned_data.get('same_billing_address')
                #save_info = form.cleaned_data.get('save_info')
                payment_option = form.cleaned_data.get('payment_option')
                billing_address = BillingAddress(
                    user=self.request.user,
                    street_address=street_address,
                    apartment_address=apartment_address,
                    country=country,
                    zip=zip
                )
                billing_address.save()
                order.billing_address = billing_address
                order.save()

#                if payment_option == 'S':
#                    return redirect('payment', payment_option='stripe')
#                elif payment_option == 'P':
#                    return redirect('payment', payment_option='paypal')
#                else:
            messages.warning(self.request, "Invalid Payment option")
            return redirect('checkout')
        except ObjectDoesNotExist:
            messages.error(self.request, "You do not have an order")
            return redirect("order-summary")


class PaymentView(View):
    def get(self, *args, **kwargs):
        order = Order.objects.get(user=self.request.user, ordered=False)
        context = {
            'order': order
        }
        return render(self.request, "product/payment.html", context)

    def post(self, *args, **kwargs):
        order = Order.objects.get(user=self.request.user, ordered=False)
        token = self.request.POST.get('stripeToken')
        amount = int(order.get_total_price() * 100)  # cents

        try:
            charge = stripe.Charge.create(
                amount=amount,
                currency="usd , naria",
                source=token
            )

            # create payment
            payment = Payment()
            payment.stripe_id = charge['id']
            payment.user = self.request.user
            payment.amount = order.get_total_price()
            payment.save()

            # assign payment to order
            order.ordered = True
            order.payment = payment
            order.save()

            messages.success(self.request, "Success make an order")
            return redirect('/')

        except stripe.error.CardError as e:
            body = e.json_body
            err = body.get('error', {})
            messages.error(self.request, f"{err.get('message')}")
            return redirect('/')

        except stripe.error.RateLimitError as e:
            # Too many requests made to the API too quickly
            messages.error(self.request, "To many request error")
            return redirect('/')

        except stripe.error.InvalidRequestError as e:
            # Invalid parameters were supplied to Stripe's API
            messages.error(self.request, "Invalid Parameter")
            return redirect('/')

        except stripe.error.AuthenticationError as e:
            # Authentication with Stripe's API failed
            # (maybe you changed API keys recently)
            messages.error(self.request, "Authentication with stripe failed")
            return redirect('/')

        except stripe.error.APIConnectionError as e:
            # Network communication with Stripe failed
            messages.error(self.request, "Network Error")
            return redirect('/')

        except stripe.error.StripeError as e:
            # Display a very generic error to the user, and maybe send
            # yourself an email
            messages.error(self.request, "Something went wrong")
            return redirect('/')

        except Exception as e:
            # Something else happened, completely unrelated to Stripe
            messages.error(self.request, "Not identified error")
            return redirect('/')


# @login_required
# def add_to_cart(request, pk):
#    product = get_object_or_404(Product, pk=pk)
#    order_product, created = OrderProduct.objects.get_or_create(
#        product=product,
#        user=request.user,
#        ordered=False
#    )
#    order_qs = Order.objects.filter(user=request.user, ordered=False)

#    if order_qs.exists():
#        order = order_qs[0]

#        if order.products.filter(product__pk=product.pk).exists():
#            order_product.quantity += 1
#            order_product.save()
#            messages.info(request, "Added quantity Product")
#            return redirect("order-summary")
#        else:
#            order.products.add(order_product)
#            messages.info(request, "Product added to your cart")
#            return redirect("order-summary")
#    else:
#        ordered_date = timezone.now()
#        order = Order.objects.create(
#            user=request.user, ordered_date=ordered_date)
#        order.products.add(order_product)
#        messages.info(request, "Product added to your cart")
#        return redirect("order-summary")


# @login_required
# def remove_from_cart(request, pk):
#    product = get_object_or_404(Product, pk=pk)
#    order_qs = Order.objects.filter(
#        user=request.user,
#        ordered=False
#    )
#    if order_qs.exists():
#        order = order_qs[0]
#        if order.products.filter(product__pk=product.pk).exists():
#            order_product = OrderProduct.objects.filter(
#                product=product,
#                user=request.user,
#                ordered=False
#            )[0]
#            order_product.delete()
#            messages.info(request, "Product \"" +
#                          order_product.product.title+"\" remove from your cart")
#            return redirect("order-summary")
#        else:
#            messages.info(request, "This Item not in your cart")
#            return redirect("product", pk=pk)
#    else:
        # add message doesnt have order
#        messages.info(request, "You do not have an Order")
#        return redirect("product", pk=pk)


# @login_required
# def reduce_quantity_item(request, pk):
#    item = get_object_or_404(Product, pk=pk)
#    order_qs = Order.objects.filter(
#        user=request.user,
#        ordered=False
#    )
#    if order_qs.exists():
#        order = order_qs[0]
#        if order.items.filter(item__pk=item.pk).exists():
#            order_item = OrderItem.objects.filter(
#                item=item,
#                user=request.user,
#                ordered=False
#            )[0]
#            if order_item.quantity > 1:
#                order_item.quantity -= 1
#                order_item.save()
#            else:
#                order_item.delete()
#            messages.info(request, "Item quantity was updated")
#            return redirect("core:order-summary")
#        else:
#            messages.info(request, "This Item not in your cart")
#            return redirect("core:order-summary")
#    else:
        # add message doesnt have order
#        messages.info(request, "You do not have an Order")
#        return redirect("core:order-summary")
