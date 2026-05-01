// location: frontend/src/lib

// image.js
export function preloadImagePromise(src, onError) {}
export function preloadImage(src, onError) {}

// api.js
export const handleApiResponse = async (response) => {}

// copy.js
export function deepCopy(obj) {}

// geolocation.js
export async function requestLocationPermission() {}

// strings.js
export function toArrayOfStrings(value) {}

// notifications.js
export const scheduleNotifications = async () => {}

// auth.js
export const handleLogin = async (email, password, failureCallback) => {}
export const handleSignup = async (email, password, confirmPassword, failureCallback) => {}
export const handleForgotPassword = async (email, failureCallback) => {}
export const handleResetPassword = async (token, password, failureCallback) => {}
export const handleDeleteAccount = async (email, token, failureCallback) => {}
export const logoutUser = (callback) => {}
export const authenticatedPostRequest = (url, token) => {}
export const authenticatedGetRequest = (url, token) => {}
export const authenticatedFormRequest = async (url, method, token, data) => {}
export const authenticatedJSONRequest = async (url, method, token, data) => {}

// settings.js
export function setSettingsLocal(settings) {}
export async function getSettingsLocal() {}
export async function getSettingsServer() {}
export async function updateSettingsServer(volume, animationVolume) {}
