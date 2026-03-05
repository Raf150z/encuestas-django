from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from django.utils import timezone
from django.db.models import Q
from .models import Pregunta, Opcion
import csv
from django.http import HttpResponse

def index(request):
    """Vista principal: lista todas las preguntas activas"""
    ahora = timezone.now()
    
    preguntas_activas = Pregunta.objects.filter(
        activa=True,
        fecha_publicacion__lte=ahora
    ).filter(
        Q(fecha_cierre__isnull=True) | Q(fecha_cierre__gt=ahora)
    )
    
    preguntas_cerradas = Pregunta.objects.filter(
        Q(activa=False) | 
        Q(fecha_cierre__isnull=False, fecha_cierre__lte=ahora)
    )
    
    preguntas_cerradas = preguntas_cerradas.exclude(
        id__in=preguntas_activas.values_list('id', flat=True)
    )
    
    context = {
        'preguntas_activas': preguntas_activas,
        'preguntas_cerradas': preguntas_cerradas,
    }
    return render(request, 'encuestas/index.html', context)

def detalle(request, pregunta_id):
    pregunta = get_object_or_404(Pregunta, pk=pregunta_id)
    
    if not pregunta.esta_activa():
        messages.warning(request, 'Esta encuesta ya no acepta votos.')
        return redirect('encuestas:resultados', pregunta_id=pregunta.id)
    
    return render(request, 'encuestas/detalle.html', {'pregunta': pregunta})

def votar(request, pregunta_id):
    pregunta = get_object_or_404(Pregunta, pk=pregunta_id)
    
    if request.session.get(f'voto_{pregunta_id}', False):
        messages.error(request, 'Ya has votado en esta encuesta.')
        return redirect('encuestas:resultados', pregunta_id=pregunta.id)
    
    if not pregunta.esta_activa():
        messages.error(request, 'No se puede votar en una encuesta cerrada.')
        return redirect('encuestas:resultados', pregunta_id=pregunta.id)
    
    try:
        opcion_seleccionada = pregunta.opcion_set.get(pk=request.POST['opcion'])
    except (KeyError, Opcion.DoesNotExist):
        messages.error(request, 'Por favor selecciona una opción.')
        return render(request, 'encuestas/detalle.html', {
            'pregunta': pregunta,
            'error_message': "No seleccionaste una opción válida.",
        })
    else:
        opcion_seleccionada.votos += 1
        opcion_seleccionada.save()
        
        request.session[f'voto_{pregunta_id}'] = True
        
        messages.success(request, f'¡Voto registrado por "{opcion_seleccionada.texto_opcion}"!')
        
        return HttpResponseRedirect(reverse('encuestas:resultados', args=(pregunta.id,)))

def resultados(request, pregunta_id):
    pregunta = get_object_or_404(Pregunta, pk=pregunta_id)
    
    opciones = pregunta.opcion_set.all()
    total_votos = pregunta.total_votos()
    
    labels = [opcion.texto_opcion for opcion in opciones]
    datos = [opcion.votos for opcion in opciones]
    colores = ['#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF', '#FF9F40']
    
    context = {
        'pregunta': pregunta,
        'opciones': opciones,
        'total_votos': total_votos,
        'labels': labels,
        'datos': datos,
        'colores': colores,
    }
    return render(request, 'encuestas/resultados.html', context)


def exportar_resultados_csv(request, pregunta_id):
    pregunta = get_object_or_404(Pregunta, pk=pregunta_id)
    opciones = pregunta.opcion_set.all()
    
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="resultados_pregunta_{pregunta_id}_resultados.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['Opción', 'Votos', 'Porcentaje'])
    
    total = pregunta.total_votos()
    
    for opcion in pregunta.opcion_set.all():
        porcentaje = (opcion.votos / total * 100) if total > 0 else 0
        writer.writerow([opcion.texto_opcion, opcion.votos, f"{porcentaje:.2f}%"])
    
    writer.writerow([])
    writer.writerow(['Total', total, '100%'])
    
    return response