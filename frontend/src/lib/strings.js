

export function toArrayOfStrings(value) {
    if (Array.isArray(value)) {
      return value.map(String);
    }
    return [String(value)];

    //   // Examples
    //   console.log(toArrayOfStrings(123)); // ["123"]
    //   console.log(toArrayOfStrings(true)); // ["true"]
    //   console.log(toArrayOfStrings([1, 2, 3])); // ["1", "2", "3"]
    //   console.log(toArrayOfStrings({key: 'value'})); // ["[object Object]"]
}
