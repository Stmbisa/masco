from django.urls import URLPattern, path
from . import views
urlpatterns = [
    path ('', views.index, name='home'),
    # path ('about/', views.about, name='about'),
    path ('contact/', views.contact, name='contact'),
    # # path ('warning/', views.warning, name='warning'),
    # path ('blogs/', views.blog, name='blog'),
    path ('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
]