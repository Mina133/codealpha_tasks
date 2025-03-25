from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register_user, name='register'),
    path('event/<int:event_id>/', views.event_detail, name='event_detail'),
    path('event/<int:event_id>/register/', views.register_for_event, name='register_for_event'),
    path('my-registrations/', views.my_registrations, name='my_registrations'),
    path('cancel-registration/<int:registration_id>/', views.cancel_registration, name='cancel_registration'),
    path('create-event/', views.create_event, name='create_event'),
] 