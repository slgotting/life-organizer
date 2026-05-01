
export function preloadImagePromise(src, onError) {
    return new Promise(function (resolve) {
        let img = new Image()
        img.src = src
        img.onerror = onError;
        img.onload = resolve
    })
}

export function preloadImage(src, onError) {
    const img = new Image();
    img.src = src;
    img.onerror = onError;
    return img;
}