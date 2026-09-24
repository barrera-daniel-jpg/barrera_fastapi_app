# FastAPI CRUD con PostgreSQL

## Iniciar el proyecto

Levanta los servicios con Docker Compose:

```powershell
docker compose up -d --build
```

La API queda disponible en:

```text
http://localhost:8080/docs
```

## Migraciones con Alembic

Crear una nueva migracion despues de cambiar los modelos:

```powershell
docker compose exec api alembic revision --autogenerate -m "descripcion"
```

Aplicar las migraciones pendientes:

```powershell
docker compose exec api alembic upgrade head
```

Consultar la version actual:

```powershell
docker compose exec api alembic current
```

Alembic usa la variable `DATABASE_URL` del archivo `.env`, la misma conexion
que utiliza la API. Por eso las migraciones se aplican al PostgreSQL del
servicio `db` y no a otra base de datos.

## Conexion a PostgreSQL

Para conectarte desde pgAdmin, DBeaver u otra herramienta usa los valores del
archivo `.env`:

```text
Host: localhost
Puerto: 5433
Base de datos: catalogo_db
Usuario: admin
Contrasena: valor de POSTGRES_PASSWORD
```

La tabla de productos es `public.app_inv_products` y la tabla de control de
Alembic es `public.alembic_version`.

Para detener los servicios sin eliminar los datos:

```powershell
docker compose down
```

No uses `docker compose down -v` salvo que quieras borrar el volumen y la base
de datos almacenada en PostgreSQL.