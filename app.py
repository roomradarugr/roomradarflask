from flask import Flask, render_template, request
from airbnb import obtener_datos_airbnb
from gtravel import obtener_datos_google_travel

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    datos_airbnb = []
    datos_google_travel = []
    
    if request.method == "POST":
        consulta = request.form["consulta"]
        
        # Obtener datos de Airbnb
        datos_airbnb = obtener_datos_airbnb(consulta)
        
        # Obtener datos de Google Travel
        datos_google_travel = obtener_datos_google_travel(consulta)

        return render_template("resultado2.html", datos_airbnb=datos_airbnb, datos_google_travel=datos_google_travel)
        
    return render_template("index.html", datos_airbnb=datos_airbnb, datos_google_travel=datos_google_travel)

if __name__ == "__main__":
    app.run(debug=True)
