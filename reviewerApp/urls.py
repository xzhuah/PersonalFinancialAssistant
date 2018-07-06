from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('add/',views.add_txs,name='add_txs'),
    path('record/',views.recorder,name='recorder'),
    path('del/', views.delete_tx, name='delete'),

    path('week3D/', views.week_fin, name='week3D'),
    path('category/', views.cata_fin, name='category'),
    path('dynamic/', views.dyna_fin, name='dynamic'),
    path('engel/', views.engel_fin, name='engel'),
    path('list_cata/<slug:catagory>/', views.list_cata, name='list'),

    path('intro/', views.intro_page, name='intro'),

    path('login_server/', views.login, name='login_server'),
    path('login/', views.login_page, name='login'),
    path("logout/",views.logout,name="logout")
]