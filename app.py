from flask import Flask, render_template
import pandas as pd
import plotly.express as px
import plotly.io as pio

app = Flask(__name__)

csv = pd.read_csv(
    "datos.csv",
    keep_default_na=False
)

# Columnas q son numericas
columnas_numericas = [
    "peso",
    "altura",
    "velocidad"
]

for columna in columnas_numericas:
    csv[columna] = pd.to_numeric(
        csv[columna],
        errors="coerce"
    )

# Funcion pa todos los calculos
def frecuencia_absoluta(columna):
    return (
        csv[columna]
        .value_counts()
        .sort_index()
    )

def frecuencia_relativa(frecuencias):
    return (
        frecuencias / frecuencias.sum()
    )

def frecuencia_acumulada(frecuencias):
    return frecuencias.cumsum()

def calcular_media(columna):
    if columna == "color":

        return "No aplica"

    return round(
        csv[columna].mean(),
        2
    )

def calcular_mediana(columna):
    if columna == "color":

        return "No aplica"

    return round(
        csv[columna].median(),
        2
    )

def calcular_moda(columna):
    return (
        csv[columna]
        .mode()
        .iloc[0]
    )

def grafica_barras(columna, frecuencias):
    fig = px.bar(
        x=frecuencias.index,
        y=frecuencias.values,
        title=f"Frecuencia Absoluta - {columna}"
    )

    return pio.to_html(
        fig,
        full_html=False
    )

def grafica_pastel(columna, frecuencia_rel):
    fig = px.pie(
        names=frecuencia_rel.index,
        values=frecuencia_rel.values,
        title=f"Frecuencia Relativa - {columna}"
    )

    return pio.to_html(
        fig,
        full_html=False
    )

def grafica_poligono(columna, frecuencias):
    fig = px.line(
        x=frecuencias.index,
        y=frecuencias.values,
        markers=True,
        title=f"Polígono - {columna}"
    )

    return pio.to_html(
        fig,
        full_html=False
    )

def procesar_columna(columna):
    frecuencias = frecuencia_absoluta(columna)

    frecuencia_rel = frecuencia_relativa(
        frecuencias
    )

    frecuencia_acum = frecuencia_acumulada(
        frecuencias
    )

    return {
        "frecuencia_abs":
            frecuencias
            .rename_axis("Valor")
            .reset_index(name="n")
            .to_html(index=False),

        "frecuencia_rel":
            frecuencia_rel
            .rename_axis("Valor")
            .reset_index(name="n")
            .to_html(index=False),

        "frecuencia_acum":
            frecuencia_acum
            .rename_axis("Valor")
            .reset_index(name="n")
            .to_html(index=False),

        "media":
            calcular_media(columna),

        "mediana":
            calcular_mediana(columna),

        "moda":
            calcular_moda(columna),

        "barras":
            grafica_barras(
                columna,
                frecuencias
            ),

        "pastel":
            grafica_pastel(
                columna,
                frecuencia_rel
            ),

        "poligono":
            grafica_poligono(
                columna,
                frecuencias
            )
    }

# Rutas de app
@app.route("/")
def inicio():
    return render_template(
        "index.html",
        tabla=csv.to_html(index=False)
    )

@app.route("/columna/peso")
def peso():
    datos = procesar_columna("peso")

    return render_template(
        "peso.html",
        datos=datos
    )

@app.route("/columna/altura")
def altura():
    datos = procesar_columna("altura")

    return render_template(
        "altura.html",
        datos=datos
    )

@app.route("/columna/velocidad")
def velocidad():
    datos = procesar_columna("velocidad")

    return render_template(
        "velocidad.html",
        datos=datos
    )

@app.route("/columna/color")
def color():
    datos = procesar_columna("color")

    return render_template(
        "color.html",
        datos=datos
    )


if __name__ == "__main__":

    app.run(debug=True)