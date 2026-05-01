<script>
    export let width = 100;

    let frame;
    let win;
    let doc;
    let head;
    let body;
    let content;
    let component;
    let props;
    $: {
        ({ component, ...props } = $$props);
        try { content.set(props) } catch {}
        // if (content) console.log(content);// content.set(props);
    }
    $: if (frame) {
        frame.addEventListener("load", loadHandler);
        if (frame.contentDocument.readyState === "complete" && frame.contentDocument.defaultView) {
            loadHandler();
        } else {
            frame.addEventListener("load", loadHandler);
        }
    }
    function loadHandler() {
        win = frame.contentWindow;
        doc = frame.contentDocument;
        head = doc.head;
        body = doc.body;
        doc.insertBefore(document.doctype.cloneNode(true), doc.documentElement);
        const style = doc.createElement("style");
        style.innerText = `html,body {
    background: none !important;
    margin: 0 !important;
    padding: 0px !important;
    overflow: hidden !important;
    height: 100% !important;
  }`;
        head.appendChild(style);
        Array.from(document.querySelectorAll('style, link[rel="stylesheet"]')).forEach((node) => head.appendChild(node.cloneNode(true)));
        if (component) {
            content = new component({ target: body, props });
        }

        body.style.display = "flex"

        const widthHandle = doc.createElement('div');
        widthHandle.innerText = 'handle'
        widthHandle.style.width = '20px';
        widthHandle.style.height = '20px';
        widthHandle.style.marginLeft = 'auto';
        body.appendChild(widthHandle);
    }

    $: updateWidth(width);

    function updateWidth(width) {
        try {
            frame.style.width = `${width}%`;
        } catch {}
    }
</script>

<iframe bind:this={frame} title height=500 />

<style>
    iframe {
        border: 2px solid black;
        width: 100%;
    }
</style>
