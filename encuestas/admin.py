from django.contrib import admin
from .models import Pregunta, Opcion

class OpcionInLIne(admin.TabularInline):
    model = Opcion
    extra = 3
    min_num = 2
    max_num = 10
    
class PreguntaAdmin(admin.ModelAdmin):
    fieldsets = [
        ('informacion de la pregunta', {'fields': ['texto_pregunta', 'activa']}),
        ('informacion de fechas', {'fields': ['fecha_publicacion', 'fecha_cierre'],
        'classes': ['collapse']}),
    ]
    inlines = [OpcionInLIne]
    list_display = ('texto_pregunta', 'fecha_publicacion', 'fecha_cierre', 'activa', 'total_votos')
    list_filter = ['fecha_publicacion', 'activa']
    search_fields = ['texto_pregunta']
    date_hieranchy = 'fecha_publicacion'
    actions = ['activar_preguntas', 'desactivar_preguntas']
    
    def activar_preguntas(self, request, queryset):
        queryset.update(activa=True)
    activar_preguntas.short_description = "Activar preguntas seleccionadas"
    
    def desactivar_preguntas(self, request, queryset):
        queryset.update(activa=False)
    desactivar_preguntas.short_description = "Desactivar preguntas seleccionadas"
    
admin.site.register(Pregunta, PreguntaAdmin)