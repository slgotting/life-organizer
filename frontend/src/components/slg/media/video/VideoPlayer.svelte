<script>

    export let example = false;

    import VideoPlayer from 'svelte-video-player';

    const poster = 'https://www.server.com/poster.jpg';
    const source = [
        'https://www.server.com/video.webm',
        'https://www.server.com/video.mp4',
        'https://www.server.com/video.ogv',
    ];

</script>

{#if example}

    <svelte:self />

{:else}

<VideoPlayer {poster} {source} />

{/if}