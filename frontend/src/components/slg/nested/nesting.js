

// structure is any key that has a key that points to an array

// the leaves are considered to be the end of the recursion

// special keys will be defined as being used for handling of custom use cases

/*

Simple recursion structure
{
    key: {
        recurseKey1: {
            recurseKey1: {
                leaves: [...leaves]
            }
            leaves: [...leaves]
        },
        recurseKey2: {
            leaves: [...leaves]
        }
        leaves: [...leaves]
    }
}


Complex recursion structure (Complex is defined as using keys that have separate functionality from the main nodes/leaves
{
    key: {
        specialKey1: somethingInteresting1,
        specialKey2: somethingInteresting2
        recurseKey1: {
            specialHandling1: somethingInteresting1
            recurseKey1: {
                specialHandling1: somethingInteresting1
                leaves: [...leaves]
            }
            leaves: [...leaves]
        },
        recurseKey2: {
            specialKey1: somethingInteresting1,
            leaves: [...leaves]
        },
        leaves: [...leaves]
    }

}


*/