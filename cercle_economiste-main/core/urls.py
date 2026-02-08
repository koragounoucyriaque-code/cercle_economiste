
from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name='index'),
    path('media-db/<str:model>/<int:pk>/<str:field>/', views.blob_image, name='blob_image'),
    path('a-propos/', views.about, name='about'),
    path('actualites/', views.news, name='news'),
    path('membres/', views.members, name='members'),
    path('publications/', views.publications, name='publications'),
    path('contact/', views.contact, name='contact'),
    path('devenir-membre/', views.join, name='join'),
]
