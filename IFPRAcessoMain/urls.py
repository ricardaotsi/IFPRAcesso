from django.conf.urls import url
from django.urls import path
from . import views

urlpatterns = [
    path('', views.pesquisa, name='pesquisa'),
    # path('edit/',views.edit, name='edit'),
    url(r'^pessoa/$', views.insertPessoa, name='insertPessoa'),
    url(r'^insertId/$', views.insertId, name='insertId'),
    url(r'^ajax/deleteId/$', views.deleteId, name='deleteId'),
    # url(r'^edit\?cracha=(?P<cracha>\d+)&matricula=(?P<matricula>\d+)&ativo=(?P<ativo>\D+)$', views.edit, name='edit'),
]