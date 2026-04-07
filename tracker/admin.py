#admin.py
from django.contrib import admin
from .models import Visita


@admin.register(Visita)
class VisitaAdmin(admin.ModelAdmin):
    list_display = ("ip", "pais", "ciudad", "isp", "fecha")
    list_filter = ("pais", "ciudad")
    search_fields = ("ip", "isp", "user_agent")
    readonly_fields = ("fecha",)
    ordering = ("-fecha",)
