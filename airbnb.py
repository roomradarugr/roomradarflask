from flask import Flask, render_template, request
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait  # Correct import
from selenium.webdriver.support import expected_conditions as EC
import os
import time

app = Flask(__name__)

def obtener_datos_google_travel(consulta):
    # Configura las opciones de Chrome para Heroku
    options = Options()
    options.binary_location = "/app/google-chrome"
    options.add_argument("--headless")  # Ejecuta Chrome en modo sin cabeza
    options.add_argument("--disable-gpu")  # Deshabilita la aceleración por GPU
    options.add_argument("--no-sandbox")  # Deshabilita el modo sandbox por seguridad
    options.add_argument("--disable-dev-shm-usage")  # Mejora el manejo de memoria en contenedores

    # Inicializa el servicio ChromeDriver especificando la ruta correcta
    chromedriver_path = "/app/chromedriver"
    os.chmod(chromedriver_path, 0o755)  # Cambia los permisos para asegurarse de que es ejecutable
    service = Service(executable_path=chromedriver_path)

    # Crea una instancia del controlador Chrome con las opciones configuradas
    driver = webdriver.Chrome(service=service, options=options)

    # Construye la URL de Google Travel con la consulta del usuario
    url = f"https://www.google.com/travel/hotels?q={consulta}"
    driver.get(url)

    # Espera a que la página se cargue completamente
    WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located((By.XPATH, '//h2[@class="BgYkof ogfYpf ykx2he"]'))
    )

    # Extraer los datos de los resultados
    resultados = driver.find_elements(By.XPATH, '//h2[@class="BgYkof ogfYpf ykx2he"]')
    precios = driver.find_elements(By.XPATH, '//span[@class="kixHKb flySGb"]')
    
    datos = []
    hoteles = []
    precios_hoteles = []

    for resultado in resultados:
        nombre_hotel = resultado.text
        hoteles.append(nombre_hotel)
        print(nombre_hotel)

    for precio in precios:
        precio_hotel = precio.text
        if precio_hotel.strip():
            precios_hoteles.append(precio_hotel)
            print(precio_hotel)

    datos = list(zip(hoteles, precios_hoteles))

    driver.quit()  # Cierra el navegador

    return datos


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        consulta = request.form["consulta"]
        datos = obtener_datos_google_travel(consulta)
        return render_template("resultado.html", datos=datos)
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
