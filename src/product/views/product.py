import datetime

from django.shortcuts import render
from django.views import generic

from product.models import Variant
from product.models import *


class CreateProductView(generic.TemplateView):
    template_name = 'products/create.html'

    def get_context_data(self, **kwargs):
        context = super(CreateProductView, self).get_context_data(**kwargs)
        variants = Variant.objects.filter(active=True).values('id', 'title')
        context['product'] = True
        context['variants'] = list(variants.all())
        print(context['view'])
        return context


def product_list(request):
    products = ProductVariantPrice.objects.all()
    all_data = []


    for i in products:
        p = {}
        # print(i.__dict__)
        p['id'] = i.id
        p['created_at'] = abs(datetime.datetime.now(datetime.timezone.utc) - i.created_at).days*24
        p['price'] = i.price
        p['stock'] = i.stock
        if i.product_variant_one_id is not None:
            p['product_variant_one_title'] = i.product_variant_one.variant_title
        if i.product_variant_two_id is not None:
            p['product_variant_two_title'] = i.product_variant_two.variant_title
        if i.product_variant_three_id is not None:
            p['product_variant_three_title'] = i.product_variant_three.variant_title
        p['description'] = i.product.description
        p['product_title'] = i.product.title
        all_data.append(p)

    context = {'products': all_data}
    return render(request, 'products/list.html', context=context)
