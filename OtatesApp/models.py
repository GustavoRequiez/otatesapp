from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Sucursal(models.Model):
    nombre=models.CharField("Nombre" ,max_length=50)
    direccion=models.CharField(max_length=50)
    tfno=models.CharField("Telefono",max_length=10)
    responsable = models.CharField("Responsable",max_length=20)
    activo=models.BooleanField(default=True)

    def __str__(self):
        return self.nombre


class Proveedor(models.Model):
    razonsocial=models.CharField("Razon social" ,max_length=50)
    nombre=models.CharField("Nombre" ,max_length=50, blank=True, null=True)
    rfc=models.CharField(max_length=16,unique=True)
    tfno=models.CharField("Telefono",max_length=10)
    activo=models.BooleanField(default=True)

    def __str__(self):
        return self.razonsocial

class Ingreso(models.Model):
    fecha=models.DateField()
    folio_in=models.IntegerField()
    folio_fin=models.IntegerField()
    area=models.CharField(max_length=20)
    no_personas=models.IntegerField()
    capturado_por=models.CharField(max_length=20)
    monto_tarjeta=models.FloatField()
    monto_efectivo=models.FloatField()
    monto_cortesia=models.FloatField()
    monto_ta_express=models.FloatField()
    monto_apps=models.FloatField()
    importe=models.FloatField()
    iva=models.FloatField()
    sucursal= models.ForeignKey(Sucursal, on_delete=models.CASCADE)

    def __str__(self):
        return '%s'%self.fecha

NN_RR= [("NN", 'NN'),("RR", 'RR')]

class Egreso(models.Model):
    fecha=models.DateField()
    folio=models.IntegerField()
    t_movimiento=models.CharField(max_length=20)
    area=models.CharField(max_length=20)
    no_items=models.IntegerField()
    proveedor= models.ForeignKey(Proveedor, on_delete=models.CASCADE)
    descripcion=models.CharField(max_length=50)
    importe=models.FloatField()
    iva=models.FloatField()
    total=models.FloatField()
    nn_rr=models.CharField("NN-RR",max_length=2, choices = NN_RR) 
    capturado_por= models.CharField(max_length=20)
    autorizado_por=models.ForeignKey(User, on_delete=models.CASCADE)
    observaciones=models.TextField(null=True,blank=True)
    sucursal= models.ForeignKey(Sucursal, on_delete=models.CASCADE)

    def __str__(self):
        return "%s"%self.fecha

class Empleado(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    sucursal = models.ForeignKey(Sucursal, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.sucursal.nombre


