
export function addKeyToStoreObject(storeVar, key, value) {
    storeVar.update(t => {
        t[key] = value;
        return t
    })
}

export function updateKeyNameForStoreObject(storeVar, key, newKey) {
    storeVar.update(t => {
        t[newKey] = t[key];
        delete t[key];
        return t
    })
}