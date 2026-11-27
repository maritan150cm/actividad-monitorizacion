"""
@file app.py
@brief Aplicación web Flask con exposición de métricas para Prometheus.
"""
from flask import Flask, request, Response
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST

app = Flask(__name__)
REQUEST_COUNT = Counter("http_requests_total", "Total de solicitudes HTTP recibidas")

@app.route("/")
def home():
    """@brief Ruta principal que incrementa el contador de peticiones."""
    REQUEST_COUNT.inc()
    return "Aplicación DevSecOps funcionando correctamente"

@app.route("/metrics")
def metrics():
    """@brief Expone las métricas en formato compatible con Prometheus."""
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
