#models.py
from django.db import models


class Visita(models.Model):
    """
    Representa una visita registrada al servidor.
    Almacena la IP, datos del navegador/sistema operativo (User-Agent),
    información geográfica aproximada y la marca de tiempo.
    """
    ip = models.GenericIPAddressField()
    user_agent = models.TextField()
    pais = models.CharField(max_length=100, null=True, blank=True)
    region = models.CharField(max_length=100, null=True, blank=True)
    ciudad = models.CharField(max_length=100, null=True, blank=True)
    isp = models.CharField(max_length=200, null=True, blank=True)
    latitud = models.FloatField(null=True, blank=True)
    longitud = models.FloatField(null=True, blank=True)
    fecha = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-fecha"]
        verbose_name = "Visita"
        verbose_name_plural = "Visitas"

    def __str__(self):
        return f"{self.ip} — {self.ciudad}, {self.pais} ({self.fecha:%Y-%m-%d %H:%M})"
