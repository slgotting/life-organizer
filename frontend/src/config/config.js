import { configDev } from './config.dev';
import { configDevLAN } from './config-lan.dev';
import { configStaging } from './config.staging';
import { configProd } from './config.prod';

let config = {
    // template endpoints
    loginEndpoint: '/auth/sign_in',
    signUpEndpoint: '/auth/sign_up',
    forgotPasswordEndpoint: '/auth/forgot-password',
    resetPasswordEndpoint: '/auth/reset-password',
    deleteAccountEndpoint: '/auth/delete_account',
    settingsEndpoint: '/settings',
    updateSettingsEndpoint: '/update_settings',
    subscriptionDetailsEndpoint: '/subscription/details',
    changePlanEndpoint: '/subscription/change_plan',
    cancelPlanEndpoint: '/subscription/cancel_plan',
    stripeCustomerPortalEndpoint: '/subscription/stripe-customer-portal-session',
    lifetimeAccessPurchaseEndpoint: '/subscription/purchase_lifetime_access',
    // |UPDATE_ME|
    publicStripeKey: 'pk_test_51PZtwRBIjE5s9OuTbrRCVjgtHoXBMArzAfiI5pVkXG4QrWtZELzBqTCXx61yDCxISpnJDKbjVsOmGRNPPGFaEWzM00Mbt4zXcD',
    webGoogleOauthClientId: "%%WEB_GOOGLE_OAUTH_CLIENT_ID%%",
    androidGoogleOauthClientId: "%%ANDROID_GOOGLE_OAUTH_CLIENT_ID%%",
    iosGoogleOauthClientId: "%%IOS_GOOGLE_OAUTH_CLIENT_ID%%",

    // unique endpoints

}

if (import.meta.env.MODE === 'production') {
  config = Object.assign({}, config, configProd);
} else if (import.meta.env.MODE === 'staging') {
  config = Object.assign({}, config, configStaging);
} else if (import.meta.env.MODE === 'dev-lan') {
  config = Object.assign({}, config, configDevLAN);
} else {
  config = Object.assign({}, config, configDev);
}


export function buildServerEndpoint(endpoint) {
    if (config.useHTTPS) {
        return `https://${config.serverName}${endpoint}`
    } else {
        return `http://${config.serverName}${endpoint}`
    }
}

export default config;