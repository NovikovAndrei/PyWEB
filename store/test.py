from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APIRequestFactory
from rest_framework import status

from .models import Cart, Product, Category, Wishlist
from .serializers import CartSerializer, WishlistSerializer
from .views import CartViewSet, WishlistViewSet


class CartViewSetTestCase(TestCase):
    fixtures = ['testdata.json']

    def setUp(self):
        # self.factory = APIRequestFactory()
        # self.user = User.objects.create_user(username='testuser', password='testpassword')
        # category = Category.objects.create(name="Vegetables")
        # self.product = Product.objects.create(name='Test Product', description='Test Description',
        #                                       price=10.0, category=category)
        self.factory = APIRequestFactory()
        self.user = User.objects.first()
        self.product = Product.objects.first()

    def test_create_cart_item(self):
        request = self.factory.post('/carts/', {'product': self.product.id})
        request.user = self.user
        view = CartViewSet.as_view({'post': 'create'})

        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['message'], 'Product added to cart')
        self.assertEqual(Cart.objects.count(), 1)

    def test_update_cart_item(self):
        cart_item = Cart.objects.create(user=self.user, product=self.product)
        request = self.factory.put(f'/carts/{cart_item.id}/', {'quantity': 5})
        request.user = self.user
        view = CartViewSet.as_view({'put': 'update'})

        response = view(request, pk=cart_item.id)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['message'], 'Product change to cart')
        cart_item.refresh_from_db()
        self.assertEqual(cart_item.quantity, 5)

    def test_delete_cart_item(self):
        cart_item = Cart.objects.create(user=self.user, product=self.product)
        request = self.factory.delete(f'/carts/{cart_item.id}/')
        request.user = self.user
        view = CartViewSet.as_view({'delete': 'destroy'})

        response = view(request, pk=cart_item.id)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['message'], 'Product delete from cart')
        self.assertEqual(Cart.objects.count(), 0)


class CartSerializerTestCase(TestCase):
    fixtures = ['testdata.json']

    def setUp(self):
        # self.user = User.objects.create_user(username='testuser', password='testpassword')
        # category = Category.objects.create(name="Vegetables")
        # self.product = Product.objects.create(name='Test Product', description='Test Description',
        #                                       price=10.0, category=category)
        # self.cart_item = Cart.objects.create(user=self.user, product=self.product)
        self.user = User.objects.first()
        self.product = Product.objects.first()
        self.cart_item = Cart.objects.create(user=self.user, product=self.product)

    def test_cart_serializer(self):
        serializer = CartSerializer(instance=self.cart_item)
        expected_data = {
            'id': self.cart_item.id,
            'user': self.user.id,
            'quantity': self.cart_item.quantity,
            'product': self.product.id,
        }
        self.assertEqual(serializer.data, expected_data)

class WishlistSerializerTestCase(TestCase):
    fixtures = ['testdata.json']

    def setUp(self):
        self.user = User.objects.first()
        self.product = Product.objects.first()
        self.wishlist_item = Wishlist.objects.create(user=self.user, product=self.product)

    def test_cart_serializer(self):
        serializer = WishlistSerializer(instance=self.wishlist_item)
        expected_data = {
            'id': self.wishlist_item.id,
            'product_name': self.product.name,
            'user': self.user.id,
            'product': self.product.id,
        }
        self.assertEqual(serializer.data, expected_data)

class WishlistViewSetTestCase(TestCase):
    fixtures = ['testdata.json']

    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = User.objects.first()
        self.product = Product.objects.first()

    def test_create_wishlist_item(self):
        request = self.factory.post('/wishlists/', {'product': self.product.id})
        request.user = self.user
        view = WishlistViewSet.as_view({'post': 'create'})

        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['message'], 'Product added to wishlist')
        self.assertEqual(Wishlist.objects.count(), 1)

    # def test_update_wishlist_item(self):
    #     wishlist_item = Wishlist.objects.create(user=self.user, product=self.product)
    #     request = self.factory.put(f'/carts/{wishlist_item.id}/', {'product': 2})
    #     request.user = self.user
    #     view = WishlistViewSet.as_view({'put': 'update'})
    #
    #     response = view(request, pk=wishlist_item.id)
    #     self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    #     self.assertEqual(response.data['message'], 'Product change to wishlist')
    #     wishlist_item.refresh_from_db()
    #     self.assertEqual(wishlist_item.product, 2)

    def test_delete_wishlist_item(self):
        wishlist_item = Wishlist.objects.create(user=self.user, product=self.product)
        request = self.factory.delete(f'/wishlists/{wishlist_item.id}/')
        request.user = self.user
        view = WishlistViewSet.as_view({'delete': 'destroy'})

        response = view(request, pk=wishlist_item.id)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['message'], 'Product delete from wishlist')
        self.assertEqual(Wishlist.objects.count(), 0)
