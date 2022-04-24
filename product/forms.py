from django import forms
from .models import Product
#from django_countries.fields import CountryField
#from django_countries.widgets import CountrySelectWidget


#from category.models import Category


#choices = Category.objects.all().values_list('name','name')


#choices_list = []


# for item in choices:
# choices_list.append(item)


PAYMENT = (
    ('S', 'Stripe'),
    ('P', 'PayPal')
)


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('image', 'image_1', 'image_2', 'title', 'price',
                  'discount_price', 'stocks', 'sold', 'discription',)

        widgets = {
            'image': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Type in the Image URL'}),
            'image_1': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Type in the Image URL'}),
            'image_2': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Type in the Image URL'}),
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Title'}),
            'price': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Price'}),
            'discount_price': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'discount_price'}),
            'stocks': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'stocks'}),
            'sold': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'sold'}),
            # 'category': forms.Select(choices=choices_list, attrs={'class': 'form-control', 'placeholder': 'Choose A Category'}),
            'discription': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Type in your post here'}),
        }


class EditForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('image', 'image_1', 'image_2', 'title', 'price',
                  'discount_price', 'stocks', 'sold', 'discription',)

        widgets = {
            'image': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Type in the Image URL'}),
            'image_1': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Type in the Image URL'}),
            'image_2': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Type in the Image URL'}),
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Title'}),
            'price': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Price'}),
            'discount_price': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'discount_price'}),
            'stocks': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'stocks'}),
            'sold': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'sold'}),
            # 'category': forms.Select(choices=choices_list, attrs={'class': 'form-control', 'placeholder': 'Choose A Category'}),
            'discription': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Type in your post here'}),
        }


PAYMENT_CHOICES = (
    ('S', 'Stripe'),
    ('P', 'PayPal'),
    ('C', 'Credit card'),
    ('D', 'Debit card'),
)


class CheckoutForm(forms.Form):
    street_address = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': '1234 Main St'
    }))

    apartment_address = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Apartment or suite'
    }))

    zip = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control d-block w-100'
    }))

    same_billing_address = forms.BooleanField(
        widget=forms.CheckboxInput(), required=False)
    save_info = forms.BooleanField(
        widget=forms.CheckboxInput(), required=False)
    payment_option = forms.ChoiceField(
        widget=forms.RadioSelect, choices=PAYMENT_CHOICES)
