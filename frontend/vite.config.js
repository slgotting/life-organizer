import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig } from 'vite';
import mkcert from 'vite-plugin-mkcert'


export default defineConfig({
    // server: { https: true }, // Not needed for Vite 5+

    // FOR HTTPS UNCOMMENT THIS AND VISIT capacitor.config.json AND UPDATE THE HOST URL TO https
	// plugins: [sveltekit(), mkcert()]

	plugins: [sveltekit()]
});
