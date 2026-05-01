

/**
* Update a value at index for a store array
* Example: addElemToStoreArray(teams, 'Vikings')
* @function
* @param {import("svelte/store").Writable} storeVar The svelte store array
* @param {object} elem New element
* @returns {string} Store array
*/
export function addElemToStoreArray(storeVar, elem) {
    storeVar.update(arr => {
        arr.push(elem);
        return arr
    })
}

/**
* Update a value at index for a store array
* Example: updateIdxForStoreArray(teams, 0, 'Team-0')
* @function
* @param {import("svelte/store").Writable} storeVar The svelte store array
* @param {integer} idx Index of update
* @param {object} elem New element
* @returns {string} Store array
*/
export function updateIdxForStoreArray(storeVar, idx, elem) {
    storeVar.update(arr => {
        arr[idx] = elem;
        return arr
    })
}