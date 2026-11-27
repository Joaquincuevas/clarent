# Reintentar las entregas de webhooks fallidas (EJEMPLO SINTÉTICO)

## Qué

Las entregas de webhooks que fallan con un 5xx o un timeout se reintentan ahora con retroceso exponencial, para que los clientes dejen de perder eventos durante sus despliegues.

## Cómo

`deliver()` se repite hasta que el endpoint responde con algo distinto de un 5xx. El retraso se duplica tras cada fallo, empezando en 1 segundo.

## Pruebas

Se añadió `test_retries_until_success`. Se verificó a mano con un servidor local que responde 503 dos veces y después 200.
