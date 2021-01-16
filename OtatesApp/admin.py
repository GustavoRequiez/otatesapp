from django.contrib import admin
from OtatesApp.models import Proveedor, Ingreso, Egreso,Sucursal, Empleado


# Register your models here.
class ProveedorAdmin(admin.ModelAdmin):
    list_display=("razonsocial", "rfc")
    search_fields=("razonsocial","rfc")

class IngresoAdmin(admin.ModelAdmin):
    list_display=("fecha", "folio_in","folio_fin","capturado_por")
    search_fields=("fecha", "folio_in","folio_fin","capturado_por")

class EgresoAdmin(admin.ModelAdmin):
    list_display=("fecha", "folio","capturado_por","autorizado_por")
    search_fields=("fecha", "folio","capturado_por","autorizado_por")

class SucursalAdmin(admin.ModelAdmin):
    list_display=("nombre", "responsable")
    search_fields=("nombre", "responsable")

class EmpleadoAdmin(admin.ModelAdmin):
    list_display=("user", "sucursal")
    search_fields=("user", "sucursal")


admin.site.register(Proveedor, ProveedorAdmin)
admin.site.register(Ingreso, IngresoAdmin)
admin.site.register(Egreso, EgresoAdmin)
admin.site.register(Sucursal, SucursalAdmin)
admin.site.register(Empleado, EmpleadoAdmin)