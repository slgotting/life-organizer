import config, { buildServerEndpoint } from "../config/config";
import { LocalNotifications } from "@capacitor/local-notifications";
import { authenticatedFormRequest, authenticatedGetRequest, authenticatedJSONRequest } from "./auth";
import { getSettingsLocal } from "./settings";


export const scheduleNotifications = async () => {
    try {
        const permissionState = await LocalNotifications.requestPermissions(); // 'prompt' | 'prompt-with-rationale' | 'granted' | 'denied';
        if (permissionState.display != "granted") {
            return;
        }

        let notifyInterval;

        const settings = await getSettingsLocal();

        notifyInterval = settings.notifyInterval; // in hours

        // cancel any pending notifications and then set the notifications from this point in time
        const pendingNotifications = await LocalNotifications.getPending();
        if (pendingNotifications.length > 0) {
            await LocalNotifications.cancel(pendingNotifications.notifications.map(notif => notif.id))
        }

        // return here, after the pending notifs are canceled so we dont notify again
        if (notifyInterval === 0) {
            return;
        }

        function rangeArray(min, max) {
            return Array.from({ length: max - min + 1 }, (_, index) => index + min);
        }

        let newNotifications = [];
        let lastTime = Date.now();
        for (let i of rangeArray(1,20)) {
            let hours = notifyInterval;
            let time = new Date(lastTime + 1000 * hours * 3600) // convert from hours to seconds
            if (!time) {
                return;
            }
            newNotifications.push({
                title: "Hey, its been a while...",
                body: "...keep up your spaced repetition by doing some flashcards!",
                id: i,
                schedule: { at: time, allowWhileIdle: true },
            })
            lastTime = time.getTime();
        }
        const result = await LocalNotifications.schedule({ notifications: newNotifications });

    } catch (error) {
    }
};
