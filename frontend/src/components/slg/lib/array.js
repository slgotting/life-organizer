/**
*
* Example: getUniqueValueFromArray(['Untitled', 'Untitled-0', 'Untitled-1'], "Untitled") => "Untitled-2"
* @function
* @param {array} array array of strings
* @param {desiredString} string string to add if doesnt exist. If does exist, start suffixing -0 [-999]
* @returns {string} [Potentially suffixed] desiredString value
*/
export function getUniqueValueFromArray(array, desiredString) {
    let exists = false;
    for (let i=0; i<array.length; i++) {
        if (desiredString == array[i]) {
            exists = true;
            break;
        }
    }
    if (!exists) {
        return desiredString
    }

    for (let i=0; i<array.length +1; i++) {
        exists = false;
        for (let j=0; j<array.length; j++) {
            if (`${desiredString}-${i}` == array[j]) {
                exists = true;
                break;
            }
        }
        if (!exists) {
            return `${desiredString}-${i}`
        }
    }
}



/**
*
* Example: getUniqueValueFromArray(['Untitled', 'Untitled-0', 'Untitled-1'], "Untitled") => "Untitled-2"
* @function
* @param {array} array array of objects with a key of "id"
* @returns {number} The available ID value
*/
export function getFirstUniqueId(array, baseIndex=1) {
    for (let i=baseIndex; i < array.length + baseIndex; i++) {
        let taken = false;
        for (let object of array) {
            if (object.id == i) {
                taken = true;
                break;
            }
        }
        if (!taken) {
            return i
        }
    }
    return array.length + baseIndex
}