from django.urls import path
from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name = 'index'),
    
    path('restaurants', views.RestaurantList.as_view(), name = 'restaurants'),
    path('restaurant/<int:pk>/', views.RestaurantDetail.as_view(), name = 'restaurant'),
    path('add_restaurant/', views.RestaurantCreateView.as_view(), name = 'addRestaurant'),

    path('review/<int:pk>/', views.ReviewDetail.as_view(), name = 'review'),

    path('success/', views.SuccessView.as_view(), name = 'success'),
]