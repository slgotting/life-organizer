// location: frontend/src/routes

// +layout.js
export const prerender = true;
export const ssr = false;

// +layout.svelte
// auth guard — redirects unauthenticated users to /signin
// nonAuthenticatedRoutes: /, /signin, /signup, /signout, /forgot-password, /reset-password, /privacy-policy, /roadmap, /changelog, /landing-page

// +page.svelte  [/]
// renders LandingPage (unauthenticated) or HomePage (authenticated)

// +error.svelte
// renders 404 page or generic error page

// signin/+page.svelte  [/signin]
function handleSubmit() {} // calls handleLogin(), redirects to /

// signup/+page.svelte  [/signup]
function handleSubmit() {} // validates passwords, calls handleSignup(), optionally redirects to Stripe
function buyPlan(type) {}  // calls changePlan(type), redirects to Stripe URL

// signout/+page.svelte  [/signout]
// calls logoutUser(), redirects to /signin

// forgot-password/+page.svelte  [/forgot-password]
function handleSubmit() {} // calls handleForgotPassword(), shows success toast

// reset-password/+page.svelte  [/reset-password]
// extracts token from URL query params
function handleSubmit() {} // calls handleResetPassword(token, password), shows toast

// account-settings/+page.svelte  [/account-settings]
// onMount: loads auth data + email from localStorage
// renders Subscription component + delete account modal
// delete callback: handleDeleteAccount(email, token, errorCallback)

// example/+page.svelte  [/example]
// redirects to /signin if not authenticated
function exampleFormRequest() {} // calls authenticatedFormRequest() with example endpoint

// landing-page/+page.svelte  [/landing-page]
// renders LandingPage component

// privacy-policy/+page.svelte  [/privacy-policy]
// static privacy policy content

// roadmap/+page.svelte  [/roadmap]
// renders Roadmap component

// changelog/+page.svelte  [/changelog]
// renders Change components per version entry

// lifetime-success/+page.svelte  [/lifetime-success]
// static post-purchase success page

// subscribe-success/+page.svelte  [/subscribe-success]
// extracts type query param, displays subscription thank-you message

// test/+page.svelte  [/test]
// renders DescriptionWithArrowRight component

// organizer/+page.svelte  [/organizer]
// onMount: loads tasks, schedule, config, active session, capacity
// tab: 'today' | 'week' | 'tasks'
async function loadAll(): ...          // fetches all organizer data in parallel
async function startTask(task): ...    // POST /organizer/tasks/:id/start
async function stopTask(): ...         // POST /organizer/tasks/:id/stop
async function saveTask(e): ...        // POST or PUT /organizer/tasks
async function deleteTask(task): ...   // DELETE /organizer/tasks/:id
async function saveConfig(e): ...      // POST /organizer/config
async function addSection(e): ...      // POST /organizer/sections
async function deleteSection(e): ...   // DELETE /organizer/sections/:id
async function editSection(e): ...     // PUT /organizer/sections/:id
async function refreshSchedule(): ...  // GET /organizer/schedule
