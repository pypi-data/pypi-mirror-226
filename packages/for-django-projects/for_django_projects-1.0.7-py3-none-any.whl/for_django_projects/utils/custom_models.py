import re

from django import forms
from django.contrib.postgres.fields import ArrayField
from django.core.validators import FileExtensionValidator
from django.db import models
from django.db.models import Value
from django.forms.widgets import DateTimeBaseInput
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.utils.safestring import mark_safe
from django_select2.forms import ModelSelect2Widget, Select2Widget, Select2MultipleWidget, ModelSelect2MultipleWidget
from pathlib import Path
import os
from django.conf import settings
from for_django_projects.form_utils.forms import BetterModelForm, BetterForm
from for_django_projects.utils.funciones_adicionales import customgetattr

TEMPLATES_PATH = os.path.join(Path(__file__).resolve().parent.parent, 'templates')

class CustomValueDb(Value):
    def __init__(self, value, output_field=None):
        from django.db.models import IntegerField, CharField, FloatField, DecimalField, BooleanField, DateField, DateTimeField
        type_value = type(value).__name__.lower()
        if not output_field:
            if "int" in type_value:
                output_field = IntegerField()
            if "str" in type_value:
                output_field = CharField()
            if "float" in type_value:
                output_field = FloatField()
            if "decimal" in type_value:
                output_field = DecimalField()
            if "bool" in type_value:
                output_field = BooleanField()
            if "date" in type_value:
                output_field = DateField()
            if "datetime" in type_value:
                output_field = DateTimeField()
        super().__init__(value, output_field=output_field)


def create_function_fancybox(name, **kwargs):
    def y(groupName=None, nombreBtn=None, caption=None):
        kwargs["nombre_btn"] = nombreBtn if nombreBtn else "Ver archivo"
        kwargs["groupName"] = groupName
        kwargs["caption"] = caption
        return mark_safe(render_to_string(os.path.join(TEMPLATES_PATH, 'fancybox_modelfile.html'), kwargs))
    y.__name__ = name
    return y

def build_dict_data(self) -> dict:
    from django.contrib.auth.models import AbstractUser
    d = {}
    for x in self._meta.fields:
        f = x.name
        if not(f == "password" and isinstance(self, AbstractUser)):
            field = self._meta.get_field(f)
            value = getattr(self, f)
            if value and type(field) in (models.ForeignKey, models.OneToOneField):
                d[f'{f}_id'] = value.id
                d[f'{f}_json_data'] = {}
                if value and hasattr(value, 'build_dict_data'):
                    d[f'{f}_json_data'] = value.build_dict_data()
            elif isinstance(field, ArrayField):
                objects_list = []
                for y in value:
                    objects_list.append(
                        y
                    )
                d[f'{f}'] = objects_list
            elif isinstance(field, models.FileField):
                d[f'{f}'] = str(value or '')
            else:
                d[f'{f}'] = value
    for x in self._meta.many_to_many:
        value = getattr(self, x.attname)
        objects_list = []
        for y in value.all():
            if hasattr(y, 'build_dict_data'):
                objects_list.append(
                    y.build_dict_data()
                )
        d[x.attname] = objects_list
    return d

def build_json_data(self) -> str:
    from django.http import JsonResponse
    return JsonResponse(self.build_dict_data()).content.decode()

class NormalModel(models.Model):

    def __init__(self, *args, **kwargs):
        SIMBOLO_MONEDA = getattr(settings, 'SIMBOLO_MONEDA', '$')
        from dateutil.tz import tz
        super().__init__(*args, **kwargs)
        for x in self._meta.fields:
            f = x.name
            if isinstance(self._meta.get_field(f), models.BooleanField):
                is_true = customgetattr(self, f)
                if is_true == None:
                    t = 'fas fa-clock text-info'
                else:
                    t = 'fa-check-circle text-success' if is_true else 'fa-times-circle text-secondary'
                setattr(self, '%s_boolhtml' % f, mark_safe('<i class="fas ' + t + '"></i>'))
                t = "HABILITADO" if is_true else "DESHABILITADO"
                setattr(self, '%s_texthtml' % f, t)
                t = "Sí" if is_true else "No"
                setattr(self, '%s_yesorno' % f, t)
            if isinstance(self._meta.get_field(f), models.DecimalField):
                t = customgetattr(self, f)
                if t != None:
                    setattr(self, '%s_unlocalize' % f, str(t).replace(',', '.'))
                    setattr(self, '%s_money' % f, "{}{}".format(SIMBOLO_MONEDA, str(t).replace(',', '.')))
                    t = int(float(customgetattr(self, f)))
                    setattr(self, '%s_integer' % f, t)
            if isinstance(self._meta.get_field(f), models.DateTimeField):
                t = customgetattr(self, f)
                if t != None:
                    setattr(self, '%s_tz' % f, t.astimezone(tz.gettz(settings.TIME_ZONE)))
            if isinstance(self._meta.get_field(f), models.FileField):
                file = getattr(self, f)
                if len(str(file)) > 0:

                    archivo_icon = '<i class="far fa-file"></i>'
                    extension = str(file.name.split('.')[-1]).lower()
                    if extension in ('svg', 'jpg', 'jpeg', 'png', 'tiff', "jfif", 'gif', 'bmp'):
                        archivo_icon = '<i class="far fa-file-image"></i>'
                    elif extension in ('doc', 'docx'):
                        archivo_icon = '<i class="far fa-file-word"></i>'
                    elif extension in ('xls', 'xlsx'):
                        archivo_icon = '<i class="far fa-file-excel"></i>'
                    elif extension in ('csv', ):
                        archivo_icon = '<i class="fas fa-file-csv"></i>'
                    elif extension in ('pptx', 'pptm', 'ppt'):
                        archivo_icon = '<i class="far fa-file-powerpoint"></i>'
                    elif extension in ('pdf',):
                        archivo_icon = '<i class="far fa-file-pdf"></i>'
                    elif extension in ('c', 'cpp', 'cxx', 'class','cmd', 'bat', 'html', 'css', 'js', 'sh'):
                        archivo_icon = '<i class="far fa-file-code"></i>'

                    setattr(self, '%s_a_tag' % f, mark_safe(
                        '<a target="_blank" href="{}">{} descargar</a>'.format(file.url, archivo_icon)
                    ))
                    setattr(self, '%s_icon' % f, mark_safe(archivo_icon))
                    is_image = extension in ('svg', 'jpg', 'jpeg', 'png', 'tiff', "jfif", 'gif', 'bmp')
                    setattr(self, '%s_is_image' % f, is_image)
                    setattr(self, '%s_extension' % f, extension)

                    setattr(self, '%s_fancybox' % f, create_function_fancybox('%s_fancybox_func' % f, **{
                        "archivo": file,
                        "archivo_is_image": is_image,
                        "archivo_extension": extension,
                        "icono": mark_safe(archivo_icon),
                        "URL_GENERAL": getattr(settings, 'URL_GENERAL', ''),
                    }))

    def build_dict_data(self) -> dict:
        return build_dict_data(self)

    def build_json_data(self) -> str:
        return build_json_data(self)

    class Meta:
        abstract = True


class ModeloBase(NormalModel):
    fecha_registro = models.DateTimeField(verbose_name="Fecha de Registro", auto_now_add=True, editable=False, null=True, blank=True)
    sin_eliminar = models.BooleanField(default=True, editable=False)

    def fecha_hora_registro(self):
        return self.fecha_registro

    class Meta:
        abstract = True

def filter_queryset(self, request, term, queryset=None, **dependent_fields):
    from django.db.models import Q;import django;from for_django_projects.utils.funciones import criterioBusquedaDinamico
    if django.VERSION < (4, 0):
        from django.contrib.admin.utils import (
            lookup_needs_distinct as lookup_spawns_duplicates,
        )
    else:
        from django.contrib.admin.utils import lookup_spawns_duplicates
    if queryset is None:
        queryset = self.get_queryset()
    search_fields = self.get_search_fields()
    select = Q()

    use_distinct = False
    if search_fields and term:
        DATABASE_ENGINE = str(settings.DATABASES[queryset.model.objects.db].get('ENGINE'))
        isPostgres = 'postgres' in DATABASE_ENGINE or 'postgis' in DATABASE_ENGINE or 'postgresql_psycopg2' in DATABASE_ENGINE
        or_queries = criterioBusquedaDinamico(term, search_fields, isPostgres=isPostgres)
        select |= or_queries
        use_distinct |= any(
            lookup_spawns_duplicates(queryset.model._meta, search_spec)
            for search_spec in search_fields
        )

    if dependent_fields:
        select &= Q(**dependent_fields)

    use_distinct |= any(
        lookup_spawns_duplicates(queryset.model._meta, search_spec)
        for search_spec in dependent_fields.keys()
    )

    if use_distinct:
        return queryset.filter(select).distinct()
    return queryset.filter(select)

class MySelect2Widget(ModelSelect2Widget):
    search_fields = []

    def __init__(self, searchs=None, *args, **kwargs):
        self.search_fields = searchs
        super().__init__(*args, **kwargs)

    def filter_queryset(self, request, term, queryset=None, **dependent_fields):
        return filter_queryset(self, request, term, queryset, **dependent_fields)

class MySelect2MultipleWidget(ModelSelect2MultipleWidget):
    search_fields = []

    def __init__(self, searchs=None, *args, **kwargs):
        self.search_fields = searchs
        super().__init__(*args, **kwargs)

    def filter_queryset(self, request, term, queryset=None, **dependent_fields):
        return filter_queryset(self, request, term, queryset, **dependent_fields)

class FormException(Exception):
    def __init__(self, form, prefix="", sufix=""):
        super().__init__("Error en el formulario")
        alerta = ""
        if isinstance(form, list) or isinstance(form, tuple):
            self.errors = []
            for x in form:
                for k, v in x.errors.items():
                    self.errors.append({prefix+k+sufix: v[0]})
        else:
            self.errors = [{prefix+k+sufix: v[0]} for k, v in form.errors.items()]
        for x in form.errors.get('__all__') or []:
            for key in getattr(settings, 'CONSTRAINT_MSG', {}).keys():
                if re.search(f"\\b{key}\\b", x):
                    alerta += f'<div>{getattr(settings, "CONSTRAINT_MSG", {})[key]}</div>'
        self.dict_error = {
            'error': True,
            "form": self.errors,
            "message": "Datos incorrectos, revise la información registrada.",
            "alerta": mark_safe(alerta)
        }


class CustomDateInput(DateTimeBaseInput):
    def format_value(self, value):
        return str(value or '')


class CustomDateTimeInput(DateTimeBaseInput):
    def format_value(self, value):
        return str(value or '')


class FormParent:
    class Media:
        css = {
            'all': (
                #'/static/assets/plugins/switchery/switchery.min.css',
                #'/static/panel/plugins/tag-it/css/jquery.tagit.css'
            )
        }
        js = (
            #'/static/assets/plugins/switchery/switchery.min.js',
            #'/static/js/renderSwicheryControl.js?v=1',
            '/static/js/forms.js?v=13',
            '/static/js/inline_forms.js?v=3',
            # '/static/panel/plugins/jquery-migrate/dist/jquery-migrate.min.js',
            # '/static/panel/plugins/tag-it/js/tag-it.min.js?v=1',
            # '/static/validaciones/funciones.js?v=2.2'
        )

    def __init__(self, *args, **kwargs):
        self.ver = kwargs.pop('ver', False)
        self.editando = bool('instance' in kwargs and kwargs.get("instance") and kwargs.get("instance").id)
        customStep = kwargs.pop('customStep', None)
        cantCharsSelect2 = kwargs.pop('cantCharsSelect2', {})
        addDataNameInput = kwargs.pop('addDataNameInput', False)
        select2_req = kwargs.pop('select2_req', [])#listado d campos que deban tener select2 ajax
        no_requeridos = kwargs.pop('no_requeridos', [])#listado d campos que no quieran q sean requeridos en el form
        requeridos = kwargs.pop('requeridos', [])#listado d campos que x defecto son requeridos pero quiere q no lo sean en el form
        campos = kwargs.pop('campos', [])#listado d campos con su widget customizado
        querysets = kwargs.pop('querysets', {})#listado d campos con un queryset filtrado
        querysetFilters = kwargs.pop('querysetFilters', {})
        no_switchery = kwargs.pop('no_switchery', [])#listado d campos BooleanField que no quieran q se dibujen con switchery en el form
        no_select2 = kwargs.pop('no_select2', [])#listado d campos que no quieran q se renderice con la librería select2
        inlines = kwargs.pop('inlines', [])
        if self.editando:
            self.instancia = kwargs['instance']
        super(FormParent, self).__init__(*args, **kwargs)
        if inlines:
            self.inlines = inlines
            if self.editando and len(args) == 0:
                instancia = self.instance
                if hasattr(self, 'inlines'):
                    for i in range(len(self.inlines)):
                        Formset = self.inlines[i]["formset"]
                        self.inlines[i]["formset"] = Formset(instance=instancia)

        # -------------------------------------------------
        for w in campos:
            self.fields[w['field']] = w['widget']
        if type(no_requeridos).__name__.lower() in ("list", "tuple"):
            for nr in no_requeridos:
                self.fields[nr].required = False
        for r in requeridos:
            self.fields[r].required = True
        for k, v in querysets.items():
            self.fields[k].queryset = v
        if hasattr(self, "Meta"):
            Modelo = self.Meta.model
            nombre_app, nombre_model = Modelo._meta.app_label, Modelo._meta.model_name
        if isinstance(querysetFilters, dict):
            for k, v in querysetFilters.items():
                self.fields[k].queryset = self.fields[k].queryset.filter(v)
        for k, v in self.fields.items():
            field = self.fields[k]
            if isinstance(field.widget, forms.FileInput) and hasattr(self, '_meta'):
                if hasattr(self._meta.model._meta.get_field(k), "validators"):
                    extensions = []
                    for x in self._meta.model._meta.get_field(k).validators:
                        if isinstance(x, FileExtensionValidator):
                            extensions.append(",".join([f".{ext}" for ext in x.allowed_extensions]))
                    if len(extensions) > 0:
                        self.fields[k].widget.attrs["accept"] = ",".join(extensions)
                        self.fields[k].widget.attrs["data-allowed-file-extensions"] = " ".join(extensions).replace(".", "").replace(",", " ")
                if self.editando and getattr(self.instance, k) and hasattr(getattr(self.instance, k), "url"):
                    self.fields[k].widget.attrs["data-default-file"] = getattr(getattr(self.instance, k), "url")
                self.fields[k].widget.attrs["class"] = (self.fields[k].widget.attrs.get("class") or "") + " dropify"
            if no_requeridos == "__all__":
                self.fields[k].required = False
            if isinstance(field, forms.DateField):
                self.fields[k].widget = CustomDateInput()
                self.fields[k].widget.input_type = "date"
            if isinstance(field, forms.DateTimeField):
                self.fields[k].widget = CustomDateTimeInput()
                self.fields[k].widget.input_type = "datetime-local"
            if isinstance(field, forms.TimeField) or isinstance(field.widget, forms.TimeInput):
                self.fields[k].widget.input_type = "time"
            if (isinstance(field, forms.ModelMultipleChoiceField) or isinstance(field, forms.ModelChoiceField)) and not field.widget.is_hidden:
                TheMySelect2 = MySelect2MultipleWidget if isinstance(field, forms.ModelMultipleChoiceField) else MySelect2Widget
                TheSelect2 = Select2MultipleWidget if isinstance(field,
                                                                   forms.ModelMultipleChoiceField) else Select2Widget
                if hasattr(field, 'queryset') and not k in no_select2:
                    if hasattr(field.queryset.model, 'sin_eliminar'):
                        self.fields[k].queryset = self.fields[k].queryset.filter(sin_eliminar=True)
                    cantReg = self.fields[k].queryset.count()
                    if k in select2_req and hasattr(self, "Meta"):
                        choices_searchs = customgetattr(Modelo, '{}_choices_searchs'.format(k))
                        dependent_fields = {}
                        if hasattr(Modelo, '{}_dependent_fields'.format(k)):
                            dependent_fields = customgetattr(Modelo, '{}_dependent_fields'.format(k))
                        if not isinstance(dependent_fields, dict):
                            raise ValueError("La función {} en {}.{} debe ser un diccionario.".format(
                                '{}_dependent_fields'.format(k), nombre_app, nombre_model))
                        if (isinstance(choices_searchs, list) or isinstance(choices_searchs, tuple)) and len(
                                choices_searchs) > 0:
                            self.fields[k].widget = TheMySelect2(searchs=choices_searchs,
                                                                 dependent_fields=dependent_fields,
                                                                 queryset=self.fields[k].queryset,
                                                                 choices=field.choices,
                                                                 attrs={'data-width': '100%', 'data-language': 'es', 'data-ajax--delay': "500", "data-ajax--cache": "false"},
                                                                 max_results=20)
                        else:
                            self.fields[k].widget = TheSelect2(choices=field.choices,
                                                               attrs={'data-width': '100%', 'data-language': 'es'})
                    else:
                        if hasattr(self, "Meta"):
                            if (cantReg <= 20) or not hasattr(Modelo, '{}_choices_searchs'.format(k)):
                                self.fields[k].widget = TheSelect2(choices=field.choices, attrs={'data-width': '100%', 'data-language': 'es'})
                            elif cantReg > 20 and hasattr(Modelo, '{}_choices_searchs'.format(k)):
                                choices_searchs = customgetattr(Modelo, '{}_choices_searchs'.format(k))
                                dependent_fields = {}
                                if hasattr(Modelo, '{}_dependent_fields'.format(k)):
                                    dependent_fields = customgetattr(Modelo, '{}_dependent_fields'.format(k))
                                if not isinstance(dependent_fields, dict):
                                    raise ValueError("La función {} en {}.{} debe ser un diccionario.".format('{}_dependent_fields'.format(k), nombre_app, nombre_model))
                                if (isinstance(choices_searchs, list) or isinstance(choices_searchs, tuple)) and len(choices_searchs) > 0:
                                    self.fields[k].widget = TheMySelect2(searchs=choices_searchs,
                                                                            dependent_fields=dependent_fields,
                                                                         queryset=self.fields[k].queryset,
                                                                         choices=field.choices,
                                                                         attrs={'data-width': '100%', 'data-language': 'es', 'data-ajax--delay': "500", "data-ajax--cache": "false"}, max_results=20)
                                else:
                                    raise ValueError("La función {} en {}.{} debe ser una lista o tupla.".format('{}_choices_searchs'.format(k), nombre_app, nombre_model))
                else:
                        self.fields[k].widget.attrs['class'] = "form-control"
            elif isinstance(field, forms.TypedChoiceField):
                if hasattr(field, 'choices'):
                    if len(field.choices) > 10:
                        self.fields[k].widget = Select2Widget(choices=field.choices, attrs={'data-width': '100%'})
                    else:
                        self.fields[k].widget.attrs['class'] = "form-control"
            elif isinstance(field, forms.MultipleChoiceField):
                if hasattr(field, 'choices'):
                    self.fields[k].widget = Select2MultipleWidget(choices=field.choices, attrs={'data-width': '100%', 'data-language': 'es'})
            elif isinstance(field.widget, forms.CheckboxInput) and not(k in no_switchery):
                self.fields[k].widget.attrs['class'] = "js-switch"
                self.fields[k].widget.attrs['data-render'] = "switchery"
                self.fields[k].widget.attrs['data-theme'] = "default"
            elif not isinstance(field, forms.FileField):
                self.fields[k].widget.attrs['class'] = "form-control"
            if isinstance(field.widget, forms.Textarea):
                self.fields[k].widget.attrs['rows'] = "2"
            if self.fields[k].required and self.fields[k].label:
                self.fields[k].label = mark_safe(self.fields[k].label + '<span style="color:red;margin-left:2px;"><strong>*</strong></span>')
            if self.ver:
                self.fields[k].widget.attrs['readonly'] = "readonly"
            if not 'col' in self.fields[k].widget.attrs:
                self.fields[k].widget.attrs['col'] = "12"
            if addDataNameInput:
                self.fields[k].widget.attrs['data-nameinput'] = k

        for f in self.fieldsets:
            step = f.name
            for ff in f.boundfields:
                k = ff.name
                if self.fields[k].required:
                    self.fields[k].widget.attrs['data-parsley-required'] = "true"
                self.fields[k].widget.attrs['data-parsley-group'] = customStep or step
                self.fields[k].widget.attrs['data-parsley-required-message'] = strip_tags("{} es obligatorio".format(
                    self.fields[k].label))


class FormBase(FormParent, BetterForm):
    pass


class ModelFormBase(FormParent, BetterModelForm):
    def is_valid(self):
        is_valid = super(ModelFormBase, self).is_valid()
        form = self
        if hasattr(form, 'inlines'):
            for inline in form.inlines:
                Formset = inline["formset"]
                formset = Formset(self.data, self.files, instance=self.instance if self.editando else None)
                is_valid = is_valid and formset.is_valid()
                errors = {}
                for i in range(len(formset.errors)):
                    e = formset.errors[i]
                    for k, v in e.items():
                        errors['{}-{}-{}'.format(formset.prefix, i, k)] = v
                self.errors.update(
                    errors
                )
        return is_valid

    def save(self, commit=True):
        obj = super(ModelFormBase, self).save(commit=commit)
        form = self
        if hasattr(form, 'inlines'):
            for inline in form.inlines:
                Formset = inline["formset"]
                formset = Formset(self.data, self.files, instance=obj)
                if formset.is_valid():
                    formset.save()
        return obj

