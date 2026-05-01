// location: frontend/src/components/slg/lib

// array.js
export function getUniqueValueFromArray(array, desiredString) {}
export function getFirstUniqueId(array, baseIndex=1) {}

// arrayOfObjects.js
export function getUniqueValueInListOfObjects(listOfObjs, key, value) {}

// async.js
export function timeFunc(promiseFunc, args) {}
export function waitAtLeast(haveWaited, totalWaitTime) {}

// clipboard.js
export function copyElemText(elem) {}

// date.js
export { format, parse, isSameDay, isDate }

// debounce.js
export function debounce(func, delay) {}

// errorHandling.js
export function getVariableOrDefault(variable, default_) {}

// localStorage.js
export function addToLocalStorage(key, val, default_) {}
export function getFromLocalStorage(key) {}

// measurements.js
export function getDivOuterHeight() {}

// objects.js
export function invertObject(obj) {}

// requests.js
export const objectToFormData = (obj) => {}

// scroll.js
export function scrollIntoView({ target }) {}
export function visible(element) {}

// sounds.js
export function playAudioElement(audioElement, volume=0.3) {}
export function playPause(sound, vol) {}
export function playSoundAtVolume(sound, vol=0.4) {}
export function playSoundNoInterrupt(sound, vol) {}

// storage.js
export function addKeyValueToStorage({ }) {}
export function getKeyFromStorage({ }) {}

// string.js
export function shortenString(string, maxLength=36) {}

// stores/arrays.js
export function addElemToStoreArray(storeVar, elem) {}
export function updateIdxForStoreArray(storeVar, idx, elem) {}

// stores/objects.js
export function addKeyToStoreObject(storeVar, key, value) {}
export function updateKeyNameForStoreObject(storeVar, key, newKey) {}
