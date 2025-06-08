from rest_framework import serializers
from .models import Product, ProductImage, Category, Tag, ProductType


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ["image"]


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["name", "slug"]
        ordering = ["name"]

class ProductTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductType
        fields = ["name"]

class ProductTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ["name", "slug"]


class ProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, read_only=True)
    categories = CategorySerializer(many=True, read_only=True)
    tags = ProductTagSerializer(many=True, read_only=True)
    types = ProductTypeSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "slug",
            "description",
            "price",
            "price_formatted",
            "sku",
            "stock",
            "categories",
            "tags",
            "types",
            "is_popular",
            "is_deal",
            "discount_precent",
            "discount_price",
            "calc_discount_price",
            "calc_discount_price_formatted",
            "images",
            
        ]
