# Code-Cook

**Code-Cook** es una aplicación web diseñada para ayudarte a explorar, gestionar y buscar recetas de manera eficiente. Utiliza Django como framework backend, Beautiful Soup para la extracción de datos desde la web, y Whoosh para la indexación y búsqueda rápida de recetas. Además, cuenta con un avanzado sistema de recomendación que utiliza técnicas de TF-IDF y similitud de coseno para sugerir recetas similares basadas en ingredientes y títulos.


---

## Objetivos

El objetivo principal de Code-Cook es proporcionar una plataforma robusta y eficiente para:

- **Facilitar la búsqueda de recetas** mediante un sistema de filtrado avanzado y personalizado.
- **Ofrecer recomendaciones personalizadas** basadas en similitudes de ingredientes y títulos.
- **Permitir la exploración de recetas destacadas**, como las más rápidas, las más fáciles y las mejor valoradas.
- **Automatizar la extracción de datos** desde sitios web de recetas populares.

---

## Descripción de las Partes del Proyecto

1. **Backend**:
   - Construido con Django, encargado de manejar la lógica del negocio, la gestión de la base de datos y las interacciones con el usuario a través de vistas y API.

2. **Extracción de datos**:
    - Utiliza Beautiful Soup y Requests para realizar scraping de recetas desde [BBC Good Food](https://www.bbcgoodfood.com/search?page=1).
   - Los datos extraídos incluyen títulos, ingredientes, tiempos de preparación y cocción, dificultad, calificaciones y número de votos.
   - El dato "tiempo total" es calculado en base a los atributos de tiempo de preparación y tiempo de cocción extraídos de la página.

3.  **Sistema de búsqueda**:
   - Implementado con Whoosh, permite indexar las recetas para ofrecer resultados rápidos y organizados.
   - Incluye herramientas de búsqueda avanzadas:
     - Búsqueda por título, tiempos de preparación, cocción y tiempo total.
     - Filtros por dificultad o calificación.
     - Combinación de ingredientes con tiempo total para encontrar recetas específicas.
     - Destaca secciones como recetas rápidas (quick recipes), recetas fáciles (easy recipes) y el top 3 de las mejor valoradas. 

4. **Sistema de recomendaciones**:
   - Utiliza Scikit-learn para analizar similitudes entre recetas basadas en técnicas de TF-IDF y similitud de coseno.
   - Permite sugerir recetas similares desde la vista de detalle de una receta.

5. **Frontend**:
   - Diseñado con Bootstrap para proporcionar una interfaz moderna, atractiva y responsiva.

---

## Elección del enfoque para el sistema de recomendación

En el sistema de recomendación de recetas, se decidió utilizar un enfoque basado en contenido con **TF-IDF (Term Frequency-Inverse Document Frequency)** y **Similitud Coseno** en lugar de un enfoque basado en ítems (como el utilizado comúnmente en sistemas de recomendación colaborativos). Las razones detrás de esta elección son las siguientes:

1. **Datos disponibles**:
    - Aunque las recetas en la página cuentan con interacción de usuarios (como puntuaciones y comentarios), no fue posible extraer esta información debido a que el contenido relacionado se genera dinámicamente mediante JavaScript, lo que limita las capacidades de extracción con herramientas como Beautiful Soup.
    - Los datos principales disponibles que se pudieron obtener son textuales: titulo, tiempo de preparación, tiempo de cocción, valoración, número de votos, dificultad e ingredientes.

2. **Adecuación del dominio**:
   - En el contexto de recetas, es lógico asumir que los usuarios buscarán recetas similares en términos de ingredientes y características textuales, más que basándose en preferencias de otros usuarios.
   - TF-IDF es ideal para identificar similitudes en conjuntos de palabras y frases, permitiendo capturar similitudes relevantes entre recetas.

3. **Escalabilidad y precomputación**:
   - La similitud entre recetas se calcula previamente y se almacena en la base de datos, mejorando la eficiencia durante las consultas.
   - Este enfoque es escalable para un conjunto grande de recetas, ya que reduce la necesidad de cálculos intensivos en tiempo real.

4. **Simplicidad de implementación**:
   - Al no requerir datos de usuarios, el enfoque basado en contenido se adapta perfectamente a aplicaciones donde el objetivo principal es recomendar ítems basados únicamente en sus características inherentes.
   - La integración de herramientas como **Scikit-learn** para la generación de la matriz TF-IDF simplifica la implementación y garantiza resultados precisos.


Por estas razones, el enfoque basado en contenido resulta ser el más adecuado para el sistema de recomendación de Code-Cook.

---

## Uso de las Herramientas

1. **Django**:
   - Manejo de la configuración global del proyecto, modelos de datos, vistas y rutas.

2. **Beautiful Soup**:
   - Extracción de información estructurada desde el HTML de BBC Good Food.

3. **Whoosh**:
   - Indexación eficiente y búsqueda avanzada en la base de datos de recetas.

4. **Scikit-learn**:
   - Cálculo de similitudes entre recetas para generar recomendaciones.

5. **Bootstrap**:
   - Creación de un diseño amigable y responsivo para el usuario final.

---

## Manual de Uso

### Instalación

1. **Clona el repositorio**:
   ```bash
   git clone <repositorio>
   cd code_cook_project
   ```

2. **Configura un entorno virtual**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # En Windows: venv\Scripts\activate
   ```

3. **Instala las dependencias**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Aplica las migraciones**:
   ```bash
   python manage.py migrate
   ```

5. **Inicia el servidor**:
   ```bash
   python manage.py runserver
   ```

### Uso de la Aplicación

1. **Carga los datos**:
   - Navega a la opción "Load Data in Database" para cargar recetas desde [BBC Good Food](https://www.bbcgoodfood.com/search?page=1).

2. **Indexa los datos**:
   - Una vez cargados, navega a "Load Index" para indexar las recetas con Whoosh.

3. **Calcula recomendaciones**:
   - Ve a "Load Recommendations" para calcular recetas similares basadas en ingredientes y títulos.

4. **Busca recetas**:
   - Utiliza las herramientas de búsqueda para encontrar recetas según tus preferencias:
     - Por título.
     - Por tiempo de preparación, cocción o total.
     - Por dificultad y/o calificación.
     - Por ingredientes y/o tiempo total.

5. **Explora las recetas destacadas**:
   - Descubre recetas rápidas (menos de 30 minutos), fáciles, o las 3 mejor valoradas.

6. **Consulta recomendaciones**:
   - Accede a las recetas similares desde el detalle de una receta.

---

## Tecnologías Utilizadas

- **Backend**: Django 5.1.4
- **Scraping**: Beautiful Soup 4.12.3, Requests 2.31.0
- **Búsqueda**: Whoosh 2.7.4
- **Recomendaciones**: Scikit-learn 1.3.1
- **Frontend**: Bootstrap 5.1.3

---

## Estructura del Proyecto

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

## Notas Importantes

1. **Recetas premium**:
   - Las recetas premium de BBC Good Food no están incluidas.

2. **Base de datos**:
   - Se utiliza SQLite por defecto, pero puede configurarse otro motor en `settings.py`.

---

## Autor

**David Guillén**
