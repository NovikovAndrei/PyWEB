from django.shortcuts import render
from django.views import View
from django.http import HttpResponse

# class ShopView(View):
#     def get(self, request):
#         context = {'data': [
#             {'name' = "Bell Pepper",
#              'discount': 30,
#              'price_before': 120.00,
#              'price_after': 80.00,
#              'url': 'store/images/product-1.jpg'}
#             ]
#         }
#         return render(request, 'store/shop.html', context)

class ShopView(View):
    def get(self, request):
        context = {'data': [
            {'name': 'Cat Zombie',
             'discount': 30,
             'price_before': 120.00,
             'price_after': 80.00,
             'url': 'store/images/product-1aa.jpg'},

        ]}

        return render(request, 'store/shop.html', context)



class CartView(View):
    def get(self, request):
        return render(request, 'store/cart.html')

class ProductSingleView(View):
    def get(self, request):
        return render(request, 'store/product-single.html')
