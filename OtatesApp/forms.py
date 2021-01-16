from django import forms
from OtatesApp.models import Proveedor, Sucursal, Ingreso, Egreso

class FormIngreso(forms.ModelForm):
    class Meta:
        model = Ingreso
        fields = (
            'fecha',
            'folio_in',
            'folio_fin',
            'area',
            'no_personas',
            'monto_tarjeta',
            'monto_efectivo',
            'monto_cortesia',
            'monto_ta_express',
            'monto_apps')


class FormEgreso(forms.ModelForm):
    class Meta:
        model = Egreso
        fields = ('fecha','folio','t_movimiento','area','no_items','proveedor','descripcion','importe','nn_rr','autorizado_por','observaciones')

class FormProveedores(forms.Form):
    razonsocial=forms.CharField()
    nombre=forms.CharField()
    rfc=forms.CharField()
    telefono=forms.CharField()
    activo=forms.BooleanField()

class FormSucursales(forms.Form):
    nombre=forms.CharField()
    direccion=forms.CharField()
    tfno=forms.CharField()
    responsable = forms.CharField()
    activo=forms.BooleanField()
