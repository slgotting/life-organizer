<script>

export let items = []
export let bottomItems = []

export let fontSize = "1rem";
export let textColor = "white";
export let closedWidth = "5rem";
export let openWidth = "15rem";

let open = false;

let navLeftClosed = true;

function toggleNav() {
    (navLeftClosed) ? openNavLeft() : closeNavLeft();
    navLeftClosed = !navLeftClosed;
}

// function openNavLeft() {
//     $nav = $('.slg-nav-left-1');
//     $nav.css('width', '15rem');
//     let menuImg = $nav.find('i').first();
//     menuImg.css('left', '82%').text('menu_open');
//     let menuText = $nav.find('span')
//     menuText.css('display', 'inline-block').css('width', 'auto');
// }
// function closeNavLeft() {
//     $nav = $('.slg-nav-left-1');
//     $nav.css('width', '5rem');
//     let menuImg = $nav.find('i').first();
//     menuImg.css('left', '0%').text('menu')
//     let menuText = $nav.find('span')
// }

</script>

<style>
/*#region slg-nav-left-1 */
.slg-nav-left-1 {
    position: fixed;
    left:0px;
    height: calc(100vh - var(--nav-height));
    display:flex;
    flex-direction: column;
    background-color: rgb(46, 46, 46);
    align-items: center;
    z-index:1050;
    box-shadow: 2px 0px 3px 0px black;
    transition: width .5s cubic-bezier(0.65, -0.18, 0.38, 1.09);
}
.slg-nav-left-1 ul {
    list-style-type: none;
    display: flex;
    flex-direction: column;
    padding-inline-start: 0px;
    width:100%;
}
.slg-nav-left-1 ul li i {
    transition: left .5s ease-out;
    left:0%;
    position:relative;
}
.slg-nav-left-1 ul li:hover {
    filter: opacity(1);
    background-color: rgb(34, 34, 34);
}
.slg-nav-left-1 ul li {
    width:100%;
    height: 60px;
    padding: 0 1.2rem;
    filter: opacity(0.5);
    transition: .5s;
    display:flex;
    align-items:center;
    cursor:pointer;
}
.slg-nav-left-1 ul li:last-child {
    margin-top:auto;
}
.slg-nav-left-1 ul li span {
    display:none;
    margin-left: 1rem;
    color: white;
    cursor: pointer;
    overflow: hidden;
    white-space: nowrap;
}

/*#endregion slg-nav-left-1 */

</style>

<nav class="slg-nav-left-1"
    class:w-12={!open}
    class:w-48={open}
    >
    <ul>
        <li class="flex justify-center" on:click={() => open = !open}>
            Menu
        </li>
        {#each items as item}

        <li on:click={item.onclick || alert('Coming soon!')}>
            <a href={ item.href || '#' } style="color:{ textColor }; font-size:{ fontSize }">
            </a>
            <span onclick={ item.text_click || '' }>{ item.description || '' }</span>
        </li>

        {/each}
    </ul>

    <ul style="margin-top:auto;">
        {#each bottomItems as item}

        <li on:click={item.onclick || alert('Coming soon!')}>
            <a href={ item.href || '#' } style="color:{ textColor }; font-size:{ fontSize };">
                <i style="color:white;font-size:2.5rem;" class="material-icons{ item.icon_type || '' }">{ item.icon || '' }</i>
            </a>
            <span onclick={ item.text_click || '' }>{ item.description || '' }</span>
        </li>

        {/each}
    </ul>
</nav>
