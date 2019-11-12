from django.conf.urls import url
from django.urls import path
from . import views

urlpatterns = [
    path('', views.pesquisaPessoa, name='pesquisa'),
    url(r'^pessoa/$', views.insertPessoa, name='insertPessoa'),
    url(r'^insertId/$', views.insertId, name='insertId'),
    url(r'^pessoa/update/$', views.updatePessoa, name='updatePessoa'),
    url(r'^ajax/deleteId/$', views.deleteId, name='deleteId'),
    url(r'^ajax/update_session/$', views.update_session, name='update_session'),
    url(r'^relatorio/$', views.relatorio, name='relatorio'),
]