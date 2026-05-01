export function scrollIntoView({ target }) {
    const el = document.querySelector(target.getAttribute('href'));
    console.log(el.getBoundingClientRect());
    if (!el) return;
    el.scrollIntoView({
        behavior: 'smooth'
    });
}


export function visible(element) {

}