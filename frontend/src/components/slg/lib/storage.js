import { addToLocalStorage, getFromLocalStorage } from "./localStorage";


export function addKeyValueToStorage({
    key=null,
    value=null,
    storageType='localStorage',
    options={}
} = {}) {
    // values are automatically handled, simply pass the raw value

    if (storageType == 'localStorage') {
        addToLocalStorage(key, value);
    }
}

export function getKeyFromStorage({
    key=null,
    storageType='localStorage',
    options={}
} = {}) {
    // values are automatically handled, simply pass the raw value

    if (storageType == 'localStorage') {
        return getFromLocalStorage(key);
    }
}