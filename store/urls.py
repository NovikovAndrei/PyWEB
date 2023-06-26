from django.urls import path
from rest_framework import routers
from .views import ShopView, CartView, ProductSingleView, CartViewSet, WishlistView, WishlistViewSet


router = routers.DefaultRouter()
router.register(r'cart', CartViewSet)
router.register(r'wishlist', WishlistViewSet)

app_name = 'store'
wishlist_view = WishlistView.as_view()

urlpatterns = [
    path('', ShopView.as_view(), name='shop'),
    path('cart/', CartView.as_view(), name='cart'),
    path('product/<int:id>/', ProductSingleView.as_view(), name='product'),
    path('wishlist', WishlistView.as_view(), name='wishlist'),
    # path('wishlist/remove/<int:id>/', WishlistRemoveView.as_view(), name='remove_from_wishlist'),
    # path('wishlist/add/<int:id>/', WishlistAddView.as_view(), name='add_to_wishlist'),
    path('wishlist/remove/<int:id>/', WishlistView.as_view(), {'method': 'remove'}, name='remove_from_wishlist'),
    path('wishlist/add/<int:id>/', WishlistView.as_view(), {'method': 'add'}, name='add_to_wishlist'),
]