<script>
  export let choices = [];
  export let disabledChoices = [];

  export let disabledInfo = "";
  export let activeChoice = "";

  export let wrapperClass = "";

  export let textSize = "xs";
  export let squareEdges = false;
  export let color = "purple";

  export let baseClass = "transform px-2 focus:outline-none relative";
  export let inactiveClass = `z-0 hover:bg-${color}-500 bg-${color}-100 dark:bg-${color}-200 border-${color}-200 text-gray-700`;
  export let activeClass = `border rounded-sm scale-110 bg-${color}-400 border-${color}-400 shadow-md text-white z-10`;

  //   console.log(disabledChoices);
  //   console.log(choices);

  function updateChoice(choice) {
    if (!disabledChoices.includes(choice)) {
      activeChoice = choice;
    }
  }
  function getFirstNonDisabledChoice() {
    let choice;
    for (let i = 0, j = choices.length; i < j; i++) {
      if (!disabledChoices.includes(choices[i])) {
        choice = choices[i];
        i += j;
      }
    }
    return choice;
  }

  if (!activeChoice) {
    let choice = getFirstNonDisabledChoice();
    updateChoice(choice);
  }
</script>

<style>
  /* NOTE: .disabled is currently being imported from globals.pcss file. @apply does not apply dark: in this context for some reason
        https://github.com/tailwindlabs/tailwindcss/discussions/2917
*/
  /* .disabled {
    color: gray;
    background-color: lightgrey;
    cursor: default;
    border-color: lightgrey;
  } */
</style>

<div class={wrapperClass}>
  {#each choices as choice, idx}
    {#if idx == 0}
      <button
        class="{activeChoice == choice ? activeClass : inactiveClass}
        {baseClass} border-l border-t border-b text-{textSize}"
        on:click={() => updateChoice(choice)}
        class:rounded-l-md={!squareEdges}
        class:radio-multi-select-active={choice == activeChoice}
        class:disabled={disabledChoices.includes(choice)}
        title={disabledChoices.includes(choice) ? disabledInfo : ''}>
        {choice}
      </button>
    {:else if idx == choices.length - 1}
      <button
        class="{activeChoice == choice ? activeClass : inactiveClass}
        {baseClass} border text-{textSize}"
        on:click={() => updateChoice(choice)}
        class:rounded-r-md={!squareEdges}
        class:radio-multi-select-active={choice == activeChoice}
        class:disabled={disabledChoices.includes(choice)}
        title={disabledChoices.includes(choice) ? disabledInfo : ''}>
        {choice}
      </button>
    {:else}
      <button
        class="{activeChoice == choice ? activeClass : inactiveClass}
        {baseClass} border-t border-b border-l text-{textSize}"
        on:click={() => updateChoice(choice)}
        class:radio-multi-select-active={choice == activeChoice}
        class:disabled={disabledChoices.includes(choice)}
        title={disabledChoices.includes(choice) ? disabledInfo : ''}>
        {choice}
      </button>
    {/if}
  {/each}
</div>
