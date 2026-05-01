<script>
  import Dropzone from 'svelte-file-dropzone'
//   import Confirm from '../components/Confirm.svelte'

  let confirmHidden = true

  export let optClass = ''
  export let numCols = 0
  export let columnHeaders = []
  export let csvData = [[]]

  export let fileUploaded = false

  let files = []
  function processRawCSV(data) {
    const output = []
    const rows = data.split('\n')
    for (let i = 0; i < rows.length; i++) {
      const cells = rows[i].split(',')
      output.push(cells)
    }
    console.log(output)
    return output
  }
  function handleFilesSelect(e) {
    files = e.detail.acceptedFiles
    for (let i = 0; i < files.length; i++) {
      const reader = new FileReader()
      reader.onload = () => {
        const binaryStr = reader.result
        console.log('processing')
        csvData = processRawCSV(binaryStr)
        fileUploaded = true
      }
      reader.readAsText(files[i])
    }
  }

  $: columnHeaders = csvData[0]
  $: numCols = getMaxColSize(csvData)

  function getMaxColSize(csvData) {
    let max = 0
    csvData.forEach(arr => {
      if (arr.length > max) {
        max = arr.length
      }
    })
    console.log(max)
    return max
  }

  function resetAll() {
    fileUploaded = false
    files = []
    numCols = 0
    columnHeaders = []
    csvData = [[]]
    confirmHidden = true
  }
</script>

<div class="flex w-64 {optClass}" class:cursor-pointer={fileUploaded == false}>
  {#if fileUploaded == true}
    <Dropzone disabled="true">
      <div class="flex">
        <p class="text-xl">{files[0].name}</p>
        <svg
          on:click={() => (confirmHidden = false)}
          class="w-8 h-8 text-red-400 cursor-pointer ml-4"
          xmlns="http://www.w3.org/2000/svg"
          viewBox="0 0 22 22">
          <path
            style="fill:currentColor;fill-opacity:1;stroke:none"
            d="M 8 3 L 0.94335938 10.056641 L 0 11 L 0.94335938 11.943359 L 8 19 L 20.333984 19 L 22 19 L 22 3 L
            20.333984 3 L 8 3 z M 11.320312 7 L 14 9.6796875 L 16.679688 7 L 18 8.3203125 L 15.320312 11 L 18 13.679688
            L 16.679688 15 L 14 12.320312 L 11.320312 15 L 10 13.679688 L 12.679688 11 L 10 8.3203125 L 11.320312 7 z "
            class="ColorScheme-Text" />
        </svg>
      </div>
    </Dropzone>
    <div class="absolute w-64 z-50 {confirmHidden ? 'hidden' : 'block'}">
      <!-- <Confirm yesFunction={() => resetAll()} noFunction={() => (confirmHidden = true)}>
        Are you sure? Any progress will be lost.
      </Confirm> -->
    </div>
  {:else}
    <Dropzone on:dropaccepted={handleFilesSelect} accept="text/csv" multiple="false">
      Drop your .csv file here, or click to select one
    </Dropzone>
  {/if}
</div>
