# Etapa 2: De datos estáticos a datos dinámicos

**Objetivo:** que el estudiante pase de servir HTML hardcodeado a renderizar datos reales desde la base de datos, y aprenda relaciones entre modelos. Los conceptos centrales son **ORM con relaciones**, **querysets**, **paso de contexto a templates** y **herencia de plantillas**.

**Prerequisitos:** Etapa 1 completada (modelo `Curso` funcionando, panel de admin accesible con superuser).

---

## Tarea 1: Segundo modelo con relación — `Estudiante`

Crear un modelo `Estudiante` con los campos:

- `nombre` (`CharField`, máximo 100)
- `email` (`EmailField`)
- `curso` — una relación **ForeignKey** apuntando a `Curso` (un estudiante pertenece a un curso; un curso tiene muchos estudiantes).

Debe incluir un `__str__` que devuelva el nombre del estudiante.

Generar la migración y aplicarla:

```bash
python manage.py makemigrations classes
python manage.py migrate
```

**Concepto que se aprende:** relaciones uno-a-muchos con `ForeignKey`, parámetro `on_delete` (debe investigar cuándo usar `CASCADE`, `PROTECT`, `SET_NULL`), y cómo se traducen a SQL.

---

## Tarea 2: Listado dinámico de cursos en una página

Crear una vista nueva `lista_cursos` que:

1. Consulte todos los cursos: `Curso.objects.all()`.
2. Pase el queryset al template como contexto.
3. Renderice un template `classes/lista_cursos.html` que itere con `{% for curso in cursos %}` y muestre cada uno como un elemento de lista.

Conectar la vista en `classes/urls.py` en la ruta `cursos/` con `name='lista_cursos'`.

**Concepto que se aprende:** el flujo completo URL → view → ORM query → context → template loop. Aquí es donde Django "hace clic" como framework de datos.

---

## Tarea 3: Vista de detalle de un curso con sus estudiantes

Crear una vista `detalle_curso` que reciba un parámetro `pk` desde la URL (`cursos/<int:pk>/`) y muestre:

- El nombre y grado del curso.
- La lista de estudiantes inscritos en ese curso.

Pista: para obtener los estudiantes de un curso, usar la relación inversa. Si el ForeignKey se llama `curso`, entonces desde un objeto `Curso` se accede con `curso.estudiante_set.all()` (o un `related_name` personalizado si se define en el modelo — investiguelo).

Manejar el caso de que el `pk` no exista usando `get_object_or_404`.

Hacer que cada curso en la lista de la Tarea 2 sea un link al detalle, usando `{% url 'detalle_curso' curso.pk %}` (nunca hardcodear URLs en templates).

**Concepto que se aprende:** URLs con parámetros, relaciones inversas en el ORM, `get_object_or_404` (manejo correcto de 404), y la etiqueta `{% url %}` para no acoplar templates a paths.

---

## Tarea 4: Plantilla base con herencia (DRY)

Crear `classes/templates/classes/base.html` con la estructura HTML común (doctype, `<head>`, `<body>`, un `<header>` con el título "Gestor de Clases" y un `<nav>` con enlace al inicio y al listado de cursos).

Definir un bloque `{% block content %}{% endblock %}` donde irá el contenido específico de cada página.

Refactorizar **todos** los templates existentes (`index.html`, `lista_cursos.html`, `detalle_curso.html`) para que extiendan `base.html` con `{% extends "classes/base.html" %}` y sobrescriban el bloque `content`.

**Concepto que se aprende:** herencia de templates — un patrón fundamental para evitar duplicar HTML en cada página. Es el equivalente a la herencia de clases, pero para presentación.

---

## Tarea 5: Personalizar el admin

En `classes/admin.py`, en vez de `admin.site.register(Curso)` plano, definir clases `ModelAdmin` para `Curso` y `Estudiante` con:

- `list_display` para mostrar varias columnas en la lista (no solo el `__str__`).
- `search_fields` para tener una barra de búsqueda.
- En el admin de `Curso`, listar los estudiantes inscritos *en línea* (investigar `TabularInline` o `StackedInline`).

Usar el decorador `@admin.register(...)` (forma moderna) en lugar de `admin.site.register(...)`.

**Concepto que se aprende:** el admin de Django es altamente personalizable y es de las herramientas más poderosas del framework. Saber sacarle provecho ahorra semanas de desarrollo de paneles CRUD.

---

## Criterio de "Etapa 2 terminada"

- [ ] Existe el modelo `Estudiante` con FK a `Curso` y migración aplicada.
- [ ] Visitando `/cursos/` se ve la lista de cursos cargados desde la BD.
- [ ] Cada curso es un link y muestra su detalle con sus estudiantes.
- [ ] Visitando una URL con un `pk` inexistente (ej. `/cursos/999/`) devuelve 404, no error 500.
- [ ] Todas las páginas comparten el header/nav definido en `base.html`.
- [ ] En el admin se pueden buscar cursos por nombre y los estudiantes aparecen inline al editar un curso.
- [ ] No hay URLs hardcodeadas en los templates (todo usa `{% url %}`).

---

## Pistas pedagógicas para guiar (sin darle el código)

- Si está confundido con la diferencia entre `objects.all()` y `objects.filter(...)`: explicarle que es la diferencia entre `SELECT *` y `SELECT ... WHERE`.
- Si no entiende para qué sirve el `name=` en `path()`: que intente hardcodear una URL en un template, luego que cambie la URL en `urls.py`, y verá que los links rompen. Con `{% url 'nombre' %}` no.
- Si el `related_name` le suena innecesario: explicarle que `estudiante_set` es el default pero es feo; con `related_name="estudiantes"` queda `curso.estudiantes.all()`, que se lee como inglés.
- Si quiere usar `Curso.objects.get(pk=pk)` en lugar de `get_object_or_404`: pedirle que pruebe ambas con un id inexistente y vea la diferencia de respuesta HTTP.
- Si quiere repetir el `<header>` en cada template en lugar de hacer `base.html`: pedirle que imagine cambiar el título del sitio cuando haya 20 templates.
