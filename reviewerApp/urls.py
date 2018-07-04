from django.urls import path

from . import views

urlpatterns = [
    path('review/', views.index, name='index'),
    path('add/',views.add_txs,name='add_txs'),
    path('record/',views.recorder,name='recorder')
]