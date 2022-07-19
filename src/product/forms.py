from django.forms import forms, ModelForm, CharField, TextInput, Textarea, BooleanField, CheckboxInput, SlugField

from product.models import Variant, Product


class VariantForm(ModelForm):
    class Meta:
        model = Variant
        fields = '__all__'
        widgets = {
            'title': TextInput(attrs={'class': 'form-control'}),
            'description': Textarea(attrs={'class': 'form-control'}),
            'active': CheckboxInput(attrs={'class': 'form-check-input', 'id': 'active'})
        }


class ProductForm(forms.Form):
    product_name = CharField(max_length=255)
    product_sku = SlugField(max_length=255)
    product_description = Textarea()
