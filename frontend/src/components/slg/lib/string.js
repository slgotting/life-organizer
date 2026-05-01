
export function shortenString(string, maxLength=36) {
    if (typeof string !== 'string') {
        throw new TypeError('Expected a string');
    }
    return (string > maxLength) ? string.slice(0, 36) + "..." : string;
}