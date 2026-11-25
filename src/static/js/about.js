// The FAQ is plain <details name="faq"> elements, so the browser handles opening, closing and
// keyboard use. On desktop the open answer is shown in a side panel (see style.css), so one
// question must always stay open.
document.addEventListener("DOMContentLoaded", () => {
    const items = Array.from(document.querySelectorAll(".faq-item"));
    if (items.length === 0) {
        return;
    }

    const desktop = window.matchMedia("(min-width: 900px)");

    const ensureOneOpen = () => {
        if (desktop.matches && !items.some((item) => item.open)) {
            items[0].open = true;
        }
    };

    items.forEach((item) => {
        item.querySelector("summary").addEventListener("click", (event) => {
            if (desktop.matches && item.open) {
                event.preventDefault();
            }
        });
    });

    desktop.addEventListener("change", ensureOneOpen);
    ensureOneOpen();
});
