<script>
	import {
		Player,
		Video,
		DefaultUi,
		usePlayerStore,
	} from '@vime/svelte';
	// Custom UI component.
	import TapSidesToSeek from './TapSidesToSeek.svelte';

    export let source = "/static/video/test.mp4"
    export let poster = ""

	// Obtain a ref if you need to call any methods.
	let player;
	/**
	 * All player properties are available through the store. If you prefer, you could also pass
	 * properties directly to the player and listen for events.
	 */
	const { paused } = usePlayerStore(() => player);
	const onPlaybackReady = () => {
		// ...
	};
</script>

	<Player on:vPlaybackReady={onPlaybackReady} bind:this={player}>
		<Video crossOrigin="" poster="{ poster }">
			<source data-src="{ source }" type="video/mp4">
		</Video>

		<DefaultUi>
			<TapSidesToSeek />
		</DefaultUi>
	</Player>

<style>
</style>