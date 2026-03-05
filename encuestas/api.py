from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Pregunta, Opcion
from .serializers import PreguntaSerializer

class PreguntaViewSet(viewsets.ModelViewSet):
    queryset = Pregunta.objects.all()
    serializer_class = PreguntaSerializer

    @action(detail=True, methods=['post'])
    def votar(self, request, pk=None):
        pregunta = self.get_object()
        opcion_id = request.data.get('opcion_id')
        try:
            opcion = pregunta.opcion_set.get(id=opcion_id)
            opcion.votos += 1
            opcion.save()
            return Response({'status': 'voto registrado'})
        except Opcion.DoesNotExist:
            return Response({'status': 'opción no encontrada'}, status=400)