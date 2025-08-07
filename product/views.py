from rest_framework.response import Response
from rest_framework import status
from product.models import Product, Category, Review
from product.serializers import ProductSerializer, CategorySerializer, ReviewSerializer
from django.db.models import Count
from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from product.filters import ProductFilter
from rest_framework.filters import SearchFilter, OrderingFilter
from product.paginations import DefaultPagination
from api.permissions import IsAdminOrReadOnly, FullDjangoModelPermission
from rest_framework.permissions import DjangoModelPermissions, DjangoModelPermissionsOrAnonReadOnly
from product.permissions import IsReviewAuthorOrReadonly

# from rest_framework.permissions import IsAdminUser, AllowAny


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ProductFilter
    pagination_class = DefaultPagination
    search_fields = ["name", "description"]
    ordering_fields = ["price", "updated_at"]
    permission_classes = [IsAdminOrReadOnly]
#    permission_classes = [IsAdminUser]
#    permission_classes = [DjangoModelPermissions]
#    permission_classes = [DjangoModelPermissionsOrAnonReadOnly]
#    permission_classes = [FullDjangoModelPermission]

#    def get_permissions(self):
#        if self.request.method == "GET":
#            return [AllowAny()]
#        return [IsAdminUser()]

    def destroy(self, request, *args, **kwargs):
        product = self.get_object()
        if product.stock > 10:
            return Response(
                {"message": "Product with stock more than 10 could not be deleted"}
            )
        self.perform_destroy(product)
        return Response(status=status.HTTP_204_NO_CONTENT)


class CategoryViewSet(ModelViewSet):
    permission_classes = [IsAdminOrReadOnly] 
    queryset = Category.objects.annotate(product_count=Count("products")).all()
    serializer_class = CategorySerializer


class ReviewViewSet(ModelViewSet):
    serializer_class = ReviewSerializer
    permission_class = [IsReviewAuthorOrReadonly]

    def perform_create(self, serializer): 
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        return Review.objects.filter(product_id=self.kwargs["product_pk"])

    def get_serializer_context(self):
        return {"product_id": self.kwargs["product_pk"]}
