from django.db import models
from django.utils import timezone
import datetime

class Pregunta(models.Model):
    texto_pregunta = models.CharField(max_length=200, verbose_name="Pregunta")
    fecha_publicacion = models.DateTimeField(default=timezone.now, verbose_name="Fecha de publicacion")
    fecha_cierre = models.DateTimeField(null=True, blank=True, verbose_name="Fecha de cierre")  # ¡CORREGIDO!
    activa = models.BooleanField(default=True, verbose_name="¿Activa?")
    
    class Meta:
        verbose_name = "Pregunta"
        verbose_name_plural = "Preguntas"
        ordering = ['-fecha_publicacion']
        
    def __str__(self):
        return self.texto_pregunta
    
    def fue_publicada_recientemente(self):
        ahora = timezone.now()
        return ahora - datetime.timedelta(days=1) <= self.fecha_publicacion <= ahora
    
    def esta_activa(self):
        if not self.activa:
            return False
        if self.fecha_cierre and self.fecha_cierre <= timezone.now():
            return False
        return True
    
    def total_votos(self):
        return sum(opcion.votos for opcion in self.opcion_set.all())
    
    fue_publicada_recientemente.boolean = True
    fue_publicada_recientemente.short_description = "¿Publicada recientemente?"
    esta_activa.boolean = True
    esta_activa.short_description = "¿Activa?"
    
    
class Opcion(models.Model):
    pregunta = models.ForeignKey(Pregunta, on_delete=models.CASCADE, verbose_name="Pregunta")
    texto_opcion = models.CharField(max_length=100, verbose_name="Opcion")
    votos = models.IntegerField(default=0, verbose_name="Numero de votos")
    
    class Meta:
        verbose_name = "Opcion"
        verbose_name_plural = "Opciones"
        
    def __str__(self):
        return self.texto_opcion
    
    def porcentaje_votos(self):
        total = self.pregunta.total_votos()
        if total > 0:
            return (self.votos / total) * 100
        return 0