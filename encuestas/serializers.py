from rest_framework import serializers
from .models import Pregunta, Opcion

class OpcionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Opcion
        fields = ['id', 'texto_opcion', 'votos']
        
class PreguntaSerializer(serializers.ModelSerializer):
    opciones = OpcionSerializer(source='opcion_set', many=True, read_only=True)
    
    class Meta:
        model = Pregunta
        fields = ['id', 'texto_pregunta', 'fecha_publicacion', 'fecha_cierre', 'opciones']