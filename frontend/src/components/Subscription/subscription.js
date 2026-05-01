import config, { buildServerEndpoint } from "../../config/config";
import { authenticatedFormRequest, authenticatedGetRequest } from "../../lib/auth";
import toast from "svelte-french-toast";

export async function getSubscriptionDetails() {
    try {
        const token = JSON.parse(localStorage.getItem('auth')).token;
        const resp = await authenticatedGetRequest(
            buildServerEndpoint(config.subscriptionDetailsEndpoint),
            token
        );
        const json = await resp.json();

        if (resp.ok) {
            return json;
        } else {
            toast.error('An unknown error has occurred. We apologize for the inconvenience and are looking into the issue.', 5000);
            return {};
        }
    } catch (e) {
        toast.error('There was an issue contacting the server.', 5000);
        return {};
    }
}

export async function changePlan(plan, paymentType) {
    let resp;
    try {
        resp = await authenticatedFormRequest(
            buildServerEndpoint(config.changePlanEndpoint),
            "POST",
            JSON.parse(localStorage.getItem('auth')).token,
            {
                plan: plan,
                paymentType: paymentType
            }
        )
        if (resp.ok) {
            const data = await resp.json();
            return data;
        } else {
            toast.error('An unknown error has occurred. We apologize for the inconvenience and are looking into the issue.', 5000);
            return false;
        }
    } catch (e) {
        toast.error('There was an issue contacting the server.', 5000);
        return false;
    }
}

export async function purchaseLifetimeAccess(paymentType) {
    let resp;
    try {
        resp = await authenticatedFormRequest(
            buildServerEndpoint(config.lifetimeAccessPurchaseEndpoint),
            "POST",
            JSON.parse(localStorage.getItem('auth')).token,
            {
                paymentType: paymentType
            }
        )
        if (resp.ok) {
            const data = await resp.json();
            return data;
        } else {
            toast.error('An unknown error has occurred. We apologize for the inconvenience and are looking into the issue.', 5000);
            return false;
        }
    } catch (e) {
        toast.error('There was an issue contacting the server.', 5000);
        return false;
    }
}

export async function cancelPlan() {
    let resp;
    try {
        resp = await authenticatedFormRequest(
            buildServerEndpoint(config.cancelPlanEndpoint),
            "POST",
            JSON.parse(localStorage.getItem('auth')).token,
        )
        if (resp.ok) {
            const data = await resp.json();
            return data;
        } else {
            toast.error('An unknown error has occurred. We apologize for the inconvenience and are looking into the issue.', 5000);
            return false;
        }
    } catch (e) {
        toast.error('There was an issue contacting the server.', 5000);
        return false;
    }
}

export async function openStripeCustomerPortal() {
    let resp;
    try {
        resp = await authenticatedGetRequest(
            buildServerEndpoint(config.stripeCustomerPortalEndpoint),
            JSON.parse(localStorage.getItem('auth')).token,
        )
    } catch (e) {
        toast.error('There was an issue contacting the server.', 5000);
        return false;
    }
    if (resp.ok) {
        const data = await resp.json();
        return data;
    } else {
        toast.error('An unknown error has occurred. We apologize for the inconvenience and are looking into the issue.', 5000);
        return false;
    }
}
