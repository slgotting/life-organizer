import darkAware from 'tailwind-dark-aware'

/** @type {import('tailwindcss').Config} */
export default {
    darkMode: 'class',
    content: [
        'frontend/src/routes/+error.svelte',
        './src/**/*.{html,js,svelte,ts}',
        './src/components/slg/**/*.{html,js,svelte,ts}'
    ],
    theme: {
        extend: {
            colors: {
                "tertiary": {"50": "#FAFAF9", "100": "#F5F5F4", "200": "#E7E5E4", "300": "#D6D3D1", "400": "#A8A29E", "500": "#78716C", "600": "#57534E", "700": "#44403C", "800": "#292524", "900": "#1C1917"},
                "primary": {"50": "#F0FDF4", "100": "#DCFCE7", "200": "#BBF7D0", "300": "#86EFAC", "400": "#4ADE80", "500": "#22C55E", "600": "#16A34A", "700": "#15803D", "800": "#166534", "900": "#14532D"},
                "secondary": {"50": "#ECFDF5", "100": "#D1FAE5", "200": "#A7F3D0", "300": "#6EE7B7", "400": "#34D399", "500": "#10B981", "600": "#059669", "700": "#047857", "800": "#065F46", "900": "#064E3B"},
            },
        },
    },
    plugins: [
        darkAware({}),
        require('@tailwindcss/forms'),
    ],
}
