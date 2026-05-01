
export function timeFunc(promiseFunc, args) {
    return new Promise(async (resolve, reject) => {
        try {
            const t0 = new Date().getTime();
            const output = (args) ? await promiseFunc(...args) : await promiseFunc();
            resolve([(new Date().getTime() - t0), output]);
        } catch (error) {
            reject(error);
        }
    });
}

export function waitAtLeast(haveWaited, totalWaitTime) {
    return new Promise((resolve, reject) => {
        try {
            if (haveWaited > totalWaitTime) {
                resolve();
            } else {
                setTimeout(() => {
                    resolve();
                }, totalWaitTime - haveWaited);
            }
        } catch (error) {
            reject(error);
        }
    })
}