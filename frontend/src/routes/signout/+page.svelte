<script>
    import { logoutUser } from '../../lib/auth'
    import { goto } from "$app/navigation";
    import { authStore } from "../../stores/auth";

    const isAuthenticated = $authStore.isAuthenticated;

    if (isAuthenticated) {
        logoutUser(() => goto('/signin'));
    }
</script>

<div></div>