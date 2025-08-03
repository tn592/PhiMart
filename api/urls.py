from django.urls import path, include
from rest_framework.routers import DefaultRouter, SimpleRouter
from product.views import CategoryViewSet, ProductViewSet, ReviewViewSet
from rest_framework_nested import routers


# router = SimpleRouter()
# router = DefaultRouter()
router = routers.DefaultRouter()
router.register("products", ProductViewSet, basename="products")
router.register("categories", CategoryViewSet)

product_router = routers.NestedDefaultRouter(router, "products", lookup="product")
product_router.register("reviews", ReviewViewSet, basename="product-review")

urlpatterns = [path("", include(router.urls)), path("", include(product_router.urls))]

# urlpatterns = router.urls

# urlpatterns = [
#     path("products/", include("product.product_urls")),
#     path("categories/", include("product.category_urls")),
# ]
