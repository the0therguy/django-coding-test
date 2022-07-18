import datetime

from django.shortcuts import render
from django.views import generic
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
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
        p = {'id': i.id, 'created_at': abs(datetime.datetime.now(datetime.timezone.utc) - i.created_at).days * 24,
             'price': i.price, 'stock': i.stock}
        if i.product_variant_one_id is not None:
            p['product_variant_one_title'] = i.product_variant_one.variant_title
        if i.product_variant_two_id is not None:
            p['product_variant_two_title'] = i.product_variant_two.variant_title
        if i.product_variant_three_id is not None:
            p['product_variant_three_title'] = i.product_variant_three.variant_title
        p['description'] = i.product.description
        p['product_title'] = i.product.title
        all_data.append(p)

    page = request.GET.get('page', 1)

    paginator = Paginator(all_data, 5)
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)
    context = {'products': products}
    return render(request, 'products/list.html', context=context)
