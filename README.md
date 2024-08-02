# Segundo Test - Backend Developer

Historia de usuario: Enriquecer transacciones en línea.

## Descripción

Como usuario, dado un conjunto de transacciones bancarias, quiero poder enriquecerlas con información sobre categoría, nombre de comercio, logo de comercio (url) usando un API REST.

## Entidades

Transacción
```json
{
	"id": "uuid4",
	"description": "PYU *UberEats",
	"amount": -300.00,
	"date": "2023-12-01"
}
```

Categoría
```json
{
	"id": "uuid4",
	"name": "Restaurantes",
	"type": "expense"
}
```

Comercio
```json
{
	"id": "uuid4",
	"merchant_name": "Uber Eats",
	"merchant_logo" : "http://...",
	"category": "category_id"
}
```

Keyword
```json
{
	"id": "uuid4",
	"keyword": "uber eats",
	"merchant_id": "merchant_id"
}
```

## Conversación

### ENRIQUECIMIENTO

<ol type="a">
	<li>El usuario mediante una petición POST, podrá enviar un listado de transacciones al API de enriquecimiento.</li>
	<li>El API debe validar que la petición esté construida debidamente.</li>
	<li>Se deberán procesar las transacciones basado en la descripción, con el objetivo de agregar a la información tanto de comercio como de categoría (enriquecimiento), utilizando (pero no limitado a), las keywords como herramienta para el enriquecimiento.</li>
	<li>Si durante el procesamiento no es posible agregar información, se deberán devolver dichos campos en nulo.</li>
</ol>

### MEJORA DEL ENRIQUECIMIENTO

<ol type="a" start="5">
	<li>En caso de que algún tipo de transacción no sea enriquecida por el API y el usuario
cuente con información sobre la misma, podrá crear nuevos comercios y tanto
categorías como keywords relacionados al mismo.</li>
	<li>Una vez creados dichos registros, cuando se vuelva a enviar una transacción similar, la
misma debe ser correctamente enriquecida.</li>
</ol>

> [!NOTE]
> **DESEABLES**
> Con el objetivo de mejorar la tasa de enriquecimiento, es posible incorporar al procesamiento de datos una capa adicional de enriquecimiento, ya sea general (comercio y categoría) o acotado (sólo comercio o sólo categoría). Esta capa puede o no usar las keywords provistas.

## Criterios de aceptación de la historia de usuario

- Funcionales
	1. El tiempo de respuesta del API para una petición de 1,000 transacciones debe ser
el menor posible, nunca excediendo los 8 segundos.
	1. En la respuesta del endpoint de enriquecimiento, se deberá incluir un detalle de
métricas donde se indique:
		1. Total de transacciones recibidas.
		2. Tasa de categorización.
		3. Tasa de identificación de comercio.
- Reglas de dominio
	1. Se consideran como gastos las transacciones cuyo monto (amount) es negativo y como ingresos aquellas cuyo monto es positivo. Se debe asignar una categoría del tipo correcto.

## Criterios de aceptación del ejercicio

- Crear un proyecto Django con los modelos necesarios para persistir las estructuras de datos provistas (transacciones, categorías, comercios, keywords)
- Disponer de endpoints necesarios para realizar operaciones CRUD para categorías, comercios y keywords. Todas deben incluir campos `created_at` y `updated_at` predeterminados.
- Instrucciones para configurar, ejecutar y utilizar el proyecto
- Durante la revisión se consideran criterios de:
	- Eficiencia algorítmica
	- Buenas prácticas y testing
- El plazo de entrega para este ejercicio será de 24 horas
- Se debe subir el ejercicio en un repositorio (preferentemente en GitHub) y dar acceso a los revisores.

> [!CAUTION]
> Considera que existirán transacciones que puedan tener una categoría por algún dato relevante en su descripción, pero no necesariamente un comercio. Por ejemplo:
> id: 1
> descripción: "tienda de abarrotes la"
> amount: -123
> date: "2023-12-01"
> Es fácil identificar que la categoría corresponde a Supermercados y Tiendas de alimentos, pero es imposible definir el comercio.


## Dependencias

### Python

Se requiere una versión de Python que sea mayor a `3.10` (por ejemplo `3.10.12`) y menor a la `3.13` (como la `3.12.1` o la `3.11.3` por ejemplo).

Este repo fue desarrollado con Python **3.12**.

### Paquetes

Se requiere Poetry para instalar las dependencias (en este repo se utilizó Poetry versión `1.8.2`).
- Para instalar todas las dependencias: `poetry install`
- Para instalar solo las dependencias principales (sin las `dev.dependencies`): `poetry install --without dev`

El listado de dependencias utilizadas es el siguiente:
* dependencias principales (`[tool.poetry.dependencies]`):
	* `Django`: framework web
	* `djangorestframework`: API REST en Django
	* `django-cors-headers`: CORS en Django
	* `drf-spectacular`: Swagger en Django
	* `python-decouple`: lee variables de entorno
* dependencias secundarias (`[tool.poetry.group.dev.dependencies]`):
	* `bandit`: análisis estático de seguridad del código
	* `black`: formateo del código
	* `codespell`: para checkeo de *spelling* en inglés
	* `coverage`: para *coverage*
	* `flake8`: análisis estático de código basada en `pycodestyle`, `pyflakes`, `mccabe`, y plugins de terceros para checkeo del estilo y calidad de código en Python
	* `ipython`: *shell* interactiva
	* `isort`: formateo del código, solo para imports
	* `mccabe`: plugin de `flake8` para checkeo de complejidad ciclomática
	* `pre-commit`: hook pre commit. Aunque después de instalarlo se ejecuta automáticamente antes de hacer cada commit, se puede checkear manualmente todos los archivos con `pre-commit run --all-files` o solo los modificados con `pre-commit run`
	* `pylint`: análisis estático de código más estricto que `flake8`
	* `pylint-django`: plugin de `pylint` para analizar estático de proyectos que utilizan `Django`
	* `prospector`: análisis estático de código basado en `flake8` y `pylint`
	* `safety`: checkeo de dependencias vulnerables

### Variables de entorno

* `SECRET_KEY`: clave secreta para el proyecto en Django
* `ALLOWED_HOSTS`: host permitidos por Django, son valores separados por commas (por ejemplo: `'127.0.0.1, localhost, 0.0.0.0'`)
* `DB_ENGINE`: motor de base de datos en Django (por ejemplo: `django.db.backends.sqlite3`)
* `DB_NAME`: nombre de la base de datos
* `DB_USER`: usuario de la base de datos
* `DB_PASSWORD`: password para acceder a la base de datos
* `DB_HOST`: host de la base de datos
* `DB_PORT`: puerto de conexión a la base de datos

Respecto a la base de datos, para probar el proyecto solo basta utilizar el *driver* de SQLite3 (no es necesario utilizar MySQL o PostgreSQL) con las siguiente variables de entorno:
```.env
DB_ENGINE = django.db.backends.sqlite3
DB_NAME = db.sqlite3
DB_USER =
DB_PASSWORD =
DB_HOST =
DB_PORT =
```


## Tests

Se implementaron pruebas unitarias.

Para ejecutarlas se utiliza el siguiente comando dentro de la misma carpeta donde está ubicado el archivo `manage.py`: `coverage run --source='.' manage.py test --failfast bank_transaction && coverage report && coverage html`

Eso realiza 3 acciones:
1. ejecuta las pruebas unitarias
1. genera un reporte por consola indicando la cobertura por cada archivo tomado en cuenta
1. genera archivos html con el reporte detallado de cobertura de cada archivo tomado en cuenta


## Docker

Se ha agregado 2 archivos para levantar el proyecto mediante Docker compose: `Dockerfile` y `docker-compose.yml` que incluyen todos los comandos necesarios desde la instalación de Poetry hasta la ejecución de la API REST.

Sin embargo, **es muy importante que el archivo `.env` esté dentro de la misma ruta donde está el archivo `manage.py` que es justamente donde está el archivo de ejemplo `.env.example`** 


## Uso de la API REST

Se implementaron 4 endpoints, que son los crea guardan datos en la base de datos:
- `POST /api/v1/category`: agrega una categoría
	- ejemplo de cuerpo:
	```json
	{
	    "name": "Entretenimiento & Recreación",
	    "type": "expense"
	}
	```
	- ejemplo de respuesta (`201`): `{}`
- `POST /api/v1/merchant`: agrega un comercio
	- ejemplo de cuerpo:
	```json
	{
        "merchant_name": "El ahorrador",
        "merchant_logo": null,
        "category": "9122880f-e50f-4954-9c71-50afdf187ee5"
    }
	```
	- ejemplo de respuesta (`201`): `{}`

- `POST /api/v1/keyword`: agrega una keyword
	- ejemplo de cuerpo:
	```json
	{
		"keyword": "uber",
		"merchant": "424b4f71-d3b9-4865-84ec-b32052df1333"
	}
	```
	- ejemplo de respuesta (`201`): `{}`

- `POST /api/v1/transaction`: agrega múltiples transacciones
	- ejemplo de cuerpo:
	```json
	"transactions": [
        {
            "description": "ahorro",
            "amount": 875.29,
            "date": "2024-07-17"
        }
    ]
	```
	- ejemplo de respuesta (`201`):
	```json
	{
        "categorization_rate": 100.0,
        "merchant_rate": 0.0,
        "total_transactions": 1
    }
	```

Un ejemplo de invocación para por ejemplo, el endpoint que agrega categoría, con algún cliente REST como Postman o Insomnia puede ser:
- url: `http://127.0.0.1:8000/api/v1/category`
- método: `POST`
- *body*:
```json
{
    "name": "Entretenimiento & Recreación",
    "type": "expense"
}
```

### Docs

Se ha generado un endpoint para documentación de la API en Swagger:
`GET /api/v1/schema/swagger-ui`

Para poder usar este endpoint, es necesario ejecutar el comando que recolecta los archivos estáticos para obtener los archivos estáticos asociados a Swagger:
`python manage.py collectstatic`
