<script>
    import Component from "./Component.svelte";
    import config, { buildServerEndpoint } from "../../config/config";
    import { authenticatedFormRequest } from "../../lib/auth";
    import { authStore } from "../../stores/auth";
    import { goto } from "$app/navigation";

    if (!$authStore.isAuthenticated) {
        goto("/signin");
    }

    const exampleFormRequest = () => authenticatedFormRequest(
        buildServerEndpoint(config.exampleEndpoint),
        "POST",
        JSON.parse(localStorage.getItem('auth')).token,
        {'data': 'example data'}
    );
</script>

<Component node={{ id: crypto.randomUUID(), children: [] }} />
