from django.shortcuts import render
from base.models import HomeSlider
from products.models import Category, Tag, ProductType, Product, ProductImage
from django.db.models import Count
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import ProductSerializer
from django.core.paginator import Paginator


def index(request):
    home_sliders = HomeSlider.objects.filter(is_active=True)
    product_categories = Category.objects.all()
    product_popular_categories = Category.objects.annotate(
        product_count=Count("products")
    ).filter(product_count__gt=0)
    products = Product.objects.all()
    products_popular = Product.objects.filter(is_popular=True).prefetch_related(
        "images"
    )
    products_deal = Product.objects.filter(is_deal=True).prefetch_related("images")
    context = {
        "home_slider_data": home_sliders,
        "product_categories": product_categories,
        "product_popular_categories": product_popular_categories,
        "products": products,
        "products_popular": products_popular,
        "products_deal": products_deal,
    }
    return render(request, "index.html", context)


def shop(request):
    category_slug = request.GET.get("category")
    tags_slugs = request.GET.get("tags", "").split(",")

    product_categories = (
        Category.objects.annotate(product_count=Count("products"))
        .filter(product_count__gt=0)
        .order_by("order")
        .only("name", "slug")
    )
    product_tags = (
        Tag.objects.annotate(product_count=Count("products"))
        .filter(product_count__gt=0)
        .order_by("name")
        .only("name", "slug")
    )
    products = Product.objects.all()

    if category_slug:
        products = products.filter(categories__slug=category_slug)

    if tags_slugs and tags_slugs != [""]:
        products = products.filter(tags__slug__in=tags_slugs).distinct()

    # Paginate
    paginator = Paginator(products, 8)  # Show 12 products per page
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "product_categories": product_categories,
        "product_tags": product_tags,
        "products": page_obj,
        # 'page_obj': page_obj,
    }
    return render(request, "shop.html", context)

def cart(request):
    
    products = Product.objects.all()

    context = {
        "products": products,
    }
    return render(request, "cart.html", context)


@api_view(["GET"])
def product_detail(request, pk):
    try:
        product = Product.objects.prefetch_related("images", "categories").get(pk=pk)
    except Product.DoesNotExist:
        return Response({"error": "Product not found"}, status=404)

    serializer = ProductSerializer(product)
    return Response(serializer.data)
