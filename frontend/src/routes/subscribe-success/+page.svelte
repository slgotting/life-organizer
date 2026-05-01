
<script>
    const urlParams = new URLSearchParams(window.location.search);
    const type = urlParams.get('type');
</script>

<div class="flex justify-center">
    <main class="max-w-screen-sm">
        <div class="py-16">
            <div class="text-center flex flex-col justify-center items-center">
                <h1 class="mt-2 text-4xl font-bold tracking-tight text-gray-900 dark:text-white sm:text-5xl">Thank you!</h1>
                <p class="mt-2 text-base text-gray-500">You've successfully subscribed to the {type} plan!</p>
                <div class="mt-6">
                    <a href="/" class="text-base font-medium text-primary-500 hover:text-primary-600">
                        Go back home
                        <span aria-hidden="true"> &rarr;</span>
                    </a>
                </div>
            </div>
        </div>
    </main>
</div>