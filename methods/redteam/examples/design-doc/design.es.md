# Diseño: enviar notificaciones desde un consumidor de streams (EJEMPLO SINTÉTICO)

Estado: propuesto. Responsable: equipo de plataforma.

## Contexto

Las notificaciones (correo y push) se envían hoy con un cron que recorre la tabla `notifications` cada minuto.
En hora punta el recorrido tarda 40 segundos y algunas notificaciones salen tarde.

## Propuesta

1. La API escribe cada notificación en la tabla `notifications` y, en la misma petición, publica su id en un Redis Stream llamado `notify`.
2. Un grupo de 4 consumidores lee el stream mediante un consumer group, llama al proveedor de correo y marca la fila como `sent`.
3. Cada consumidor confirma el mensaje (ack) apenas lo lee, de modo que una llamada lenta al proveedor nunca bloquea al grupo.
4. El cron se elimina en el mismo despliegue.

## Supuestos

- Redis casi siempre está disponible cuando la API publica; si no lo está, la notificación queda en la tabla y se enviará más tarde.
- El proveedor de correo acepta como máximo un mensaje por segundo por consumidor, y con 4 consumidores nos quedamos por debajo.
- Las notificaciones rara vez se duplican, así que los consumidores no necesitan ser idempotentes.
- La carga en hora punta seguirá por debajo de 200 notificaciones por minuto.

## Despliegue

El grupo de consumidores se activa detrás de un flag. Cuando el flag esté activo para todos los usuarios, se elimina el cron
y su código, y la columna antigua `notifications.sent_at` se borra en la siguiente migración.
