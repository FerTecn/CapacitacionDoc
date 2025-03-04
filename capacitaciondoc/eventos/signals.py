import os
from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver
from .models import Evidencia

# ELIMINAR ARCHIVOS AL BORRAR OBJETOS
@receiver(post_delete, sender=Evidencia)
def eliminar_archivo_evidencia(sender, instance, **kwargs):
    """Elimina el archivo de evidencia cuando se borra la Evidencia de la BD."""
    if instance.archivo_evidencia and os.path.isfile(instance.archivo_evidencia.path):
        os.remove(instance.archivo_evidencia.path)

# ELIMINAR ARCHIVOS ANTERIORES AL ACTUALIZAR UNO NUEVO
@receiver(pre_save, sender=Evidencia)
def eliminar_archivo_evidencia(sender, instance, **kwargs):
    """Elimina el archivo de firma anterior si se actualiza en Autoridad."""
    try:
        evidencia_anterior = Evidencia.objects.get(pk=instance.pk)
        if evidencia_anterior.archivo_evidencia and evidencia_anterior.archivo_evidencia != instance.archivo_evidencia:
            if os.path.isfile(evidencia_anterior.archivo_evidencia.path):
                os.remove(evidencia_anterior.archivo_evidencia.path)
    except Evidencia.DoesNotExist:
        pass  # Si el objeto no existe aún (es nuevo), no hacemos nada