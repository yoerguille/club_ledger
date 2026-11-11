
document.addEventListener("DOMContentLoaded", () => {

    const sidebar = document.getElementById("sidebar-container");
    const toggleButton = document.getElementById("sidebar-toggle");
    const headings = sidebar.querySelectorAll(
        "[data-sidebar-heading]"
    );

    if (!sidebar || !toggleButton) return;

    // Textos del sidebar
    const labels = sidebar.querySelectorAll("[data-sidebar-label]");

    // Recuperar el estado anterior
    let isCollapsed =
        localStorage.getItem("sidebar-collapsed") === "true";

    function updateSidebar() {

        // Modificar anchura
        sidebar.classList.toggle("w-64", !isCollapsed);
        sidebar.classList.toggle("w-20", isCollapsed);

        // Mostrar u ocultar textos suavemente
        labels.forEach(label => {
            label.classList.toggle("opacity-0", isCollapsed);
            label.classList.toggle("opacity-100", !isCollapsed);
            label.classList.toggle("pointer-events-none", isCollapsed);
        });

        // Actualizar accesibilidad
        toggleButton.setAttribute(
            "aria-expanded",
            String(!isCollapsed)
        );

        toggleButton.setAttribute(
            "aria-label",
            isCollapsed
                ? "Expandir menú lateral"
                : "Contraer menú lateral"
        );

        headings.forEach(heading => {
            heading.classList.toggle("invisible", isCollapsed);
        });
    }

    // Aplicar estado inicial
    updateSidebar();

    // Escuchar clic
    toggleButton.addEventListener("click", () => {

        isCollapsed = !isCollapsed;

        updateSidebar();

        // Recordar preferencia
        localStorage.setItem(
            "sidebar-collapsed",
            String(isCollapsed)
        );

    });

});
