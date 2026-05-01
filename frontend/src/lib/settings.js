import config, { buildServerEndpoint } from "../config/config";
import { authenticatedFormRequest, authenticatedGetRequest } from "./auth";
import toast from "svelte-french-toast";

export function setSettingsLocal(settings) {
    localStorage.setItem('settings', JSON.stringify(settings));
}

export async function getSettingsLocal() {
    let localSettings = localStorage.getItem('settings');
    let settings;
    if (localSettings) {
        settings = JSON.parse(localSettings);
        if (Object.entries(settings).length > 0) {
            return settings;
        }
    }
    try {
        settings = await getSettingsServer();
        setSettingsLocal(settings);
    } catch (e) {
        return {}
    }
    return settings;
}

export async function getSettingsServer() {
    let resp;
    try {
        resp = await authenticatedGetRequest(buildServerEndpoint(config.settingsEndpoint), JSON.parse(localStorage.getItem('auth')).token);
        const json = await resp.json();
        if (resp.ok) {
            const settings = {
                volume : json.volume,
                animationVolume : json.animation_volume
            }
            return settings;
        } else {
            return {}
        }
    } catch (e) {
        toast.error('There was an issue contacting the server for your settings. We apologize for the issue and are looking into it.', 5000);
        return {};
    }
}

export async function updateSettingsServer(volume, animationVolume) {
    const settingsDict = {
        volume: volume,
        animationVolume: animationVolume
    };
    setSettingsLocal(settingsDict);
    let resp;
    try {
        resp = await authenticatedFormRequest(buildServerEndpoint(config.updateSettingsEndpoint), "POST", JSON.parse(localStorage.getItem('auth')).token, settingsDict);
    } catch {
        toast.error('There was an issue contacting the server to update settings. We apologize for the issue and are looking into it.', 5000);
        return settingsDict;
    }
    if (resp.ok) {
        toast.success("Settings updated successfully");
        return settingsDict;
    } else {
        const json = await resp.json();
        toast.error(json.error);
        return settingsDict;
    }
}