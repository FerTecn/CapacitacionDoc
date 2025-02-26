import os
from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver
from .models import Autoridad, FormatoDepartamento, FormatoConstancia

# ELIMINAR ARCHIVOS AL BORRAR OBJETOS
@receiver(post_delete, sender=FormatoDepartamento)
def eliminar_archivos_formato_departamento(sender, instance, **kwargs):
    """Elimina los archivos de header y footer cuando se borra un FormatoDepartamento."""
    for archivo in [instance.header, instance.footer]:
        if archivo and os.path.isfile(archivo.path):
            os.remove(archivo.path)

@receiver(post_delete, sender=FormatoConstancia)
def eliminar_archivo_formato_constancia(sender, instance, **kwargs):
    """Elimina el archivo de header cuando se borra un FormatoConstancia."""
    if instance.header and os.path.isfile(instance.header.path):
        os.remove(instance.header.path)

@receiver(post_delete, sender=Autoridad)
def eliminar_archivo_firma_autoridad(sender, instance, **kwargs):
    """Elimina el archivo de firma cuando se borra una Autoridad."""
    if instance.firma and os.path.isfile(instance.firma.path):
        os.remove(instance.firma.path)

# ELIMINAR ARCHIVOS ANTERIORES AL ACTUALIZAR UNO NUEVO
@receiver(pre_save, sender=FormatoDepartamento)
def eliminar_archivos_anteriores_departamento(sender, instance, **kwargs):
    """Elimina los archivos anteriores de header y footer si se actualizan en FormatoDepartamento."""
    try:
        formato_anterior = FormatoDepartamento.objects.get(pk=instance.pk)
        for campo in ["header", "footer"]:
            archivo_anterior = getattr(formato_anterior, campo)
            archivo_nuevo = getattr(instance, campo)

            if archivo_anterior and archivo_anterior != archivo_nuevo and os.path.isfile(archivo_anterior.path):
                os.remove(archivo_anterior.path)
    except FormatoDepartamento.DoesNotExist:
        pass  # Si el objeto no existe aún (es nuevo), no hacemos nada

@receiver(pre_save, sender=FormatoConstancia)
def eliminar_archivo_anterior_constancia(sender, instance, **kwargs):
    """Elimina el archivo de header anterior si se actualiza en FormatoConstancia."""
    try:
        formato_anterior = FormatoConstancia.objects.get(pk=instance.pk)
        if formato_anterior.header and formato_anterior.header != instance.header:
            if os.path.isfile(formato_anterior.header.path):
                os.remove(formato_anterior.header.path)
    except FormatoConstancia.DoesNotExist:
        pass  # Si el objeto no existe aún (es nuevo), no hacemos nada

@receiver(pre_save, sender=Autoridad)
def eliminar_archivo_anterior_firma(sender, instance, **kwargs):
    """Elimina el archivo de firma anterior si se actualiza en Autoridad."""
    try:
        firma_anterior = Autoridad.objects.get(pk=instance.pk)
        if firma_anterior.firma and firma_anterior.firma != instance.firma:
            if os.path.isfile(firma_anterior.firma.path):
                os.remove(firma_anterior.firma.path)
    except Autoridad.DoesNotExist:
        pass  # Si el objeto no existe aún (es nuevo), no hacemos nada