from django.urls import URLPattern, path
from . import views
urlpatterns = [
    path ('', views.index, name='home'),
    path ('booking/', views.booking, name='booking'),
    path ('one_day_booking/', views.one_day_booking, name='one_day_booking'),
    path ('contact/', views.contact, name='contact'),
    # # path ('warning/', views.warning, name='warning'),
    # path ('blogs/', views.blog, name='blog'),
    path ('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
]