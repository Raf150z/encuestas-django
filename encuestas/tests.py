from django.test import TestCase, Client
from django.utils import timezone
from django.urls import reverse
from datetime import timedelta
from .models import Pregunta, Opcion

class PreguntaModelTests(TestCase):
    def setUp(self):
        self.pregunta = Pregunta.objects.create(
            texto_pregunta="¿Test?",
            fecha_publicacion=timezone.now()
        )
        self.opcion1 = Opcion.objects.create(
            pregunta=self.pregunta,
            texto_opcion="Opción 1",
            votos=5
        )
        self.opcion2 = Opcion.objects.create(
            pregunta=self.pregunta,
            texto_opcion="Opción 2",
            votos=3
        )
    
    def test_fue_publicada_recientemente(self):
        ahora = timezone.now()
        pregunta_reciente = Pregunta.objects.create(
            texto_pregunta="Reciente",
            fecha_publicacion=ahora
        )
        self.assertTrue(pregunta_reciente.fue_publicada_recientemente())
        
        pregunta_antigua = Pregunta.objects.create(
            texto_pregunta="Antigua",
            fecha_publicacion=ahora - timedelta(days=2)
        )
        self.assertFalse(pregunta_antigua.fue_publicada_recientemente())
    
    def test_total_votos(self):
        self.assertEqual(self.pregunta.total_votos(), 8)
    
    def test_esta_activa(self):
        pregunta_test = Pregunta.objects.create(
            texto_pregunta="Pregunta de prueba",
            fecha_publicacion=timezone.now()
        )
        
        self.assertTrue(pregunta_test.esta_activa())
        
        pregunta_test.activa = False
        pregunta_test.save()
        self.assertFalse(pregunta_test.esta_activa())
        
        pregunta_test.activa = True
        pregunta_test.fecha_cierre = None
        pregunta_test.save()
        self.assertTrue(pregunta_test.esta_activa())
        
        pregunta_test.fecha_cierre = timezone.now() + timedelta(days=1)
        pregunta_test.save()
        self.assertTrue(pregunta_test.esta_activa())
        
        pregunta_test.fecha_cierre = timezone.now() - timedelta(days=1)
        pregunta_test.save()
        self.assertFalse(pregunta_test.esta_activa())

class OpcionModelTests(TestCase):
    def setUp(self):
        self.pregunta = Pregunta.objects.create(
            texto_pregunta="¿Test?",
            fecha_publicacion=timezone.now()
        )
        self.opcion = Opcion.objects.create(
            pregunta=self.pregunta,
            texto_opcion="Opción Test",
            votos=3
        )
    
    def test_porcentaje_votos(self):
        Opcion.objects.create(
            pregunta=self.pregunta,
            texto_opcion="Otra opción",
            votos=7
        )
        self.assertEqual(self.opcion.porcentaje_votos(), 30.0)

class VistaTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.pregunta = Pregunta.objects.create(
            texto_pregunta="¿Pregunta de prueba?",
            fecha_publicacion=timezone.now()
        )
        self.opcion = Opcion.objects.create(
            pregunta=self.pregunta,
            texto_opcion="Opción prueba"
        )
    
    def test_vista_index(self):
        response = self.client.get(reverse('encuestas:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "¿Pregunta de prueba?")
    
    def test_vista_detalle(self):
        self.pregunta.fecha_cierre = None
        self.pregunta.activa = True
        self.pregunta.save()
    
        response = self.client.get(reverse('encuestas:detalle', args=(self.pregunta.id,)))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Opción prueba")
        self.assertContains(response, "Registrar mi voto")
    
    def test_votar(self):
        self.pregunta.fecha_cierre = None
        self.pregunta.activa = True
        self.pregunta.save()
    
        response = self.client.post(
            reverse('encuestas:votar', args=(self.pregunta.id,)),
            {'opcion': self.opcion.id},
            follow=True
        )
    
        self.assertEqual(response.status_code, 200)
    
        self.opcion.refresh_from_db()
        self.assertEqual(self.opcion.votos, 1)
    
        messages = list(response.context['messages'])
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), f'¡Voto registrado por "Opción prueba"!')
        
        self.assertEqual(response.status_code, 200)
        
        self.opcion.refresh_from_db()
        self.assertEqual(self.opcion.votos, 1)
        
        messages = list(response.context['messages'])
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), f'¡Voto registrado por "Opción prueba"!')
    
    def test_voto_duplicado(self):
        session = self.client.session
        session[f'voto_{self.pregunta.id}'] = True
        session.save()
        
        response = self.client.post(
            reverse('encuestas:votar', args=(self.pregunta.id,)),
            {'opcion': self.opcion.id},
            follow=True
        )
        
        self.assertEqual(response.status_code, 200)
        
        self.opcion.refresh_from_db()
        self.assertEqual(self.opcion.votos, 0)
        
        messages = list(response.context['messages'])
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Ya has votado en esta encuesta.')
    
    def test_votar_sin_seleccion(self):
        self.pregunta.fecha_cierre = None
        self.pregunta.activa = True
        self.pregunta.save()
    
        response = self.client.post(
            reverse('encuestas:votar', args=(self.pregunta.id,)),
            {},
            follow=True
        )
    
        self.assertEqual(response.status_code, 200)
    
        self.assertContains(response, "Registrar mi voto")
    
        self.assertContains(response, "No seleccionaste una opción válida")
    
        self.opcion.refresh_from_db()
        self.assertEqual(self.opcion.votos, 0)
        
        self.assertEqual(response.status_code, 200)
        
        self.assertContains(response, "No seleccionaste una opción válida")
        
        self.opcion.refresh_from_db()
        self.assertEqual(self.opcion.votos, 0)
    
    def test_votar_pregunta_inactiva(self):
        self.pregunta.activa = False
        self.pregunta.save()
        
        response = self.client.post(
            reverse('encuestas:votar', args=(self.pregunta.id,)),
            {'opcion': self.opcion.id},
            follow=True
        )
        
        self.assertEqual(response.status_code, 200)
        
        messages = list(response.context['messages'])
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'No se puede votar en una encuesta cerrada.')
        
        self.opcion.refresh_from_db()
        self.assertEqual(self.opcion.votos, 0)