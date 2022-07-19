import datetime

from django.db.models import Count
from django.shortcuts import render
from django.views import generic
from django.views.generic import ListView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from product.models import Variant, ProductVariantPrice, Product, ProductVariant
from product.forms import VariantForm, ProductForm


class CreateProductView(generic.CreateView):
    template_name = 'products/create.html'
    form_name = ProductForm

    def get_context_data(self, **kwargs):
        print(self.request)
        if self.request.method == "POST":
            print(19, " anjdanjda")
            form = ProductForm(self.request.POST)
            if form.is_valid():
                print(form)
        context = super(CreateProductView, self).get_context_data(**kwargs)
        print(context)
        variants = Variant.objects.filter(active=True).values('id', 'title')
        context['product'] = True
        context['variants'] = list(variants.all())
        print(context)
        return context


def product_list(request):

    all_data = []
    v = ProductVariant.objects.values('variant_title', 'variant__title').order_by('variant__title').annotate(dcount=Count('variant_title'))
    data = {}

    for i in v:
        if i['variant__title'] not in data:
            data[i['variant__title']] = [i['variant_title']]

        else:
            data[i['variant__title']].append(i['variant_title'])
    search = {}

    if request.GET.get('title') != "":
        search['product__title'] = request.GET.get('title')
    if request.GET.get('price_from'):
        search['price__gte'] = float(request.GET.get('price_from'))
    if request.GET.get('price_to'):
        search['price__lte'] = float(request.GET.get('price_to'))
    if request.GET.get('date'):
        date_format = '%Y-%m-%d'
        search['created_at'] = datetime.datetime.strptime(request.GET.get('date'), date_format)

    if search and len(request.GET) == 4:
        # print(search)
        products = ProductVariantPrice.objects.filter(**search)
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
        context = {'products': products, 'variants': data}
        return render(request, 'products/list.html', context=context)


    else:
        products = ProductVariantPrice.objects.all()
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
        context = {'products': products, 'variants': data}
        return render(request, 'products/list.html', context=context)


class BasedProductVariantPriceView(generic.View):
    model = ProductVariantPrice
    template_name = 'products/create.html'
    success_url = '/product/'
