

// Function to get initial state from localStorage
export const getInitialState = (store, defaultInitialState) => {
    const state = localStorage.getItem(store);
    return state ? JSON.parse(state) : defaultInitialState;
};