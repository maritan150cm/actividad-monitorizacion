"""
@file app.py
@brief Aplicación web Flask con métricas Prometheus y envío de logs a Elasticsearch.
"""
import json
import os
import urllib.request
from datetime import datetime, timezone
from flask import Flask, request, Response
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST

app = Flask(__name__)
REQUEST_COUNT = Counter("http_requests_total", "Total de solicitudes HTTP recibidas")
ES_URL = os.getenv("ELASTICSEARCH_URL", "http://elasticsearch:9200/appsegura-logs/_doc")

def send_log(level, message, status):
    """@brief Envía un evento de registro estructurado al índice de Elasticsearch."""
    log_entry = {
        "@timestamp": datetime.now(timezone.utc).isoformat(),
        "service": "appsegura",
        "level": level,
        "method": request.method,
        "path": request.path,
        "status": status,
        "message": message,
    }
    try:
        req = urllib.request.Request(
            ES_URL,
            data=json.dumps(log_entry).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        urllib.request.urlopen(req, timeout=1)
    except Exception:
        pass

@app.route("/")
def home():
    """@brief Ruta principal que incrementa el contador y registra acceso exitoso."""
    REQUEST_COUNT.inc()
    send_log("INFO", "Acceso exitoso a la ruta principal", 200)
    return "Aplicación DevSecOps funcionando correctamente"

@app.route("/metrics")
def metrics():
    """@brief Expone las métricas en formato compatible con Prometheus."""
    send_log("INFO", "Consulta de metricas Prometheus", 200)
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)

@app.errorhandler(404)
def not_found(error):
    """@brief Registra un evento de error cuando se solicita una ruta inexistente."""
    send_log("ERROR", f"Ruta no encontrada: {request.path}", 404)
    return "Recurso no encontrado", 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
