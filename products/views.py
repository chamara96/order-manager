from django.core.paginator import Paginator
from django.db.models import Count
from django.shortcuts import redirect, render
from rest_framework.decorators import api_view
from rest_framework.response import Response

from base.models import HomeSlider, Section, SectionType
from carts.cart_service import CartService
from products.models import Category, Product, ProductImage, ProductType

from .serializers import ProductSerializer


def index(request):
    home_sliders = HomeSlider.objects.filter(is_active=True)
    product_categories = Category.objects.all()
    product_popular_categories = Category.objects.annotate(
        product_count=Count("products")
    ).filter(product_count__gt=0)
    products = Product.objects.all()
    section_settings = Section.objects.filter(is_active=True)
    product_types = ProductType.objects.all()

    trending_products = Product.objects.filter(trending=True).prefetch_related("images")
    context = {
        "home_slider_data": home_sliders,
        "product_categories": product_categories,
        "product_popular_categories": product_popular_categories,
        "products": products,
        "trending_products": trending_products,
        "product_types": product_types,
        "section_settings": {
            SectionType.NEW_COLLECTION: section_settings.filter(
                type=SectionType.NEW_COLLECTION
            ).first(),
            SectionType.SERVICES: section_settings.filter(type=SectionType.SERVICES),
            SectionType.WHY_WITH_US: section_settings.filter(
                type=SectionType.WHY_WITH_US
            ),
        },
    }
    return render(request, "pages/index/index.html", context)


def shop(request):
    category_slug = request.GET.get("category")
    type_slug = request.GET.get("type")
    orderby = request.GET.get("orderby", "order")

    if orderby not in ["created_at", "-created_at", "price", "-price"]:
        orderby = "order"

    product_categories = (
        Category.objects.annotate(product_count=Count("products"))
        .filter(product_count__gt=0)
        .order_by("order")
        .only("name", "slug")
    )
    product_types = (
        ProductType.objects.annotate(product_count=Count("products"))
        .filter(product_count__gt=0)
        .only("name", "slug")
    )
    products = (
        Product.objects.all()
        .order_by(orderby)
        .prefetch_related("images", "categories", "types")
    )

    if category_slug:
        products = products.filter(categories__slug=category_slug)

    if type_slug:
        products = products.filter(types__slug=type_slug).distinct()

    # Paginate
    paginator = Paginator(products, 8)  # Show 8 products per page
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "product_categories": product_categories,
        "products": page_obj,
        "product_types": product_types,
        # 'page_obj': page_obj,
    }
    return render(request, "pages/shop.html", context)


from django.http import Http404


def product_detail(request, slug):
    if request.method == "POST":
        product_id = request.POST.get("productid")
        quantity = request.POST.get("quantity", 1)
        try:
            quantity = int(quantity)
        except ValueError:
            quantity = 1

        CartService(request).add(product_id, quantity)
        return redirect("products:shop")
    try:
        product = Product.objects.prefetch_related("images", "categories").get(
            slug=slug
        )
    except Product.DoesNotExist:
        raise Http404("Product not found")

    context = {
        "product": product,
    }
    return render(request, "pages/product-details.html", context)
