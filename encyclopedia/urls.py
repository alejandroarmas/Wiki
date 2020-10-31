from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:page_title>", views.page, name="wiki"),
    path("search/", views.search, name="site_search"),
    path("createpage/", views.createpage, name="create_page"),
    path("randompage/", views.randompage, name="random_page")
]
