

export function deepCopy(obj) {
    if (typeof obj !== 'object' || obj === null) {
        // If obj is not an object or is null, return it directly
        return obj;
    }

    // Create an empty object to store the copied properties
    const newObj = Array.isArray(obj) ? [] : {};

    // Iterate over each property in the original object
    for (let key in obj) {
        // Recursively deep copy nested objects and arrays
        newObj[key] = deepCopy(obj[key]);
    }

    return newObj;
}
