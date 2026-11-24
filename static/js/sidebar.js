document.addEventListener("DOMContentLoaded", () => {
    const toggleButton = document.getElementById("sidebar-toggle");
    if (!toggleButton) return;

    const root = document.documentElement;

    function updateButton(collapsed) {
        toggleButton.setAttribute("aria-expanded", String(!collapsed));
        toggleButton.setAttribute("aria-label", collapsed ? "Expandir menú lateral" : "Contraer menú lateral");
    }

    updateButton(root.classList.contains("sidebar-collapsed"));

    toggleButton.addEventListener("click", () => {
        const collapsed = root.classList.toggle("sidebar-collapsed");
        updateButton(collapsed);
        localStorage.setItem("sidebar-collapsed", String(collapsed));
    });
});
