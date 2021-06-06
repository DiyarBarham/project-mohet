from django.urls import path
from . import views
urlpatterns = [
    path('', views.index),
    path('articles', views.articles),
    path('about', views.about),
    path('contact', views.contact),
    path('rigesterwithus', views.rigesterwithus),
    path('rigesterwith', views.rigesterwith),
    path('contact_us',views.contact_us),
    path('articles/<int:id>',views.image)
]