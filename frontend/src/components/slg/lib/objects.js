

export function invertObject(obj) {
    // inverts a simple object, no nesting
    // THIS ALSO SWITCHES TYPES OF KEYS IF THEY ARE AN int (only one tested)
    // so {3: 4} will invert to {4: '3'}
    // stupid i know :facepalm:

    return Object.fromEntries(Object.entries(obj).map(elem => [elem[1], elem[0]]));
}