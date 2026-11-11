
document.addEventListener("DOMContentLoaded", () => {

    const sidebar = document.getElementById("sidebar-container");
    const toggleButton = document.getElementById("sidebar-toggle");

    if (!sidebar || !toggleButton) return;

    // Recuperar preferencia del usuario
    let isHidden = localStorage.getItem("sidebar-hidden") === "true";

    function updateSidebar() {

        // Mostrar u ocultar el sidebar
        sidebar.classList.toggle("hidden", isHidden);

        // Actualizar accesibilidad
        toggleButton.setAttribute(
            "aria-expanded",
            String(!isHidden)
        );

        toggleButton.setAttribute(
            "aria-label",
            isHidden ? "Mostrar menú lateral" : "Ocultar menú lateral"
        );
    }

    // Aplicar estado inicial
    updateSidebar();

    // Escuchar clics del botón
    toggleButton.addEventListener("click", () => {

        isHidden = !isHidden;

        updateSidebar();

        // Guardar preferencia
        localStorage.setItem("sidebar-hidden", String(isHidden));

    });

});
