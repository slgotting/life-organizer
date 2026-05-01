/**
* Checks a certain keys value in each object in an array, returning the desired value if not taken, or suffixed with the first numerical equivalent available
* Example: getUniqueValueInListOfObjects([{x: 1}, {x: Untitled}, {x: Untitled-0}], "x", "Untitled") => "Untitled-1"
*
* Another name might be something like "conformNameToOtherObjects"
* @function
* @param {array} listOfObjs list of the
* @param {string} key Key to check in each object
* @param {number} value Desired value for key
* @returns {string} First [potentially suffixed] value that isn't taken
*/
export function getUniqueValueInListOfObjects(listOfObjs, key, value) {
    // check if exists without suffix first
    let exists = false;
    for (let i=0; i<listOfObjs.length; i++) {
        if (value == listOfObjs[i][key]) {
            exists = true;
            break;
        }
    }
    if (!exists) {
        return value
    }

    // if we didnt return with the value, we check for suffixed names
    for (let i=0; i<999; i++) {
        exists = false;
        for (let j=0; j<listOfObjs.length; j++) {
            if (`${value}-${i}` == listOfObjs[j][key]) {
                exists = true;
                break;
            }
        }
        if (!exists) {
            return `${value}-${i}`
        }
    }
}