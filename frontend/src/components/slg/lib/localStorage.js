
export function addToLocalStorage(key, val, default_) {
    localStorage.setItem(key, JSON.stringify(val ? val : default_))
}
export function getFromLocalStorage(key) {
    return JSON.parse(localStorage.getItem(key))
}