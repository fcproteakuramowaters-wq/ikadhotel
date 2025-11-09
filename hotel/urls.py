from django.urls import path
from . import views

urlpatterns = [
    path('confirm-booking/', views.confirm_booking, name='confirm_booking'),
    path('', views.home, name='home'),
    path('hotels/victoria-island/', views.ikad_victoria_island, name='ikad_victoria_island'),
    path('hotels/cooli-hotel/', views.cooli_hotel, name='cooli_hotel'),
    path('contact/', views.contact, name='contact'),
    path('booking/victoria-island/', views.booking_confirmation, {'hotel_type': 'vi'}, name='vi_booking'),
    path('booking/cooli-hotel/', views.booking_confirmation, {'hotel_type': 'bw'}, name='bw_booking'),
    path('booking/process/', views.process_booking, name='process_booking'),
]