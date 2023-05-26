"""OIM URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from MGYP import views as MGYPViews

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', MGYPViews.home),
    path('home/', MGYPViews.home),
    path('login/', MGYPViews.login1),
    path('registro/', MGYPViews.registro),
    path('logout/', MGYPViews.logoutUser),
    path('inventario/', MGYPViews.inventario),
    path('inventario/next', MGYPViews.inventario_next),
    path('productos/', MGYPViews.productos),
    path('historial/', MGYPViews.historial),
    path('ingreso_productos/', MGYPViews.ingreso_productos),
    path('ingreso_productos/next', MGYPViews.ingreso_productos_next),
    path('productos/nuevo_producto', MGYPViews.nuevo_producto),
    path('despacho_productos/', MGYPViews.despacho_productos),
    path('despacho_productos/next', MGYPViews.despacho_productos_next),
]
