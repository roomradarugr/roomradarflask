from flask import Flask, render_template, request
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

app = Flask(__name__)

def obtener_datos_google_travel(consulta):
    # Initialize ChromeDriver service
    service = Service('/usr/bin/chromedriver')
    service.start()

    # Configure Chrome options (uncomment for headless mode)
    options = Options()
    # options.add_argument('--headless')

    # Create Chrome driver instance
    driver = webdriver.Chrome(service=service, options=options)

    # Build Google Travel URL with user query
    url = f"https://www.google.com/travel/hotels?q={consulta}"

    # Open the URL in the browser
    driver.get(url)

    time.sleep(15)

    # Extraer los datos de los resultados
    resultados = driver.find_elements(By.XPATH, '//h2[@class="BgYkof ogfYpf ykx2he"]')
    #precios = driver.find_elements(By.XPATH, '//div[@class="CQYfx UDzrdc"]')
    precios = driver.find_elements(By.XPATH, '//span[@class="kixHKb flySGb"]')
    
    #<span jsaction="mouseenter:JttVIc;mouseleave:VqIRre;">49&nbsp;€</span>
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

    # Cerrar el navegador
    driver.quit()

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


#<span class="qQOQpe ERGPc prxS3d">49&nbsp;€</span> precios
# div class="jVsyI" nobre + precios
#span class="qQOQpe prxS3d"
# precios <div class="CQYfx UDzrdc">49&nbsp;€ en total</div>
#nombres class="BgYkof ogfYpf ykx2he"
