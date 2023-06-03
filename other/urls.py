from django.urls import path
from .views import CurrentDateView, RandomNumber, IndexView, HelloWorld


urlpatterns = [
    path('', IndexView.as_view()),
    path('datetime/', CurrentDateView.as_view()),
    path('hello/', HelloWorld.as_view()),
    path('randomnum/', RandomNumber.as_view()),

]