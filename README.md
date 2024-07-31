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
	"date": "2023-12-01",
}
```

Categoría
```json
{
	"id":"uuid4",
	"name": "Restaurantes",
	"type": "expense"
}
```

Comercio
```json
{
	"id":"uuid4",
	"merchant_name": "Uber Eats",
	"merchant_logo" : "http://...",
	"category": "category_id"
}
```

Keyword
```json
{
	"id":"uuid4",
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
> id:1
> descripción: "tienda de abarrotes la"
> amount: -123
> date: "2023-12-01"
> Es fácil identificar que la categoría corresponde a Supermercados y Tiendas de alimentos, pero es imposible definir el comercio.
