# Retry failed webhook deliveries (SYNTHETIC EXAMPLE)

## What

Webhook deliveries that fail with a 5xx or a timeout are now retried with exponential backoff, so customers stop losing events during their deploys.

## How

`deliver()` loops until the endpoint answers with something other than a 5xx. The delay doubles after each failure, starting at 1 second.

## Testing

Added `test_retries_until_success`. Verified by hand against a local server that answers 503 twice and then 200.
