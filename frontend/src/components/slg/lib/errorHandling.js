
/**
* This is for handling issues with accessing bound variables and if they have not yet been created
* We return a default object if the object is null or undefined so that that variable can be populated later
* This could have potentially nasty side effects if the variable is needed to be defined.
* Example: getOrDefault(variable, default)
* @function
* @param {string} variable What is the variable we are trying to access?
* @returns {string} The variable, if defined, or the default
*/
export function getVariableOrDefault(variable, default_) {
    try {
        return variable
    } catch {
        return default_
    }
}