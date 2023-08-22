import json
from datetime import time
import random
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.core import signing
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render
from django.utils import timezone
from django.utils.safestring import mark_safe
from decimal import Decimal
import copy

from datetime import date
from django.db import transaction
from django.conf import settings
from .funciones_adicionales import round_num_dec, customgetattr
from datetime import datetime

def null_to_numeric(valor, decimales=None):
    if decimales:
        return round((valor if valor else 0), decimales)
    return valor if valor else 0


def codigo_ramdon():
    x = range(10)
    codigo = list(x)
    return "".join([str(_) for _ in random.sample(codigo, 6)])


def codigoRandomLetDig(N=10):
    import random
    import string
    return ''.join(random.SystemRandom().choice(string.ascii_letters + string.digits) for _ in range(N))

def null_to_decimal(valor, decimales=None):
    if valor:
        if decimales:
            if decimales > 0:
                return float(Decimal(valor if valor else 0).quantize(
                    Decimal('.' + ''.zfill(decimales - 1) + '1')) if valor else 0)
            else:
                return float(Decimal(valor if valor else 0).quantize(Decimal('0')))
    return valor if valor else 0

def renderHtmlToJson(*args, titulo="", **kwargs):
    rendered = render(*args, **kwargs).content.decode()
    return JsonResponse(
        {
            "data": rendered,
            "result": True,
            "titulo": titulo or ""
        }
    )

def convertir_fecha(s):
    if ':' in s:
        sep = ':'
    elif '-' in s:
        sep = '-'
    else:
        sep = '/'
    return date(int(s.split(sep)[2]), int(s.split(sep)[1]), int(s.split(sep)[0]))


def convertir_hora(s):
    if ':' in s:
        sep = ':'
    return time(int(s.split(sep)[0]), int(s.split(sep)[1]))


def convertir_fecha_invertida(s):
    if ':' in s:
        sep = ':'
    elif '-' in s:
        sep = '-'
    else:
        sep = '/'
    return date(int(s.split(sep)[0]), int(s.split(sep)[1]), int(s.split(sep)[2]))


def convertir_fecha_invertida__mes_dia_ano(s):
    if ':' in s:
        sep = ':'
    elif '-' in s:
        sep = '-'
    else:
        sep = '/'
    return date(int(s.split(sep)[2].split(' ')[0]), int(s.split(sep)[0]), int(s.split(sep)[1]))


def convertir_fecha_invertida_dia_mes_ano(s):
    if ':' in s:
        sep = ':'
    elif '-' in s:
        sep = '-'
    else:
        sep = '/'
    return date(int(s.split(sep)[2]), int(s.split(sep)[1]), int(s.split(sep)[0]))


def pagination2(request, list_qs, cantidad):
    page = request.GET.get('page', 1)
    paginator = Paginator(list_qs, cantidad)
    paginas = []
    primera_pagina = False
    ultima_pagina = False
    try:
        list_qs = paginator.page(page)
    except PageNotAnInteger:
        list_qs = paginator.page(1)
    except EmptyPage:
        list_qs = paginator.page(paginator.num_pages)
    return list_qs

def formarCondicion(c, busqueda):
    if c.endswith("__islisttype"):
        return Q(**{c.replace("__islisttype", ""): [busqueda]})
    else:
        return Q(**{c: busqueda})
def campoSinFiltro(c):
    filtros = ["__icontains", "__contains", "__startswith", "__istartswith", "__endswith", "__iendswith", "__range", "__search"]
    for f in filtros:
        if c.endswith(f):
            return False
    return True
def criterioBusquedaDinamico(criterio: str, campos: list, isPostgres=True):
    '''Si el modelo no proviene de una base de datos postgres set isPostgres=False'''
    from django.db.models import Q
    from utils.function_utils import remover_espacios_de_mas
    filtros = Q()
    criterio_list = remover_espacios_de_mas(criterio).split(" ")
    for cl in criterio_list:
        cri = cl.strip()
        f = Q()
        if cri:
            for c in campos:
                if campoSinFiltro(c):
                    if cri.startswith("%") and cri.endswith("%"):
                        c = c + "__icontains"
                    elif cri.startswith("%"):
                        c = c + "__iendswith"
                    elif cri.endswith("%"):
                        c = c + "__istartswith"
                    else:
                        if isPostgres:
                            f |= formarCondicion(c + "__search", cri.replace("%", ""))
                        c = c + "__icontains"
                f |= formarCondicion(c, cri.replace("%", ""))
            filtros &= (f)
    return (filtros)

def rangos_paginado(p, pagina):
    left = p - 4
    right = p + 4
    if left < 1:
        left = 1
    if right > pagina.paginator.num_pages:
        right = pagina.paginator.num_pages
    pagina.paginas = range(left, right + 1)
    pagina.primera_pagina = True if left > 1 else False
    pagina.ultima_pagina = True if right < pagina.paginator.num_pages else False
    pagina.ellipsis_izquierda = left - 1
    pagina.ellipsis_derecha = right + 1


def paginador_api(request, list_qs, cantidad, *values, functionDataListado=None):
    data = {}
    if cantidad <= 0:
        cantidad = 1
    paging = MiPaginador(list_qs, cantidad)
    p = 1
    try:
        if 'page' in request.GET:
            p = int(request.GET['page'])
        data['siguiente'] = p + 1
        page = paging.page(p)
    except:
        page = paging.page(p)
    paging.desde = p if p == 1 else cantidad * p - (cantidad - 1)
    paging.hasta = cantidad if p == 1 else cantidad * p
    if paging.hasta > paging.total:
        paging.hasta = paging.total
    if paging.total == 0:
        paging.desde = 0
    data['listado'] = page.object_list
    data['pageHasNext'] = pageHasNext = page.has_next()

    data['pageNextPag'] = pageNextPag = page.next_page_number() if pageHasNext else 0
    data['dataJsonPaginacion'] = {"hasNext": pageHasNext, "nextPag": pageNextPag}

    data["paginas"] = []
    if paging.num_pages > 5:
        if paging.primera_pagina:
            data["paginas"].append(
                {
                    "page": 1,
                    "isActive": False,
                    "texto": str(1)
                }
            )
            data["paginas"].append(
                {
                    "page": paging.ellipsis_izquierda,
                    "isActive": True,
                    "texto": "..."
                }
            )
        for pagenumber in paging.paginas:
            data["paginas"].append(
                {
                    "page": pagenumber,
                    "isActive": pagenumber == page.number,
                    "texto": str(pagenumber)
                }
            )
        if paging.ultima_pagina:
            data["paginas"].append(
                {
                    "page": paging.ellipsis_derecha,
                    "isActive": True,
                    "texto": "..."
                }
            )
            data["paginas"].append(
                {
                    "page": paging.num_pages,
                    "isActive": False,
                    "texto": str(paging.num_pages)
                }
            )
    else:
        for pagenumber in paging.paginas:
            data["paginas"].append(
                {
                    "page": pagenumber,
                    "isActive": pagenumber == page.number,
                    "texto": str(pagenumber)
                }
            )
    if functionDataListado:
        functionDataListado(data)
    else:
        data["listado"] = list(data["listado"].values(*values) if len(values) > 0 else data["listado"].values())
    return data


def paginar_queryset(list_qs, cantidad, p=1):
    paging = MiPaginador(list_qs, cantidad)
    return paging, paging.page(p)

def paginador(request, list_qs, cantidad, data, url_vars=''):
    if cantidad <= 0:
        cantidad = 1
    p = int(request.GET.get('page') or 1)
    paging, page = paginar_queryset(list_qs, cantidad, p)
    if not "page=" in url_vars:
        url_vars += "&page={}".format(p)
    paging.desde = p if p == 1 else cantidad * p - (cantidad - 1)
    paging.hasta = cantidad if p == 1 else cantidad * p
    if paging.hasta > paging.total:
        paging.hasta = paging.total
    if paging.total == 0:
        paging.desde = 0
    data['paging'] = paging
    data['rangospaging'] = paging.rangos_paginado(p)
    data['page'] = page
    data['listado'] = page.object_list
    data['pageHasNext'] = pageHasNext = page.has_next()
    data['pageNextPag'] = pageNextPag = page.next_page_number() if pageHasNext else 0
    data['dataJsonPaginacion'] = json.dumps({"hasNext": pageHasNext, "nextPag": pageNextPag})
    get_filtros_anteriores(request, data, url_vars, en_paginador=True)



def get_filtros_anteriores(request, data, url_vars, en_paginador:bool=False):
    data["dict_url_vars"] = ""
    if en_paginador:
        if url_vars:
            try:
                dict_url_vars = json.loads(get_decrypt(request.GET.get('dict_url_vars'))[1]) if request.GET.get(
                    'dict_url_vars') else {}
                dict_url_vars[request.path] = url_vars
                d = json.dumps(dict_url_vars)
                data["dict_url_vars"] = "dict_url_vars={}".format(get_encrypt(d)[1])
            except Exception as ex:
                print(ex)
    elif request.GET.get("dict_url_vars"):
        data["dict_url_vars"] = "dict_url_vars={}".format(request.GET.get("dict_url_vars", "").replace("dict_url_vars=", ""))


def generar_nombre(nombre, original):
    from django.utils.text import slugify
    ext = ""
    if original.find(".") > 0:
        ext = original[original.rfind("."):]
    return slugify("{} {}".format(nombre, datetime.now().strftime("%Y-%m-%d %H-%M"))) + ext.lower()


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[-1].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


import pandas as pd
from io import BytesIO as IO, StringIO


def export_queryset_to_excel(columnas=[], queryset=None, filename="reporte_excel", nombre_hoja="Hoja 1"):
    import xlwt
    from django.http import HttpResponse
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="{}.xls"'.format(filename)
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet(nombre_hoja)
    columnas2 = list(columnas)
    columnas2.sort(key=len, reverse=True)
    col_width = 256 * len(columnas2[0])
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = columnas
    for col_num in range(len(columns)):
        ws.col(col_num).width = col_width
        ws.write(row_num, col_num, columns[col_num], font_style)
    font_style = xlwt.XFStyle()
    rows = queryset
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, str(row[col_num] or ""), font_style)
    wb.save(response)
    return response

def export_listmodel_to_excel(columnas=[], queryset=None, fields: list = [], filename="reporte_excel", nombre_hoja="Hoja 1"):
    import xlwt
    from django.http import HttpResponse
    col_list = []
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="{}.xls"'.format(filename)
    style0 = xlwt.easyxf('font: name Times New Roman, color-index black, bold off; align: wrap on, horiz center',
                         num_format_str='#,##0.00')
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet(nombre_hoja, cell_overwrite_ok=True)
    columnas2 = list(columnas)
    columnas2.sort(key=len, reverse=True)
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = columnas
    rows = queryset
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style) #Encabezados a la hoja excel

    font_style = xlwt.XFStyle()
    col_valor = [len(columns[x]) for x in range(0,len(columns))] #Asignando len de encabezados
    col_list.append(copy.copy(col_valor)) #Agregando a la lista

    for row in rows:
        row_num += 1
        for col_num in range(len(fields)):
            f = fields[col_num]
            ws.write(row_num, col_num, str(customgetattr(row, f) or ""), style0) #Genera valores para cada celda
            col_valor[col_num] = len(str(f).encode('gb18030'))#Calculando el len de cada celda
        col_list.append(copy.copy(col_valor)) #Agrega valor de len a la lista
    col_max = get_max_col(col_list) # Método para extraer el MAX len de cada columna

    for col_num in range(len(columns)):
        ws.col(col_num).width = 256 * (col_max[col_num] + 2)#Asigna ancho para cada celda

    wb.save(response)
    return response

def get_max_col(max_list):
    """ Calcula la Longitud Máxima de cada celda"""
    line_list = []
    # i significa fila, j significa columna
    for j in range(len(max_list[0])):
        line_num = []
        for i in range(len(max_list)):
            line_num.append(max_list[i][j])  # Almacene el ancho de cada columna en line_num
        line_list.append(max(line_num))  # Almacene el ancho máximo de cada columna en line_list
    return line_list


def save_file_in_media(file: InMemoryUploadedFile, path: str = "", extensions: list=[]) -> str:
    '''path = "ruta/fin/"'''
    if len(path) > 0:
        assert path[-1] == "/" or path[-1] == "\\", "El argumento path debe terminar con /"
        assert not path[0] in ("/", "\\"), "El argumento path no debe empezar con /"
    import os
    ruta = os.path.join(settings.BASE_DIR, 'media', path)
    os.makedirs(ruta, exist_ok=True)

    rutaFinal = os.path.join(ruta, file.name)
    filename, file_extension = os.path.splitext(file.name)
    if len(extensions) == 0 or file_extension.replace(".", "") in extensions:
        counter = 0
        while os.path.exists(rutaFinal):
            counter += 1
            filename = f"{filename}-{counter}"
            rutaFinal = os.path.join(ruta, f"{filename}{file_extension}")
        with open(rutaFinal, "wb+") as destination:
            for chunk in file.chunks():
                destination.write(chunk)
        return f"/media/{path}{filename}{file_extension}".replace("\\", '/')
    else:
        raise ValueError("")


def custom_get_timezone(request, user=None):
    import pytz
    if request.user.is_authenticated:
        return timezone.now().astimezone(pytz.timezone(settings.TIME_ZONE))
    return timezone.now().astimezone(pytz.timezone(settings.TIME_ZONE))


def redirectAfterPostGet(request, campos_add={}):
    dict_url_vars = request.GET.get('dict_url_vars') or request.POST.get('dict_url_vars') or ""
    if dict_url_vars:
        try:
            dict_url_vars = json.loads(get_decrypt(dict_url_vars)[1]).get(request.path) or ""
        except Exception as ex:
            print(ex)
    salida = "?action=add&" if '_add' in request.POST else request.path + "?"
    if '_add' in request.POST:
        for k, v in campos_add.items():
            salida += "&{}={}".format(k, v)
    return salida + "{}".format(dict_url_vars)


class MiPaginador(Paginator):
    def __init__(self, object_list, per_page, orphans=0, allow_empty_first_page=True, rango=5):
        super(MiPaginador, self).__init__(object_list, per_page, orphans=orphans,
                                          allow_empty_first_page=allow_empty_first_page)
        self.rango = rango
        self.paginas = []
        self.primera_pagina = False
        self.ultima_pagina = False
        self.total = len(object_list) if type(object_list).__name__.lower() in ("list", "tuple") else object_list.count()
        self.desde = 0
        self.hasta = 0

    def rangos_paginado(self, pagina):
        left = pagina - self.rango
        right = pagina + self.rango
        if left < 1:
            left = 1
        if right > self.num_pages:
            right = self.num_pages
        self.paginas = range(left, right + 1)
        self.primera_pagina = True if left > 1 else False
        self.ultima_pagina = True if right < self.num_pages else False
        self.ellipsis_izquierda = left - 1
        self.ellipsis_derecha = right + 1


def ip_client_address(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[-1].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def get_encrypt(values):
    try:
        return True, signing.dumps(values, compress=True)
    except Exception as ex:
        return False, str(ex)


def get_decrypt(cyphertxt):
    try:
        return True, signing.loads(cyphertxt)
    except Exception as ex:
        return False, str(ex)


def db_table_exists(table):
    try:
        from django.db import connection
        cursor = connection.cursor()
        table_names = [x.name for x in list(connection.introspection.get_table_list(cursor))]
    except Exception as ex:
        print("unable to determine if the table '%s' exists" % table)
    else:
        return table in table_names
