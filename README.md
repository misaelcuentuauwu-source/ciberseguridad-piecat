# IP Tracker — Proyecto Académico

Aplicación web desarrollada con **Django** que captura, geolocaliza y muestra
la dirección IP del visitante de forma **transparente y ética**, con fines de
demostración académica en la materia de Ciberseguridad.

---

## ¿Qué hace?

1. Captura la IP pública del visitante desde los headers HTTP.
2. La geolocaliza usando la API gratuita de `ip-api.com`.
3. Guarda el registro en base de datos (SQLite).
4. Muestra toda la información directamente al usuario (sin rastreo oculto).

---

## Instalación y ejecución

```bash
# 1. Crear y activar entorno virtual
python -m venv venv
source venv/bin/activate        # Linux/macOS
venv\Scripts\activate           # Windows

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Aplicar migraciones
python manage.py makemigrations
python manage.py migrate

# 4. (Opcional) Crear superusuario para el panel de administración
python manage.py createsuperuser

# 5. Correr el servidor
python manage.py runserver
```

Abre `http://127.0.0.1:8000/` en tu navegador.

> **Nota:** Para que la geolocalización funcione con IPs reales, el servidor
> debe estar expuesto a internet. En local puedes usar **ngrok**:
> ```bash
> ngrok http 8000
> ```

---

## Estructura del proyecto

```
tracker-django/
├── config/
│   ├── settings.py      # Configuración global (SECRET_KEY desde variable de entorno)
│   └── urls.py          # Rutas raíz
├── tracker/
│   ├── models.py        # Modelo Visita (IP, geolocalización, User-Agent)
│   ├── views.py         # Lógica de captura y geolocalización
│   ├── urls.py          # Rutas de la app
│   ├── admin.py         # Panel de administración
│   └── templates/
│       └── tracker/
│           └── home.html  # Página principal con diseño visual
├── requirements.txt
└── manage.py
```

---

## Conceptos de ciberseguridad demostrados

| Concepto | Dónde se aplica |
|---|---|
| Captura de IP vía headers HTTP | `views.py` → `obtener_ip()` |
| Diferencia entre `REMOTE_ADDR` y `X-Forwarded-For` | `views.py` → comentarios |
| Geolocalización por IP | `views.py` → `geolocalizacion()` |
| User-Agent fingerprinting | `request.META['HTTP_USER_AGENT']` |
| Secret Key en variables de entorno | `settings.py` |
| Limitaciones: VPN, CG-NAT, IPs dinámicas | Página principal → sección explicativa |

---

## Consideraciones éticas

- El aviso en la página informa al usuario **antes** de cualquier acción.
- No se usa JavaScript oculto ni píxeles de rastreo.
- Los datos son exclusivamente para demostración académica.
- La geolocalización es aproximada; **no revela domicilios exactos**.
