<script>
    export let componentType = "standard"; // standard, helpText, cornerHint, leadingIcon, trailingIcon, prefixAddon, inlineAddon, doubleAddon, leadingDropdown, trailingDropdown
    export let id = "email";
    export let label = "Email";
    export let description = "Your full email address";
    export let value = "";
    export let placeholder = "you@example.com";
    export let hint = "Optional"
    export let inputClasses = "px-3 py-2 bg-inherit border border-gray-300 dark:border-gray-700  focus:ring-primary-500 focus:border-primary-500 block w-full"
    export let labelClasses = "block "
    export let disabled = false;

    export let addonText = "http://";

    export let icon = `

    `;

    export let trailingIcon = '';
</script>

{#if componentType == "standard"}
        <label for={id} class={labelClasses}>{@html label}</label>
        <div class="{label ? 'mt-1' : ''}">
            <input
                id={id}
                disabled={disabled}
                bind:value={value}
                type="text"
                class={inputClasses}
                placeholder={placeholder} />
        </div>
{:else if componentType == "helpText"}
    <div>
        <label for={id} class="block font-medium ">{label}</label>
        <div class="mt-1">
            <input
                type="text"
                class="shadow-sm focus:ring-primary-500 focus:border-primary-500 block w-full border-gray-300 rounded-md"
                placeholder={value}
                aria-describedby="email-description" />
        </div>
        <p class="mt-2 ">{description}</p>
    </div>
{:else if componentType == "cornerHint"}
    <div>
        <div class="flex justify-between">
            <label for={id} class="block font-medium ">{label}</label>
            <span class="">{hint}</span>
        </div>
        <div class="mt-1">
            <input
                type="text"
                name={id}
                id={id}
                class="shadow-sm focus:ring-primary-500 focus:border-primary-500 block w-full border-gray-300 rounded-md"
                placeholder={value}
                aria-describedby="email-optional" />
        </div>
    </div>
{:else if componentType == "leadingIcon"}
    <div>
        <label for={id} class="block font-medium ">{label}</label>
        <div class="mt-1 relative rounded-md shadow-sm">
            <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                <!-- Heroicon name: solid/mail -->
                <svg class="h-5 w-5 ">
                    <path d="M2.003 5.884L10 9.882l7.997-3.998A2 2 0 0016 4H4a2 2 0 00-1.997 1.884z" />
                    <path d="M18 8.118l-8 4-8-4V14a2 2 0 002 2h12a2 2 0 002-2V8.118z" />
                </svg>
            </div>
            <input
                type="text"
                name={id}
                id={id}
                class="focus:ring-primary-500 focus:border-primary-500 block w-full pl-10 sm"
                placeholder={value} />
        </div>
    </div>
{:else if componentType == "trailingIcon"}
    <div>
        <label for="account-number" class="block ">Account number</label>
        <div class="mt-1 relative rounded-md shadow-sm">
            <input
                type="text"
                name="account-number"
                id="account-number"
                class="focus:ring-primary-500 focus:border-primary-500 block w-full pr-10 sm"
                placeholder="000-00-0000" />
            <div class="absolute inset-y-0 right-0 pr-3 flex items-center pointer-events-none">
                <!-- Heroicon name: solid/question-mark-circle -->
                <svg class="h-5 w-5 ">
                    <path
                        fill-rule="evenodd"
                        d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-8-3a1 1 0 00-.867.5 1 1 0 11-1.731-1A3 3 0 0113 8a3.001 3.001 0 01-2 2.83V11a1 1 0 11-2 0v-1a1 1 0 011-1 1 1 0 100-2zm0 8a1 1 0 100-2 1 1 0 000 2z"
                        clip-rule="evenodd" />
                </svg>
            </div>
        </div>
    </div>
{:else if componentType == "prefixAddon"}
    <div>
        <label for="company-website" class="block "> Company Website </label>
        <div class="mt-1 flex rounded-md shadow-sm">
            <span class="inline-flex items-center px-3 rounded-l-md border border-r-0 border-gray-300 bg-gray-50 ">{addonText}</span>
            <input
                type="text"
                name="company-website"
                id="company-website"
                class="flex-1 min-w-0 block w-full px-3 py-2 rounded-none rounded-r-md focus:ring-primary-500 focus:border-primary-500 sm"
                placeholder="www.example.com" />
        </div>
    </div>
{:else if componentType == "inlineAddon"}
    <div>
        <label for="company-website" class="block ">Company Website</label>
        <div class="mt-1 relative rounded-md shadow-sm">
            <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                <span class="">{addonText}</span>
            </div>
            <input
                type="text"
                name="company-website"
                id="company-website"
                class="focus:ring-primary-500 focus:border-primary-500 block w-full pl-16 sm:pl-14 sm"
                placeholder="www.example.com" />
        </div>
    </div>
{:else if componentType == "doubleAddon"}
    <div>
        <label for="price" class="block ">Price</label>
        <div class="mt-1 relative rounded-md shadow-sm">
            <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                <span class=""> $ </span>
            </div>
            <input
                type="text"
                name="price"
                id="price"
                class="focus:ring-primary-500 focus:border-primary-500 block w-full pl-7 pr-12 sm"
                placeholder="0.00"
                aria-describedby="price-currency" />
            <div class="absolute inset-y-0 right-0 pr-3 flex items-center pointer-events-none">
                <span class=""> USD </span>
            </div>
        </div>
    </div>
{:else if componentType == "leadingDropdown"}
    <div>
        <label for="phone-number" class="block ">Phone Number</label>
        <div class="mt-1 relative rounded-md shadow-sm">
            <div class="absolute inset-y-0 left-0 flex items-center">
                <label for="country" class="sr-only">Country</label>
                <select
                    id="country"
                    name="country"
                    autocomplete="country"
                    class="focus:ring-primary-500 focus:border-primary-500 h-full py-0 pl-3 pr-7 border-transparent bg-transparent ">
                    <option>US</option>
                    <option>CA</option>
                    <option>EU</option>
                </select>
            </div>
            <input
                type="text"
                name="phone-number"
                id="phone-number"
                class="focus:ring-primary-500 focus:border-primary-500 block w-full pl-16 sm"
                placeholder="+1 (555) 987-6543" />
        </div>
    </div>
{:else if componentType == "trailingDropdown"}
    <div>
        <label for="price" class="block ">Price</label>
        <div class="mt-1 relative rounded-md shadow-sm">
            <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                <span class=""> $ </span>
            </div>
            <input
                type="text"
                name="price"
                id="price"
                class="focus:ring-primary-500 focus:border-primary-500 block w-full pl-7 pr-12 sm"
                placeholder="0.00" />
            <div class="absolute inset-y-0 right-0 flex items-center">
                <label for="currency" class="sr-only">Currency</label>
                <select
                    id="currency"
                    name="currency"
                    class="focus:ring-primary-500 focus:border-primary-500 h-full py-0 pl-2 pr-7 border-transparent bg-transparent ">
                    <option>USD</option>
                    <option>CAD</option>
                    <option>EUR</option>
                </select>
            </div>
        </div>
    </div>
{/if}
