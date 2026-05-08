# Project01 — Guía técnica de Django

Este documento explica cómo está organizado el proyecto, qué decisiones tomar al crecerlo y cómo evitar errores comunes cuando recién empiezas con Django.

---

## 1. Proyecto vs. App: la distinción que define todo

Django separa el código en dos niveles, y entender la diferencia es lo más importante:

| Concepto | Qué es | Hay cuántos | Ejemplo en este repo |
|---|---|---|---|
| **Proyecto** | El "sitio" completo. Contiene la configuración global (`settings.py`), las URLs raíz, WSGI/ASGI, y orquesta a las apps. | **Uno solo** por sitio. | `mysite/` |
| **App** | Un módulo de funcionalidad reutilizable. Tiene sus propios modelos, vistas, URLs, plantillas, migraciones. | **Uno o muchos**. | `classes/` |

**Analogía:** el proyecto es el edificio (cimientos, instalaciones, entrada principal). Las apps son los departamentos dentro del edificio. Un edificio sin departamentos no sirve, y un departamento sin edificio no se puede habitar.

**Consecuencia práctica:** el proyecto **no** va en `INSTALLED_APPS` (no es una app); las apps **sí** van en `INSTALLED_APPS`.

---

## 2. Estructura actual

```
Project01/
├── .gitignore
├── README.md                ← este archivo
├── CLAUDE.md                ← guía para Claude Code
├── requirements.txt         ← dependencias Python
├── manage.py                ← punto de entrada CLI (runserver, migrate, etc.)
├── db.sqlite3               ← base de datos local (gitignored)
├── mysite/                  ← PROYECTO
│   ├── __init__.py
│   ├── settings.py          ← configuración global
│   ├── urls.py              ← URLconf raíz, incluye URLs de apps
│   ├── wsgi.py              ← entrada para servidores WSGI (gunicorn, etc.)
│   └── asgi.py              ← entrada para servidores ASGI (async)
└── classes/                 ← APP (dominio: gestión de clases)
    ├── __init__.py
    ├── apps.py              ← config de la app (clase AppConfig)
    ├── admin.py             ← registro de modelos en /admin
    ├── models.py            ← modelos de datos (ORM)
    ├── views.py             ← funciones/clases que reciben requests
    ├── tests.py             ← tests de la app
    └── migrations/          ← cambios de schema versionados
```

> Estructura aplanada: `manage.py` y los paquetes (`mysite/`, `classes/`) son hermanos en la raíz. Esto simplifica los comandos (no necesitas `cd` a un subdirectorio) y es la convención más usada en proyectos Django reales.

---

## 3. Cómo funciona tener varias apps en un mismo proyecto

Django asume desde el inicio que un proyecto puede tener **múltiples apps**. El flujo es:

1. **Crear la app** (desde la raíz del repo):
   ```bash
   python manage.py startapp <nombre_app>
   ```

2. **Registrarla en `INSTALLED_APPS`** (en `mysite/settings.py`):
   ```python
   INSTALLED_APPS = [
       # ...apps de Django...
       'classes.apps.ClassesConfig',
       'enrollments.apps.EnrollmentsConfig',
   ]
   ```
   Sin esto, Django **ignora** los modelos, plantillas y comandos de la app.

3. **Crear `urls.py` dentro de la app** y conectarla desde `mysite/urls.py`:
   ```python
   # mysite/urls.py
   from django.urls import include, path
   urlpatterns = [
       path('admin/', admin.site.urls),
       path('classes/', include('classes.urls')),
       path('enrollments/', include('enrollments.urls')),
   ]
   ```

4. **Crear migraciones** cuando la app tenga modelos:
   ```bash
   python manage.py makemigrations classes
   python manage.py migrate
   ```

### ¿Cuándo crear una nueva app y cuándo no?

**Crea una app nueva cuando:**
- Tienes un *dominio* claramente diferenciado (ej. `classes`, `users`, `payments`, `notifications`).
- El conjunto de modelos + vistas tendría sentido **reutilizarse** en otro proyecto.
- Quieres aislar permisos, plantillas o pruebas que no se mezclan con el resto.
- La app puede borrarse del proyecto sin romper a las demás (acoplamiento bajo).

**NO crees una app nueva cuando:**
- Es solo "una vista más" del mismo dominio. → ponla en la app existente.
- Es un helper sin modelos ni vistas (ej. utilidades de fechas). → un módulo `utils.py` basta.
- Estás separando por *capa técnica* en vez de por dominio (ej. una app `views`, otra `models`). → eso rompe la filosofía de Django, evítalo.
- Aún no sabes si el dominio es estable. → empieza monolítico, divide después cuando duela.

**Heurística:** si dos áreas del código *casi nunca* se importan entre sí pero hablan a la misma BD, son candidatas a apps separadas. Si todo el tiempo se llaman entre sí, déjalas juntas.

---

## 4. Convención de nombres para apps

`APP1` es un mal nombre por tres razones: no dice qué hace, usa mayúsculas (Python recomienda lowercase para módulos), y numera en vez de describir.

### Convención propuesta

| Regla | Ejemplo bueno | Ejemplo malo |
|---|---|---|
| **lowercase, sin guiones bajos si es una palabra** | `classes`, `users` | `Classes`, `User_app` |
| **plural cuando representa una colección de entidades** | `classes`, `enrollments`, `payments` | `class`, `enrollment` |
| **snake_case si son dos palabras** | `class_schedules`, `payment_methods` | `classSchedules`, `class-schedules` |
| **describe el dominio, no la capa técnica** | `notifications` | `views_app`, `helpers` |
| **evita prefijos genéricos** (`app_`, `module_`, `core_`) | `billing` | `app_billing` |
| **evita números** salvo versionado deliberado de API | `accounts` | `accounts2`, `app1` |
| **idioma consistente** en todo el proyecto | todo en inglés *o* todo en español | mezclar `users` con `clases` |

### Aplicado a este proyecto

La app inicial fue renombrada de `APP1` a **`classes`** (dominio: gestión de clases/cursos). El `AppConfig` correspondiente es `ClassesConfig` y se registra en `INSTALLED_APPS` como `'classes.apps.ClassesConfig'`.

Cuando agregues nuevas apps, sigue las mismas reglas de la tabla de arriba.

---

## 5. Buenas prácticas y antipatrones

### Hazlo así

- **Un app = un dominio.** Nombra por *qué hace*, no por *qué tipo de archivo contiene*.
- **`urls.py` por app**, incluido desde el del proyecto con `include()`. Mantiene las rutas cerca del código que las sirve.
- **Configura `AppConfig` explícitamente** en `INSTALLED_APPS` (`'classes.apps.ClassesConfig'`, no solo `'classes'`). Permite hooks de inicialización en `ready()`.
- **Migraciones se commitean**, siempre. Son parte del código fuente, no artefactos generados.
- **`db.sqlite3` se ignora.** Cada desarrollador tiene la suya, no se versiona.
- **Variables sensibles fuera de `settings.py`.** Usa variables de entorno (con `os.environ` o `django-environ`) para `SECRET_KEY`, credenciales, etc. cuando salgas de desarrollo local.
- **Usa el panel `/admin/`** desde el inicio: registra modelos en `admin.py` y `createsuperuser`. Te ahorra construir CRUDs durante prototipado.

### No hagas esto

- **No metas lógica de negocio en `views.py`.** Las vistas orquestan; la lógica vive en modelos o en módulos `services.py`/`selectors.py`. Vistas gordas son la causa #1 de proyectos Django imposibles de mantener.
- **No edites migraciones aplicadas a producción.** Si necesitas cambiar algo, crea una migración nueva.
- **No uses `DEBUG=True` en producción.** Expone tracebacks con secretos; es un agujero de seguridad.
- **No commitees `__pycache__/`, `.venv/`, ni `db.sqlite3`.** Por eso existe `.gitignore`.
- **No conectes una app a otra a través de imports profundos** (`from otra_app.views import _internal_helper`). Si necesitas algo de otra app, exponlo en una API pública (signals, funciones de servicio).
- **No mezcles inglés y español** en nombres de modelos/apps. Elige uno y sé consistente.
- **No uses `from app.models import *`.** Imports explícitos siempre.

---

## 6. Setup local (resumen)

```bash
# Una sola vez:
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Cada vez que abras una terminal nueva (desde la raíz del repo):
source .venv/bin/activate

# Primera vez en este equipo:
python manage.py migrate
python manage.py createsuperuser

# Día a día:
python manage.py runserver           # http://127.0.0.1:8000/
python manage.py makemigrations
python manage.py migrate
python manage.py test
```

---

## 7. Lecturas recomendadas

- [Django docs — Writing your first Django app](https://docs.djangoproject.com/en/6.0/intro/tutorial01/)
- [Django docs — Applications](https://docs.djangoproject.com/en/6.0/ref/applications/) — qué es exactamente una app y cómo Django la carga.
- [Two Scoops of Django](https://www.feldroy.com/books/two-scoops-of-django-3-x) — el libro de referencia para convenciones y arquitectura en proyectos reales.
