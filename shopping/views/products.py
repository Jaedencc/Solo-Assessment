from django.shortcuts import redirect, render, get_object_or_404
from django.utils import timezone
from shopping.forms import ProductForm
from shopping.models import Product, Country
from django.db.models import Count
import plotly.express as px
import plotly.io as pio

"""def product_list(request):                     # no search function
    products = Product.objects.all()    
    return render(request, 'shopping/product_list.html', {'products' : products })"""

def product_list(request):
    brand_query = request.GET.get('brand', '')    # get the brand name for the url
    if brand_query:  
        products = Product.objects.filter(brand__icontains=brand_query)  # achieve case insensitive search
    else:
        products = Product.objects.all()          # if there is no that brand, present all product
    return render(request, 'shopping/product_list.html', {'products': products})


def product_new(request):
    if request.method=="POST":
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save(commit=False)    
            product.created_date = timezone.now()
            product.save()
            return redirect('shopping:product_list')
    else:
        form = ProductForm()
    return render(request, 'shopping/product_edit.html', {'form': form})


def product_edit(request, id):
    product = get_object_or_404(Product, id=id)
    if request.method=="POST":
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            product = form.save(commit=False)
            product.created_date = timezone.now()
            product.save()
            return redirect('shopping:product_list')
    else:
        form = ProductForm(instance=product)
    return render(request, 'shopping/product_edit.html', {'form': form})


def product_delete(request, id):
    product = get_object_or_404(Product, id=id)
    deleted = request.session.get('deleted', 'empty')
    request.session['deleted'] = product.name
    product.delete()
    return redirect('shopping:product_list' )


def product_detail(request, id):
    product = get_object_or_404(Product, id=id)
    return render(request, 'shopping/product_detail.html', {'product' : product})


def brand_chart(request):
    data = Product.objects.values('brand').annotate(count=Count('id')).order_by('-count')
    brands = [item['brand'] for item in data]
    counts = [item['count'] for item in data]

    figure = px.bar(x=brands, y=counts, labels={'x': 'Brand', 'y': 'Number of Products'}, title='Number of Products by Brand')    # Generate a bar chart using Plotly（inspired by the example of https://plotly.com/python/bar-charts/）
    barChart_html = pio.to_html(figure, full_html=False)                                                                          # Convert the Plotly figure to HTML

    return render(request, 'shopping/brand_chart.html', {'barChart_html': barChart_html})