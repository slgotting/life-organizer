# Requirements

tailwind-dark-aware

```javascript
// In tailwind.config.js

import darkAware from 'tailwind-dark-aware';

plugins: [
    darkAware({}),
    // Other plugins
]
```


In order to create the tree you must run (this may change and I forget to update this, so be wary and use test directory first):

    1. ./build-component-tree -p 'library' -a
    2. ./create-component-library-pages -i /home/steven/time-log-app/src/components/slg -o /home/steven/time-log-app/src/pages/library

This builds a component tree with hrefs with the prefix "library" and then
creates the pages themselves in the output folder

Note: create-component-library-pages requires absolute paths

## Notes on component creation

### Component types

Should use `export let componentType = "example" // each, type, separated, by commas`

Any different types of component that you can define as a variable should use the export variable `export let componentType = "example"`

### Bindable variables

Should contain the word value in its name with a description following a comment //

If you wish for the variable to not be considered a variable, add a suffix

Example: `export let inputValue = "test" // This is the value of the input box associated with this.`

Note: Perhaps just assigning bindable status to anything that uses a "let" assign to a variable should be considered bindable.

### Nonbindable variables

Use const directive to define nonbindable variables

Example: `export const title="" // The topmost header title for your component.`

# The whole bindable/ non bindable thing needs to be tested on my end before implementing anything

# I do, however, want certain values to be defined explicitly as bindable and for those to be guaranteed to be able to be bound to
