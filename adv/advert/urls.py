from django.urls import path

from . import views

app_name = 'advert'

urlpatterns = [
    path('search/', views.search, name='search'),
    path('profile/<str:username>/', views.profile, name='profile'),
    path('create/', views.advert_create, name='advert_create'),
    path(
        'advert/<int:advert_id>/edit/',
        views.advert_edit,
        name='advert_edit'
    ),
    path(
        'advert/<str:username>/<int:advert_id>/delete/',
        views.advert_delete,
        name='advert_delete'
    ),
    path(
        '<str:category>/<str:subcategory>/<int:advert_id>/comment/',
        views.add_comment,
        name='add_comment'
    ),
    path(
        '<str:category>/<str:subcategory>/<int:advert_id>/<int:comment_id>/',
        views.delete_comment,
        name='delete_comment'
    ),
    path(
        '<str:category>/<str:subcategory>/<int:advert_id>/',
        views.advert_detail,
        name='advert_detail'
    ),
    path(
        '<str:category>/<slug:slug>/',
        views.subcategory_list,
        name='subcategory_list'
    ),
    path('<slug:slug>/', views.category_adverts, name='category_list'),
    path('', views.index, name='index'),
]
