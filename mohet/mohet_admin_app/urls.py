from django.urls import path
from . import views
urlpatterns = [
    path('/', views.index),
    path('/login', views.login),
    path('/logout', views.logout),
    path('/home', views.home),
    path('/new_article', views.new_article),
    path('/new_user', views.new_user),
    path('/new', views.new),
    path('/accept_article', views.accept_article),
    path('/article/accept/<int:id>', views.accept),
    path('/article/refuse/<int:id>', views.refuse),
    path('/article/<int:id>', views.view),
    path('/narticle', views.narticle)
]