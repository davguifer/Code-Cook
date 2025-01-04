# Code-Cook

**Code-Cook** es una aplicación web diseñada para ayudarte a explorar, gestionar y buscar recetas de manera eficiente. Utiliza Django como framework backend, Beautiful Soup para la extracción de datos desde la web, y Whoosh para la indexación y búsqueda rápida de recetas.

---

## Características

- **Extracción de datos**: Obtén recetas directamente desde [BBC Good Food](https://www.bbcgoodfood.com/search?page=1).
- **Filtrado avanzado**: Encuentra recetas fácilmente mediante criterios como el título, tiempos específicos de preparación, cocción o el tiempo total. Además, filtra por dificultad, calificación (rating) o combina ingredientes con el tiempo total. También incluye secciones destacadas como recetas rápidas (quick recipes), recetas fáciles (easy recipes) y el top 3 de recetas mejor valoradas.
- **Sistema de recomendaciones**: Descubre recetas similares basadas en sus ingredientes y títulos utilizando una matriz TF-IDF y similitud de coseno.
- **Indexación rápida**: Usa Whoosh para búsquedas eficientes y organizadas.
- **UI Intuitiva**: Interfaz amigable desarrollada con Bootstrap.

---

## Instalación

1. **Clona el repositorio:**
   ```bash
   git clone <repositorio>
   cd code_cook_project
   ```

2. **Configura un entorno virtual:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # En Windows: venv\Scripts\activate
   ```

3. **Instala las dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Aplica las migraciones:**
   ```bash
   python manage.py migrate
   ```

5. **Inicia el servidor:**
   ```bash
   python manage.py runserver
   ```

---

## Uso

1. **Carga los datos:**
   - Navega a la opción "Load Data in Database" para cargar recetas desde [BBC Good Food](https://www.bbcgoodfood.com).

2. **Indexa los datos:**
   - Una vez cargados, navega a "Load Index" para indexar las recetas con Whoosh.

3. **Calcula recomendaciones:**
   - Ve a "Load Recommendations" para calcular recetas similares basadas en ingredientes y títulos.

4. **Busca recetas:**
   - Utiliza las herramientas de búsqueda para encontrar recetas según tus preferencias:
     - Por título.
     - Por tiempo de preparación, cocción o total.
     - Por dificultad o calificación.
     - Por ingredientes y tiempo total.

5. **Explora las recetas destacadas:**
   - Descubre recetas rápidas (menos de 30 minutos), fáciles, o las 3 mejor valoradas.

6. **Consulta recomendaciones:**
   - Accede a las recetas similares desde el detalle de una receta.

---

## Tecnologías utilizadas

- **Backend**: Django 5.1.4
- **Scraping**: Beautiful Soup 4.12.3, Requests 2.31.0
- **Búsqueda**: Whoosh 2.7.4
- **Recomendaciones**: Scikit-learn 1.3.1
- **Frontend**: Bootstrap 5.1.3

---

## Estructura del proyecto

```plaintext
code_cook_project/
├── code_cook_project/  # Configuración principal de Django
│   ├── settings.py     # Configuración global
│   ├── urls.py         # Rutas de la aplicación
│   └── wsgi.py         # Configuración WSGI
├── recipes/            # Aplicación principal
│   ├── models.py       # Modelos de datos
│   ├── views.py        # Lógica de negocio
│   ├── urls.py         # Rutas específicas
│   ├── templates/      # Archivos HTML
│   └── whoosh_config/  # Configuración de Whoosh
├── recommendation/     # Sistema de recomendaciones
│   ├── models.py       # Modelos para almacenar similitudes
│   ├── utils.py        # Cálculo de recomendaciones
│   ├── views.py        # Vistas relacionadas
└── manage.py           # Herramienta administrativa de Django
```

---

## Notas importantes

1. **Recetas premium**: Las recetas premium de BBC Good Food no están incluidas.
2. **Base de datos**: Se utiliza SQLite por defecto, pero puede configurarse otro motor en `settings.py`.

---

## Autor

**David Guillén**
