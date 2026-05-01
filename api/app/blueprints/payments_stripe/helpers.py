import stripe

# unused
def get_or_create_webhook_endpoint(configured_url):
    # List all webhook endpoints
    endpoints = stripe.WebhookEndpoint.list()

    # Check if any existing webhook endpoint matches the configured URL
    for endpoint in endpoints.data:
        if endpoint.url == configured_url:
            print("Webhook endpoint already exists:", endpoint.id)
            return endpoint

    # If no matching endpoint is found, create a new one
    new_endpoint = stripe.WebhookEndpoint.create(
        enabled_events=["charge.succeeded", "charge.failed"],
        url=configured_url,
    )
    print("Created new webhook endpoint:", new_endpoint.id)
    return new_endpoint