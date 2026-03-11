# Aplicación de Encuestas con Django 

Aplicación web desarrollada con Django para crear y votar encuestas. Los usuarios pueden ver preguntas, votar por diferentes opciones y visualizar los resultados con gráficos interactivos.

## Características Principales

### Modelos y Base de Datos
- **Modelos completos**: Pregunta y Opción con relaciones
- **Panel admin personalizado**: Edición inline de opciones
- **Interfaz de administración** para gestionar preguntas y opciones fácilmente

### Sistema de Votación
- **Vistas principales**: Lista de encuestas, detalle, votación y resultados
- **URLs dinámicas**: Basadas en IDs para cada encuesta
- **Formularios de votación**: Con validación de datos
- **Sistema de votación para usuarios** intuitivo y funcional
- **Prevención de votos duplicados**: Control por sesión de usuario

### Visualización y UX
- **Templates con herencia**: Base.html reutilizable para consistencia visual
- **Mensajes flash**: Feedback inmediato al usuario después de cada acción
- **Visualización de resultados con gráficos**: Gráficos de barras y pastel usando Chart.js
- **Gráficos interactivos**: Visualización dinámica de resultados

### Funcionalidades Extra
- **Exportación de datos**: Resultados descargables en formato CSV
- **API REST**: Endpoints para acceder a los datos de las encuestas
- **Pruebas unitarias**: Coverage básico para garantizar funcionamiento

### Documentación y Control de Versiones
- **Documentación completa**: README detallado con instrucciones de instalación
- **Control de versiones**: Git y GitHub para seguimiento del código

## Tecnologías Utilizadas

- **Python** - Lenguaje de programación principal
- **Django** - Framework web
- **HTML5** - Estructura de las páginas
- **CSS3** - Estilos y diseño responsive
- **JavaScript** - Interactividad y gráficos
- **SQLite** - Base de datos (por defecto)
- **Chart.js** - Librería para gráficos interactivos
- **Django REST Framework** - Para la API REST

## Requisitos Previos

- Python 3.8 o superior
- pip (gestor de paquetes de Python)
- Git (opcional, para clonar el repositorio)

## Instalación

Sigue estos pasos para poner el proyecto en funcionamiento:

### En CMD

1. Clonar el repositorio
```
git clone https://github.com/Raf150z/encuestas-django.git
```
2. Entrar a la carpeta del proyecto
```
cd encuestas-django
```
3. Crear entorno virtual
```
python -m venv venv
```
4. Activar el entorno virtual
```
venv\Scripts\activate
```
5. Instalar dependencias
```
pip install -r requirements.txt
```
6. Realizar migraciones
```
python manage.py migrate
```
7. Crear superusuario (para acceder al panel admin)
```
python manage.py createsuperuser
```
8. Ejecutar el servidor
```
python manage.py runserver
```
9. Acceder a la aplicación
```
Página principal	http://localhost:8000
Panel de administración	http://localhost:8000/admin
API REST	http://localhost:8000/api/preguntas/
```

