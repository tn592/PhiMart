from django.db.models import Count
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from product.models import Product, Category
from product.serializers import CategorySerializer, ProductSerializer
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView


# Create your views here.


class ViewProducts(APIView):
    def get(self, request):
        products = Product.objects.select_related("category").all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ProductSerializer(data=request.data)  # Deserializer
        serializer.is_valid(raise_exception=True)
        print(serializer.validated_data)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ProductList(ListCreateAPIView):
    queryset = Product.objects.select_related("category").all()
    serializer_class = ProductSerializer

    # def get_queryset(self):
    #     return Product.objects.select_related("category").all()

    # def get_serializer_class(self):
    #     return ProductSerializer

    # def get_serializer_context(self):
    #     return {"request": self.request}


class ViewSpecificProduct(APIView):
    def get(self, request, id):
        product = get_object_or_404(Product, pk=id)
        serializer = ProductSerializer(product)
        return Response(serializer.data)

    def put(self, request, id):
        product = get_object_or_404(Product, pk=id)
        serializer = ProductSerializer(product, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, id):
        product = get_object_or_404(Product, pk=id)
        copy_of_product = product
        product.delete()
        serializer = ProductSerializer(copy_of_product)
        return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)


class ViewCategories(APIView):
    def get(self, reqeust):
        categories = Category.objects.annotate(product_count=Count("products")).all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CategorySerializer(data=request.data)  # Deserializer
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CategoryList(ListCreateAPIView):
    queryset = Category.objects.annotate(product_count=Count("products")).all()
    serializer_class = CategorySerializer


class ViewSpecificCategory(APIView):
    def get(self, request, pk):
        category = get_object_or_404(
            Category.objects.annotate(product_count=Count("products")).all(), pk=pk
        )
        serializer = CategorySerializer(category)
        return Response(serializer.data)

    def put(self, request, pk):
        category = get_object_or_404(
            Category.objects.annotate(product_count=Count("products")).all(), pk=pk
        )
        serializer = CategorySerializer(category, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, pk):
        category = get_object_or_404(
            Category.objects.annotate(product_count=Count("products")).all(), pk=id
        )
        copy_of_category = category
        category.delete()
        serializer = ProductSerializer(copy_of_category)
        return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)
