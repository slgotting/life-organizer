<!-- @format -->
<script>
    import { authStore } from "../stores/auth";
    import LandingPage from "../components/LandingPage/Main.svelte";
    import HomePage from "../components/HomePage/Main.svelte";
</script>

{#if !$authStore.isAuthenticated}
    <LandingPage />
{:else}
    <HomePage />
{/if}