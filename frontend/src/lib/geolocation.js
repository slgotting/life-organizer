
import { Geolocation } from '@capacitor/geolocation';

export async function requestLocationPermission() {
    try {
        const status = await Geolocation.requestPermissions();
        if (status && status.location === 'granted') {
        const coordinates = await Geolocation.getCurrentPosition();
        console.log('Current location:', coordinates);
        } else {
        console.error('Location permission denied');
        }
    } catch (error) {
        console.error('Error requesting location permission:', error);
    }
}