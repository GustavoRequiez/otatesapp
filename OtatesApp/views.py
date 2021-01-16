from django.shortcuts import render, HttpResponse
from OtatesApp.forms  import FormProveedores,FormSucursales, FormEgreso, FormIngreso
from OtatesApp.models  import Proveedor, Sucursal,Ingreso,Egreso, Empleado
from django.db.utils import IntegrityError, DataError
from django.contrib.auth.models import User
import xlwt
import datetime

# Create your views here.

def home(request):
    return render(request,"OtatesApp/home.html")
def proveedores(request):
    if request.user.is_authenticated==False:
        return render(request,"OtatesApp/errorlogin.html")     
    else:
        if request.method=="POST":
            formulario=FormProveedores(request.POST)
            if formulario.is_valid():
                info=formulario.cleaned_data
                p=Proveedor(razonsocial=info["razonsocial"],nombre=info["nombre"],rfc=info["rfc"],tfno=info["telefono"],activo=info["activo"])
                try:
                    p.save()
                    return render(request,"OtatesApp/success.html",{"tipo":"PROVEEDOR"})
                except IntegrityError:
                    mensaje="YA EXISTE UN REGISTRO CON EL RFC %s"%info["rfc"]
                    return render(request,"OtatesApp/error.html",{"mensaje":mensaje,"tipo":"PROVEEDOR"})
                except DataError:
                    mensaje="DEBES INGRESAR UN NÚMERO TELEFÓNICO VÁLIDO"
                    return render(request,"OtatesApp/error.html",{"mensaje":mensaje,"tipo":"PROVEEDOR"})
        else:
            formulario=FormProveedores()
    return render(request,"OtatesApp/proveedores.html",{"formulario":formulario})  
def listarProveedores(request):
    proveedores_pool=Proveedor.objects.filter(activo=True)
    return render(request,"OtatesApp/listaproveedores.html",{"proveedores":proveedores_pool})
        
def sucursales(request):
    users=User.objects.filter(is_active=True)

    if request.user.is_authenticated==False:
        return render(request,"OtatesApp/errorlogin.html")     
    else:
        if request.method=="POST":
            if request:
                s=Sucursal(
                    nombre=request.POST["nombre"],
                    direccion=request.POST["direccion"],
                    tfno=request.POST["tfno"],
                    responsable=request.POST["responsable"])
                try:
                    s.save()
                    return render(request,"OtatesApp/success.html",{"tipo":"SUCURSAL"})
                except IntegrityError:
                    mensaje="ERROR AL REGISTRAR LA SUCURSAL"
                    return render(request,"OtatesApp/error.html",{"mensaje":mensaje,"tipo":"SUCURSAL"})
            
        return render(request,"OtatesApp/sucursales.html",{"users":users})
def listarSucursales(request):
    sucursales_pool=Sucursal.objects.filter(activo=True)
    return render(request,"OtatesApp/listasucursales.html",{"sucursales":sucursales_pool})
def ingresos(request):
    current_user = request.user
    if current_user.is_authenticated==False:
        return render(request,"OtatesApp/errorlogin.html")     
    else:
        emp=Empleado.objects.get(user=current_user)
        if request.method=="POST":
            formulario=FormIngreso(request.POST)
            if formulario.is_valid():
                infoform=formulario.cleaned_data
                importe=infoform["monto_tarjeta"]+infoform["monto_efectivo"]-infoform["monto_cortesia"]+infoform["monto_ta_express"]+infoform["monto_apps"]
                i=Ingreso(
                    fecha=infoform["fecha"], 
                    folio_in=infoform["folio_in"], 
                    folio_fin=infoform["folio_fin"], 
                    area=infoform["area"], 
                    no_personas=infoform["no_personas"], 
                    capturado_por=current_user.first_name,
                    monto_tarjeta=infoform["monto_tarjeta"], 
                    monto_efectivo=infoform["monto_efectivo"], 
                    monto_cortesia=infoform["monto_cortesia"], 
                    monto_ta_express=infoform["monto_ta_express"], 
                    monto_apps=infoform["monto_apps"], 
                    importe=importe, 
                    iva=importe*0.16, 
                    sucursal=emp.sucursal)
                try:
                    i.save()
                    return render(request,"OtatesApp/success.html",{"tipo":"INGRESO"})
                except IntegrityError:
                    mensaje="ERROR AL REGISTRAR EL INGRESO"
                    return render(request,"OtatesApp/error.html",{"mensaje":mensaje,"tipo":"INGRESO"})
        else:
            formulario=FormIngreso()
        return render(request,"OtatesApp/ingresos.html",{"formulario":formulario})

def listarIngresos(request):
    current_user = request.user
    emp=Empleado.objects.get(user=current_user)
    ingresos_pool=""
    fecha_in=""
    fecha_fin=""
    nombre_sucursal=""
    filename="Ingresos"
    if current_user.is_superuser:
        sucursal_pool=Sucursal.objects.filter(activo=True)
    else:
        sucursal_pool=Sucursal.objects.filter(nombre=emp.sucursal)

    if request.method=="POST":
        fecha_in=request.POST["fecha_in"]
        fecha_fin=request.POST["fecha_fin"]
        nombre_sucursal=request.POST["sucursal"]
        sucursal_pool2=sucursal_pool.exclude(nombre=nombre_sucursal)
        sucursal=Sucursal.objects.filter(nombre=nombre_sucursal)[:1]
        if fecha_in and fecha_fin:
            if sucursal:
                ingresos_pool=Ingreso.objects.filter(fecha__range=(fecha_in, fecha_fin),sucursal=sucursal)
            else:
                ingresos_pool=Ingreso.objects.filter(fecha__range=(fecha_in, fecha_fin))
        sucursal_pool=sucursal_pool2

    return render(request,"OtatesApp/listaingresos.html",{
        "ingresos":ingresos_pool,
        "sucursales":sucursal_pool,
        "fecha_in":fecha_in,
        "fecha_fin":fecha_fin,
        "sucursal":nombre_sucursal})

def egresos(request):
    current_user = request.user
    if current_user.is_authenticated==False:
        return render(request,"OtatesApp/errorlogin.html")     
    else:
        emp=Empleado.objects.get(user=current_user)
        if request.method=="POST":
            formulario=FormEgreso(request.POST)
            if formulario.is_valid():
                infoform=formulario.cleaned_data
                iva=infoform["importe"]*0.16
                total=infoform["importe"]+iva
                e=Egreso(
                    fecha=infoform["fecha"],
                    folio=infoform["folio"],
                    t_movimiento=infoform["t_movimiento"],
                    area=infoform["area"],
                    no_items=infoform["no_items"],
                    proveedor=infoform["proveedor"],
                    descripcion=infoform["descripcion"],
                    importe=infoform["importe"],
                    iva=iva,
                    total=total,
                    nn_rr=infoform["nn_rr"],
                    capturado_por=current_user.first_name,
                    autorizado_por=infoform["autorizado_por"],
                    observaciones=infoform["observaciones"],
                    sucursal=emp.sucursal)
                try:
                    e.save()
                    return render(request,"OtatesApp/success.html",{"tipo":"EGRESO"})
                except IntegrityError:
                    mensaje="ERROR AL REGISTRAR EL EGRESO"
                    return render(request,"OtatesApp/error.html",{"mensaje":mensaje,"tipo":"EGRESO"})
        else:
            formulario=FormEgreso()
        return render(request,"OtatesApp/egresos.html",{"formulario":formulario})
def listarEgresos(request):
    current_user = request.user
    emp=Empleado.objects.get(user=current_user)
    egresos_pool=""
    fecha_in=""
    fecha_fin=""
    nombre_sucursal=""
    filename="Egresos"
    if current_user.is_superuser:
        sucursal_pool=Sucursal.objects.filter(activo=True)
    else:
        sucursal_pool=Sucursal.objects.filter(nombre=emp.sucursal)

    if request.method=="POST":
        fecha_in=request.POST["fecha_in"]
        fecha_fin=request.POST["fecha_fin"]
        nombre_sucursal=request.POST["sucursal"]
        sucursal_pool2=sucursal_pool.exclude(nombre=nombre_sucursal)
        sucursal=Sucursal.objects.filter(nombre=nombre_sucursal)[:1]
        if fecha_in and fecha_fin:
            if sucursal:
                egresos_pool=Egreso.objects.filter(fecha__range=(fecha_in, fecha_fin),sucursal=sucursal)
            else:
                egresos_pool=Egreso.objects.filter(fecha__range=(fecha_in, fecha_fin))
        sucursal_pool=sucursal_pool2


    return render(request,"OtatesApp/listaegresos.html",{
        "egresos":egresos_pool,
        "sucursales":sucursal_pool,
        "fecha_in":fecha_in,
        "fecha_fin":fecha_fin,
        "sucursal":nombre_sucursal
        })


def export_excel(request,tipo,fecha_in,fecha_fin,sucursal):
    current_user = request.user
    emp=Empleado.objects.get(user=current_user)
    superuser=current_user.is_superuser
    rows=0
    columns=0
    data=[]
    if tipo==1:
        columns=['Fecha','Folio','Movimiento','Area','Articulos','Proveedor','Descripcion','Importe','Iva','Total','Tipo','Capturo','Autorizo','Observaciones','Sucursal']
        sucursal_obj=Sucursal.objects.filter(nombre=sucursal)[:1]
        if sucursal_obj:
            rows=Egreso.objects.filter(fecha__range=(fecha_in, fecha_fin),sucursal=sucursal_obj).values_list('fecha', 'folio', 't_movimiento', 'area', 'no_items', 'proveedor', 'descripcion', 'importe', 'iva', 'total', 'nn_rr', 'capturado_por', 'autorizado_por', 'observaciones','sucursal')
        else:
            rows=Egreso.objects.filter(fecha__range=(fecha_in, fecha_fin)).values_list('fecha', 'folio', 't_movimiento', 'area', 'no_items', 'proveedor', 'descripcion', 'importe', 'iva', 'total', 'nn_rr', 'capturado_por', 'autorizado_por', 'observaciones','sucursal')
        filename="Egresos"
        for row in rows:
            for col_num in range(len(row)):
                if columns[col_num]=="Proveedor":
                    proveedor=Proveedor.objects.filter(id=row[col_num]).values_list('razonsocial')
                elif columns[col_num]=="Autorizo":
                    user=User.objects.filter(id=row[col_num]).values_list('first_name')
                elif columns[col_num]=="Sucursal":
                    sucursal_id=Sucursal.objects.filter(id=row[col_num]).values_list('nombre')
            data_row=(row[0],row[1],row[2],row[3],row[4],proveedor[0],row[6],row[7],row[8],row[9],row[10],row[11],user[0],row[13],sucursal_id[0])
            data.append(data_row)
    #*****************************        
    elif tipo==2:
        columns=['Fecha','Folio Inicio','Folio Fin','Area','NO. personas','Capturo','monto_tarjeta','monto_efectivo','monto_cortesia','monto_ta_express','monto_apps','importe','iva','Sucursal']
        sucursal_obj=Sucursal.objects.filter(nombre=sucursal)[:1]
        if sucursal_obj:
            rows=Ingreso.objects.filter(fecha__range=(fecha_in, fecha_fin),sucursal=sucursal_obj).values_list('fecha', 'folio_in', 'folio_fin', 'area', 'no_personas', 'capturado_por', 'monto_tarjeta', 'monto_efectivo', 'monto_cortesia', 'monto_ta_express', 'monto_apps', 'importe', 'iva','sucursal')
        else:
            rows=Ingreso.objects.filter(fecha__range=(fecha_in, fecha_fin)).values_list('fecha', 'folio_in', 'folio_fin', 'area', 'no_personas', 'capturado_por', 'monto_tarjeta', 'monto_efectivo', 'monto_cortesia', 'monto_ta_express', 'monto_apps', 'importe', 'iva','sucursal')
        for row in rows:
            for col_num in range(len(row)):
                if columns[col_num]=="Sucursal":
                    sucursal_id=Sucursal.objects.filter(id=row[col_num]).values_list('nombre')
            data_row=(row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],row[9],row[10],row[11],row[12],sucursal_id[0])
            data.append(data_row)
        filename="Ingresos"
    
    response=HttpResponse(content_type="application/ms-excel")
    response['Content-Disposition'] = 'attachment; filename=%s.xls'%filename
    wb=xlwt.Workbook(encoding='utf-8')
    ws=wb.add_sheet(filename)
    row_num=0
    font_style=xlwt.XFStyle()
    font_style.font.bold=True
    date_format = xlwt.XFStyle()
    date_format.num_format_str = 'dd/mm/yyyy'

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    font_style=xlwt.XFStyle()

    for row in data:
        row_num+=1
        for col_num in range(len(row)):
            if col_num==0:
                ws.write(row_num, col_num, row[col_num], date_format)
            else:
                ws.write(row_num, col_num, row[col_num], font_style)
    wb.save(response)
    return response


def exportExcel(request,tipo):
    if tipo==1:
        columns=['Nombre','Direccion','Telefono','Responsable']
        rows=Sucursal.objects.all().values_list('nombre','direccion','tfno','responsable')
        filename="Sucursales"
    elif tipo==2:
        columns=['Razon social','Nombre','RFC','Telefono']
        rows=Proveedor.objects.filter(activo=True).values_list('razonsocial','nombre','rfc','tfno')
        filename="Proveedores"
    response=HttpResponse(content_type="application/ms-excel")
    response['Content-Disposition'] = 'attachment; filename=%s.xls'%filename
    wb=xlwt.Workbook(encoding='utf-8')
    ws=wb.add_sheet(filename)
    row_num=0
    font_style=xlwt.XFStyle()
    font_style.font.bold=True
    date_format = xlwt.XFStyle()
    date_format.num_format_str = 'dd/mm/yyyy'

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    font_style=xlwt.XFStyle()

    for row in rows:
        row_num+=1
        for col_num in range(len(row)):
            if col_num==0:
                ws.write(row_num, col_num, row[col_num], date_format)
            else:
                ws.write(row_num, col_num, row[col_num], font_style)
    wb.save(response)
    return response
