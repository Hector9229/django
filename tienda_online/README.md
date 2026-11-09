# Tienda Online API — Django + DRF + JWT

Backend de una **tienda en línea** desarrollado con Django, Django REST Framework,
autenticación JWT y documentación Swagger.

> Práctica 4 — Desarrollo Web Integral
> Proyecto base: Unidad 1 (Django + DRF + CRUD de productos), adaptado a la
> Unidad 3 (usuario personalizado, JWT, Swagger y corrección de fallas de seguridad).

---

## 1. Características

- Proyecto Django llamado **`tienda_online`** (tema: tienda en línea).
- Modelo de usuario personalizado (`users.User`) que usa el **email** para iniciar sesión.
- Campo extra del usuario: **`phone` (teléfono)**.
- CRUD de usuarios protegido para administradores.
- Endpoint de datos personales: `GET /api/v1/auth/me/`.
- Login con JWT: `POST /api/v1/auth/token/`.
- Renovación de token: `POST /api/v1/auth/token/refresh/`.
- Documentación interactiva con **Swagger** y **ReDoc**.
- CRUD de productos y categorías (proyecto de Unidad 1).
- Pruebas automatizadas de las correcciones de seguridad.

---

## 2. Requisitos

- Python 3.10 o superior
- pip

---

## 3. Instalación

```bash
# 1. Crear y activar el entorno virtual
python -m venv venv
# Windows
venv\Scripts\activate
# Linux / macOS
source venv/bin/activate

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Aplicar migraciones
python manage.py migrate

# 4. Crear los usuarios de prueba (admin y cliente)
python manage.py seed_demo

# 5. Crear un superusuario propio (opcional)
python manage.py createsuperuser

# 6. Ejecutar el servidor
python manage.py runserver
```

La base de datos es **SQLite** (`db.sqlite3`). El archivo está excluido en
`.gitignore`, por lo que no se sube al repositorio.

---

## 4. Usuarios de prueba

| Rol | Email | Contraseña |
|---|---|---|
| Administrador | `admin@tiendaonline.com` | `Admin12345!` |
| Cliente | `cliente@tiendaonline.com` | `Cliente12345!` |

> Estas credenciales son solo para el entorno local de la práctica.
> La base `db.sqlite3` no se sube al repositorio, así que después de clonarlo
> hay que ejecutar `python manage.py migrate` y `python manage.py seed_demo`
> para crearlas. El comando es idempotente: se puede ejecutar varias veces.

---

## 5. Endpoints principales

| Método | Endpoint | Descripción | Permiso |
|---|---|---|---|
| POST | `/api/v1/auth/token/` | Obtener `access` y `refresh` (email + contraseña) | Público |
| POST | `/api/v1/auth/token/refresh/` | Renovar el `access` con el `refresh` | Público |
| GET | `/api/v1/auth/me/` | Datos personales del usuario autenticado | JWT |
| GET/POST | `/api/v1/users/` | Listar / crear usuarios | Admin |
| GET/PUT/PATCH/DELETE | `/api/v1/users/{id}/` | Detalle / editar / eliminar usuario | Admin |
| GET/POST | `/api/v1/products/` | Listar / crear productos | JWT |
| GET/PUT/PATCH/DELETE | `/api/v1/products/{id}/` | Detalle / editar / eliminar producto | JWT |
| GET | `/api/v1/products/{id}/precio-final/` | Precio con descuento por categoría | JWT |
| GET/POST | `/api/v1/categories/` | Listar / crear categorías | JWT |

### Documentación

- Swagger UI: <http://127.0.0.1:8000/swagger/>
- ReDoc: <http://127.0.0.1:8000/redoc/>
- Esquema OpenAPI JSON: <http://127.0.0.1:8000/swagger/?format=openapi>
- Admin de Django: <http://127.0.0.1:8000/admin/>

En Swagger, para probar endpoints protegidos:

1. Ejecutar `POST /auth/token/` con el email y la contraseña.
2. Copiar el valor de `access`.
3. Pulsar **Authorize** e ingresar `Bearer <access_token>`.
4. Ejecutar `GET /auth/me/`.

---

## 6. Configuración del token

En `tienda_online/settings.py`:

```python
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(
        minutes=int(os.environ.get('ACCESS_TOKEN_LIFETIME_MINUTES', 60))
    ),
    'REFRESH_TOKEN_LIFETIME': timedelta(
        days=int(os.environ.get('REFRESH_TOKEN_LIFETIME_DAYS', 1))
    ),
    'AUTH_HEADER_TYPES': ('Bearer',),
}
```

- El **access token** dura **60 minutos** por defecto.
- Se puede cambiar sin tocar el código:

```bash
# Windows PowerShell
$env:ACCESS_TOKEN_LIFETIME_MINUTES=15
python manage.py runserver
```

---

## 7. Correcciones de seguridad aplicadas

El manual original tenía dos fallas importantes:

### 7.1 La contraseña se devolvía en las respuestas

**Problema:** el `UserSerializer` incluía `password` como campo normal, por lo que
el hash aparecía en el CRUD y en `/auth/me/`.

**Solución:** en `users/serializers.py` el campo se declara como `write_only=True`:

```python
password = serializers.CharField(
    write_only=True,
    required=False,
    min_length=8,
    style={'input_type': 'password'},
)
```

Así la contraseña se puede enviar al crear/actualizar, pero **nunca** se incluye
en las respuestas de la API.

### 7.2 Al editar sin contraseña se asignaba la contraseña del solicitante

**Problema:** el `partial_update` del manual hacía:

```python
else:
    request.data["password"] = request.user.password
```

Eso cambiaba la contraseña del usuario editado por el hash del administrador que
hacía la petición.

**Solución:** la lógica se movió al serializer y solo se llama a `set_password`
cuando la contraseña viene en la petición:

```python
def update(self, instance, validated_data):
    password = validated_data.pop('password', None)

    for field, value in validated_data.items():
        setattr(instance, field, value)

    if password:
        instance.set_password(password)

    instance.save()
    return instance
```

Si se edita un usuario sin enviar `password`, su contraseña **permanece intacta**.

### 7.3 Otras mejoras

- Se eliminó `username`; el email es el identificador único.
- Se usa `set_password()` (hash de Django) en lugar de guardar texto plano.
- Se validan las contraseñas con los validadores de Django.
- El CRUD de usuarios requiere `IsAdminUser`.
- Los endpoints de productos requieren autenticación JWT.
- `precio_final` devuelve 404 si el producto no existe.

---

## 8. Pruebas

```bash
python manage.py test
```

Las pruebas cubren, entre otras cosas:

- Login con email y contraseña.
- `/auth/me/` sin token → 401.
- `/auth/me/` no incluye `password`.
- Listado de usuarios no incluye `password`.
- Crear usuario guarda la contraseña hasheada.
- **Editar usuario sin contraseña no cambia el hash.**
- Editar usuario con contraseña sí la cambia.
- Usuario no administrador no puede listar usuarios (403).

Resultado esperado: **17 pruebas OK**.

---

## 9. Estructura del proyecto

```
tienda_online/
├── .gitignore
├── requirements.txt
├── README.md
├── manage.py
├── db.sqlite3              (excluido del repositorio)
├── tienda_online/          (configuración del proyecto)
│   ├── settings.py
│   ├── urls.py             (Swagger / ReDoc)
│   ├── asgi.py
│   └── wsgi.py
├── users/                  (usuario personalizado, JWT, /auth/me)
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   ├── admin.py
│   └── tests.py
└── products/               (CRUD de productos y categorías)
    ├── models.py
    ├── serializers.py
    ├── views.py
    ├── urls.py
    ├── services.py
    └── tests.py
```

---

## 10. Repositorio

<https://github.com/Hector9229/django.git>

El PDF y el documento Word con las capturas de Swagger, obtención del token,
consulta de datos personales y la prueba de edición sin contraseña se
encuentran en la carpeta `docs/`:

- `docs/Practica4_Django_JWT.pdf`
- `docs/Practica4_Django_JWT.docx` (versión editable, sin enlace al repositorio)
