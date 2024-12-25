import requests
from bs4 import BeautifulSoup
import csv

BASE_URL = "https://www.mundorecetas.com/recetas-pc/"

# 1. Extraer categorías desde la página principal
def obtener_categorias():
    url = f"{BASE_URL}index.htm"
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Error al acceder a la página principal: {response.status_code}")
        return []

    # Parsear el HTML
    soup = BeautifulSoup(response.text, 'html.parser')

    # Buscar la tabla que contiene las categorías
    tabla = soup.find("table", {"border": "0"})  # Buscar tabla con atributo border="0"
    celdas = tabla.find_all("td", {"align": "center", "valign": "top"})  # Celdas relevantes

    # Extraer categorías
    categorias = []
    for celda in celdas:
        enlace = celda.find("a", href=True)
        if enlace:
            nombre = enlace.text.strip()  # Texto del enlace (nombre de la categoría)
            link = enlace["href"]        # Enlace relativo
            categorias.append({"nombre": nombre, "link": link})
    return categorias

# 2. Extraer recetas de una categoría
def obtener_recetas_categoria(link_categoria):
    url = f"{BASE_URL}{link_categoria}"
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Error al acceder a la categoría: {response.status_code}")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')
    filas_recetas = soup.find_all('tr', class_='row1')  # Ajustar al HTML de las recetas
    recetas = []
    for fila in filas_recetas:
        enlace = fila.find('a', href=True)
        titulo = fila.find('b').get_text(strip=True) if fila.find('b') else "Sin título"
        link = enlace['href'] if enlace else "No disponible"
        autor = fila.find(text=lambda t: "Autor:" in t).split(":")[-1].strip() if fila and "Autor:" in fila.text else "Desconocido"
        visitas = fila.find(text=lambda t: "Visitas:" in t).split(":")[-1].strip() if fila and "Visitas:" in fila.text else "0"
        recetas.append({"titulo": titulo, "link": link, "autor": autor, "visitas": visitas})
    return recetas

# 3. Extraer detalles de una receta
def obtener_detalle_receta(link_receta):
    url = f"{BASE_URL}{link_receta}"
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Error al acceder a la receta: {response.status_code}")
        return None

    soup = BeautifulSoup(response.text, 'html.parser')
    detalle_receta = {
        "titulo": soup.find("h2").get_text(strip=True) if soup.find("h2") else "No disponible",
        "porciones": soup.find("span", class_="yield").get_text(strip=True) if soup.find("span", class_="yield") else "No disponible",
        "tiempo_preparacion": soup.find("span", class_="preptime").get_text(strip=True) if soup.find("span", class_="preptime") else "No disponible",
        "tiempo_coccion": soup.find("span", class_="cooktime").get_text(strip=True) if soup.find("span", class_="cooktime") else "No disponible",
        "categoria": soup.find("span", class_="category").get_text(strip=True) if soup.find("span", class_="category") else "No disponible",
        "dificultad": soup.find("span", class_="duration").get_text(strip=True) if soup.find("span", class_="duration") else "No disponible",
        "introduccion": soup.find("h2", text="Introducción:").find_next("p").get_text(strip=True) if soup.find("h2", text="Introducción:") else "No disponible",
        "ingredientes": "\n".join([ing.get_text(strip=True) for ing in soup.find_all("span", class_="ingredient")]) if soup.find_all("span", class_="ingredient") else "No disponible",
        "instrucciones": soup.find("h2", text="Instrucciones:").find_next("p").get_text(strip=True) if soup.find("h2", text="Instrucciones:") else "No disponible",
    }

    return detalle_receta

# 4. Guardar en CSV
def guardar_en_csv(datos, nombre_archivo="recetas.csv"):
    with open(nombre_archivo, mode="w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=datos[0].keys())
        writer.writeheader()
        writer.writerows(datos)

# 5. Flujo completo
if __name__ == "__main__":
    categorias = obtener_categorias()
    print(f"Se encontraron {len(categorias)} categorías.")

    todas_recetas = []
    for categoria in categorias:
        print(f"Procesando categoría: {categoria['nombre']}")
        recetas = obtener_recetas_categoria(categoria['link'])
        for receta in recetas:
            print(f"  Procesando receta: {receta['titulo']}")
            detalle = obtener_detalle_receta(receta['link'])
            if detalle:
                todas_recetas.append(detalle)

    # Guardar todas las recetas en un archivo CSV
    if todas_recetas:
        guardar_en_csv(todas_recetas)
        print(f"Se guardaron {len(todas_recetas)} recetas en 'recetas.csv'.")
