from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>",views.Entry_page,name="title"),
    path("search",views.search,name="search"),
    path("newpage",views.new_page,name="newpage"),
    path("editpage/<str:title>",views.editpage, name="editpage"),
    path("randoms",views.randoms,name="randoms")
]

