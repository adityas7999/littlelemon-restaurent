from django.contrib import admin
from django.urls import include, path
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.routers import DefaultRouter

from restaurant import views


router = DefaultRouter()
router.register(r'tables', views.BookingViewSet, basename='tables')
router.register(r'bookings', views.BookingViewSet, basename='bookings')
router.register(r'users', views.UserViewSet, basename='users')

urlpatterns = [
    # Django Admin
    path('admin/', admin.site.urls),

    # Restaurant HTML & Static Views
    path('', include('restaurant.urls')),
    path('restaurant/', include('restaurant.urls')),

    # Restaurant API Paths (lab conventions)
    path('restaurant/menu/', views.MenuItemsView.as_view(), name='restaurant-menu-list'),
    path('restaurant/menu/<int:pk>/', views.SingleMenuItemView.as_view(), name='restaurant-menu-detail'),
    path('restaurant/booking/', include(router.urls)),

    # Standalone API Paths
    path('api/menu-items/', views.MenuItemsView.as_view(), name='api-menu-items'),
    path('api/menu-items/<int:pk>/', views.SingleMenuItemView.as_view(), name='api-menu-items-detail'),
    path('api/menu/', views.MenuItemsView.as_view(), name='api-menu'),
    path('api/menu/<int:pk>/', views.SingleMenuItemView.as_view(), name='api-menu-detail'),
    path('api/registration/', views.UserRegistrationView.as_view(), name='api-registration'),
    path('api/register/', views.UserRegistrationView.as_view(), name='api-register'),
    path('api-token-auth/', obtain_auth_token, name='api-token-auth'),
    path('api/token/login/', obtain_auth_token, name='api-token-login'),

    # ViewSet Router Paths
    path('api/', include(router.urls)),
    path('booking/', include(router.urls)),

    # Djoser Authentication Endpoints
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
    path('api/auth/', include('djoser.urls')),
    path('api/auth/', include('djoser.urls.authtoken')),
]
