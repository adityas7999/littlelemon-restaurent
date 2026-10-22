from django.urls import path

from . import views


urlpatterns = [
    # HTML template routes (serving static content & templates)
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('book/', views.book, name='book'),
    path('reservations/', views.reservations, name='reservations'),
    path('menu/', views.menu, name='menu'),
    path('menu_item/<int:pk>/', views.display_menu_item, name='menu_item'),
    path('register/', views.register_page, name='register'),
    path('bookings', views.bookings_api, name='bookings'),
    path('bookings/', views.bookings_api, name='bookings-slash'),

    # REST API Menu routes
    path('menu-items/', views.MenuItemsView.as_view(), name='menu-items'),
    path('menu-items/<int:pk>/', views.SingleMenuItemView.as_view(), name='single-menu-item'),
    path('api/menu-items/', views.MenuItemsView.as_view(), name='api-app-menu-items'),
    path('api/menu-items/<int:pk>/', views.SingleMenuItemView.as_view(), name='api-app-single-menu-item'),
]
