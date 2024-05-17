from flask import Flask, render_template, request
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import os
import time


app = Flask(__name__)

def obtener_datos_airbnb(consulta):
    # Configura las opciones de Chrome para Heroku
    chrome_options = Options()
    chrome_options.binary_location = "/app/google-chrome"
    chrome_options.add_argument("--headless")  # Ejecuta Chrome en modo sin cabeza
    chrome_options.add_argument("--disable-gpu")  # Deshabilita la aceleración por GPU
    chrome_options.add_argument("--no-sandbox")  # Desactiva el modo sandbox por seguridad
    chrome_options.add_argument("--disable-dev-shm-usage")  # Soluciona problemas de espacio limitado en /dev/shm

    # Inicializa el servicio ChromeDriver especificando la ruta correcta
    chromedriver_path = "/app/chromedriver"
    os.chmod(chromedriver_path, 0o755)  # Cambia los permisos para asegurarse de que es ejecutable
    service = Service(executable_path=chromedriver_path)

    # Crea una instancia del controlador Chrome con las opciones configuradas
    driver = webdriver.Chrome(service=service, options=chrome_options)

    # Abre una página web en el navegador
    cadena_previa = 'https://www.airbnb.es/s/'
    cadena_siguiente = '/homes?tab_id=home_tab&refinement_paths%5B%5D=%2Fhomes&flexible_trip_lengths%5B%5D=one_week&monthly_start_date=2024-06-01&monthly_length=3&monthly_end_date=2024-09-01&price_filter_input_type=0&channel=EXPLORE&date_picker_type=calendar&source=structured_search_input_header&search_type=filter_change'
    enlace = cadena_previa + consulta + cadena_siguiente
    driver.get(enlace)

    # Espera 5 segundos para que la página cargue completamente
    time.sleep(5)

    # Extraer los datos de los resultados
    resultados = driver.find_elements(By.XPATH, '//span[@data-testid="listing-card-name"]')
    precios = driver.find_elements(By.XPATH, '//span[@class="a8jt5op atm_3f_idpfg4 atm_7h_hxbz6r atm_7i_ysn8ba atm_e2_t94yts atm_ks_zryt35 atm_l8_idpfg4 atm_mk_stnw88 atm_vv_1q9ccgz atm_vy_t94yts dir dir-ltr"]')
    datos = []
    hoteles = []
    precios_hoteles = []

    for resultado in resultados:
        nombre_hotel = resultado.text
        hoteles.append(nombre_hotel)

    for precio in precios:
        if 'noche' in precio.text:
            precio_hotel = precio.text
            precios_hoteles.append(precio_hotel)

    datos = list(zip(hoteles, precios_hoteles))

    # Cerrar el navegador
    driver.quit()

    return datos


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        consulta = request.form["consulta"]
        datos = obtener_datos_airbnb(consulta)
        return render_template("resultado.html", datos=datos)
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)

