

export function playAudioElement(audioElement, volume=0.3) {
    // handles restarting the sound if its already playing
    audioElement.volume = volume
    audioElement.pause();
    audioElement.currentTime = 0;
    audioElement.play();
}

export function playPause(sound, vol) {
    sound.volume = vol;
    sound.currentTime = 0;
    sound.play();
}

export function playSoundAtVolume(sound, vol = 0.4) {
    if (!vol) {
        vol = 0.2;
    }
    vol = parseFloat(vol);
    playPause(sound, vol);
}

export function playSoundNoInterrupt(sound, vol) {
    if (!vol) {
        vol = 0.2;
    }
    vol = parseFloat(vol);
    const audio = sound.cloneNode(true);
    audio.volume = vol;
    audio.play();
}