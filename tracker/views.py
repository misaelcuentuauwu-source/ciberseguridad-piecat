#views.py
import requests
import logging
from django.shortcuts import render
from .models import Visita

logger = logging.getLogger(__name__)


def obtener_ip(request):
    """
    Extrae la IP pública real del visitante.
    Se prioriza X-Forwarded-For (cuando hay proxies/CDN por delante)
    sobre REMOTE_ADDR (IP directa de la conexión TCP).
    """
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        # X-Forwarded-For puede ser una cadena como "IP_cliente, proxy1, proxy2"
        # La primera IP es siempre la del cliente original
        ip = x_forwarded_for.split(",")[0].strip()
    else:
        ip = request.META.get("REMOTE_ADDR")
    return ip


def geolocalizacion(ip):
    """
    Consulta ip-api.com para obtener información geográfica
    asociada a una IP pública. Retorna un dict con los datos
    o un dict vacío si la consulta falla.
    Nota: ip-api.com es gratuito para uso no comercial (≤45 req/min).
    """
    try:
        respuesta = requests.get(
            f"http://ip-api.com/json/{ip}",  # HTTP, no HTTPS (requerido en plan gratuito)
            timeout=5
        )
        respuesta.raise_for_status()
        return respuesta.json()
    except requests.RequestException as error:
        logger.warning("Error al consultar ip-api.com: %s", error)
        return {}


def home(request):
    """
    Vista principal: captura la IP del visitante de forma transparente,
    la geolocaliza, guarda el registro y muestra la información al usuario.
    El visitante sabe exactamente qué datos se están recolectando.
    """
    ip = obtener_ip(request)
    user_agent = request.META.get("HTTP_USER_AGENT", "Desconocido")
    data = geolocalizacion(ip)

    visita = Visita.objects.create(
        ip=ip,
        user_agent=user_agent,
        pais=data.get("country"),
        region=data.get("regionName"),
        ciudad=data.get("city"),
        isp=data.get("isp"),
        latitud=data.get("lat"),
        longitud=data.get("lon"),
    )

    contexto = {
        "ip": ip,
        "user_agent": user_agent,
        "pais": visita.pais or "No disponible",
        "region": visita.region or "No disponible",
        "ciudad": visita.ciudad or "No disponible",
        "isp": visita.isp or "No disponible",
        "latitud": visita.latitud,
        "longitud": visita.longitud,
        "fecha": visita.fecha,
    }

    return render(request, "tracker/home.html", contexto)