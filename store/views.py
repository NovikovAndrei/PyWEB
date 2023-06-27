from django.shortcuts import render
from django.views import View
from django.http import HttpResponse
from django.db.models import OuterRef, Subquery, F, ExpressionWrapper, DecimalField, Case, When
from django.utils import timezone
from .models import Product, Discount, Cart, Wishlist
from rest_framework import viewsets, response
from rest_framework.permissions import IsAuthenticated
from .serializers import CartSerializer, WishlistSerializer
from django.shortcuts import get_object_or_404, redirect

class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        cart_items = self.get_queryset().filter(product__id=request.data.get('product'))
        if cart_items:
            cart_item = cart_items[0]
            if request.data.get('quantity'):
                cart_item.quantity += int(request.data.get('quantity'))
            else:
                cart_item.quantity += 1
        else:
            product = get_object_or_404(Product, id=request.data.get('product'))
            if request.data.get('quantity'):
                cart_item = Cart(user=request.user, product=product, quantity=request.data.get('quantity'))
            else:
                cart_item = Cart(user=request.user, product=product)
        cart_item.save()
        return response.Response({'message': 'Product added to cart'}, status=201)

    def update(self, request, *args, **kwargs):
        cart_item = get_object_or_404(Cart, id=kwargs['pk'])
        if request.data.get('quantity'):
            cart_item.quantity = request.data['quantity']
        if request.data.get('product'):
            product = get_object_or_404(Product, id=request.data['product'])
            cart_item.product = product
        cart_item.save()
        return response.Response({'message': 'Product change to cart'}, status=201)

    def destroy(self, request, *args, **kwargs):
        cart_item = self.get_queryset().get(id=kwargs['pk'])
        cart_item.delete()
        return response.Response({'message': 'Product delete from cart'}, status=201)



class ShopView(View):
    def get(self, request):
        discount_value = Case(When(discount__value__gte=0,
                                   discount__date_begin__lte=timezone.now(),
                                   discount__date_end__gte=timezone.now(),
                                   then=F('discount__value')),
                              default=0,
                              output_field=DecimalField(max_digits=10, decimal_places=2)
                              )

        price_with_discount = ExpressionWrapper(
            F('price') * (100.0 - F('discount_value')) / 100.0,
            output_field=DecimalField(max_digits=10, decimal_places=2)
        )

        products = Product.objects.annotate(
            discount_value=discount_value,
            price_before=F('price'),
            price_after=price_with_discount
        ).values('id', 'name', 'image', 'price_before',  'price_after',
                 'discount_value')

        return render(request, 'store/shop.html', {'data': products})


class CartView(View):
    def get(self, request):
        return render(request, 'store/cart.html')

class ProductSingleView(View):
    def get(self, request, id):
        data = Product.objects.get(id=id)
        return render(request, 'store/product-single.html',
                      context={'name': data.name,
                               'description': data.description,
                               'price': data.price,
                               'rating': 5.0,
                               'url': data.image.url,
                               })

# class WishlistView(View):
#     def get(self, request):
#         if request.user.is_authenticated:
#             wishlist = Wishlist.objects.filter(user=request.user)
#             return render(request, "store/wishlist.html", {'wishlist': wishlist})
#         return redirect('login:login')
#
# class WishlistRemoveView(View):
#     def get(self, request, id):
#         product = get_object_or_404(Product, id=id)
#         wishlist_item = Wishlist.objects.filter(user=request.user, product=product)
#         wishlist_item.delete()
#         return redirect('store:wishlist')
#
#
# class WishlistAddView(View):
#     def get(self, request, id):
#         product = get_object_or_404(Product, id=id)
#         wishlist_item = Wishlist.objects.filter(user=request.user, product=product)
#
#         if wishlist_item.exists():
#             return redirect('store:shop')
#         else:
#             wishlist_item = Wishlist(user=request.user, product=product)
#             wishlist_item.save()
#             return redirect('store:shop')

class WishlistView(View):
    def get(self, request):
        if request.user.is_authenticated:
            wishlist = Wishlist.objects.filter(user=request.user)
            return render(request, "store/wishlist.html", {'wishlist': wishlist})
        return redirect('login:login')

    def post(self, request, id):
        # Логика для добавления товара в список желаний
        if request.user.is_authenticated:
            product = get_object_or_404(Product, id=id)
            wishlist_item = Wishlist.objects.filter(user=request.user, product=product)

            if wishlist_item.exists():
                return redirect('store:shop')
            else:
                wishlist_item = Wishlist(user=request.user, product=product)
                wishlist_item.save()
                return redirect('store:shop')
        return redirect('login:login')

    def delete(self, request, id):
        # Логика для удаления товара из списка желаний
        product = get_object_or_404(Product, id=id)
        wishlist_item = Wishlist.objects.filter(user=request.user, product=product)
        wishlist_item.delete()
        return redirect('store:wishlist')

    def dispatch(self, request, *args, **kwargs):
        if 'method' in kwargs:
            if kwargs['method'] == 'remove':
                return self.delete(request, id=kwargs['id'])
            elif kwargs['method'] == 'add':
                return self.post(request, id=kwargs['id'])
        return super().dispatch(request, *args, **kwargs)


class WishlistViewSet(viewsets.ModelViewSet):
    queryset = Wishlist.objects.all()
    serializer_class = WishlistSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        wishlist_items = self.get_queryset().filter(product__id=request.data.get('product'))
        if wishlist_items:
            wishlist_item = wishlist_items[0]
        else:
            product = get_object_or_404(Product, id=request.data.get('product'))
            wishlist_item = Wishlist(user=request.user, product=product)
        wishlist_item.save()
        return response.Response({'message': 'Product added to wishlist'}, status=201)

    def update(self, request, *args, **kwargs):
        wishlist_item = get_object_or_404(Wishlist, id=kwargs['pk'])
        if request.data.get('product'):
            product = get_object_or_404(Product, id=request.data['product'])
            wishlist_item.product = product
        wishlist_item.save()
        return response.Response({'message': 'Product change to wishlist'}, status=201)

    def destroy(self, request, *args, **kwargs):
        wishlist_item = self.get_queryset().get(id=kwargs['pk'])
        wishlist_item.delete()
        return response.Response({'message': 'Product delete from wishlist'}, status=201)
