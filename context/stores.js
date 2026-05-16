// location: frontend/src/stores

// auth.js
export const authStore // writable({ isAuthenticated, user, token })

// settings.js
export const settingsModalOpenStore // writable(false)
export const settingsStore          // writable({})

// session.js
export const activeSessionStore // writable({ session, task, timerMin })

// pulse.js
export const pulseDataStore // writable({ tasks: Task[], sections: Section[] }) — populated by organizer page

// localStorage.js
export const getInitialState = (store, defaultInitialState) => {}
