from django.urls import path
from OtatesApp import views


urlpatterns = [
    path('', views.home, name="Home"),
    path('proveedores', views.proveedores, name="Proveedores"),
    path('sucursales', views.sucursales, name="Sucursales"),
    path('ingresos', views.ingresos, name="Ingresos"),
    path('egresos', views.egresos, name="Egresos"),
    path('listarProveedores', views.listarProveedores, name="listarproveedores"),
    path('listarSucursales', views.listarSucursales, name="listarsucursales"),
    path('listarIngresos', views.listarIngresos, name="listaringresos"),
    path('listarEgresos', views.listarEgresos, name="listaregresos"),
    path('exportar_excel/<int:tipo>/<fecha_in>/<fecha_fin>/<sucursal>', views.export_excel, name="exportar_excel"),
    path('exportar/<int:tipo>', views.exportExcel, name="exportar"),

]
