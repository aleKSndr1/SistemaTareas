"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from paginasinicio import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.vPaginaInicio, name = 'INICIO'),
    path('registro/',views.vPaginaRegistro, name = 'REGISTRO'),
    path('tarea/',views.vPaginaTareas, name='TAREA'),
    path('cerrarsesion/', views.singout, name = 'CSESION'),
    path('iniciarsesion/', views.sesion, name = 'ISESION'),
    path('crear/tarea/', views.creatarea, name = 'CTAREA'),
    path('tarea/<int:id_tarea>/', views.tarea_detalle, name = 'DTAREA'),
    path('tarea/<int:id_tarea>/completa', views.tarea_completada, name = 'TAREAC'),
    path('tarea/<int:id_tarea>/eliminada', views.tarea_eliminada, name = 'TAREAE'),
    path('tareas_completas', views.tareas_completas, name = 'TAREASCOMPLETAS'),
]
