document.addEventListener("DOMContentLoaded", () => {

    const filters = [
        "customer-filters",
        "account-filters",
    ];

    filters.forEach((filterId) => {

        const form = document.getElementById(filterId);

        if (!form) {
            return;
        }

        const selects = form.querySelectorAll("select");

        selects.forEach((select) => {

            select.addEventListener("change", () => {
                form.submit();
            });

        });

    });



    /*
     * =========================
     * CAMBIO DE TEMA
     * =========================
     */

    const themeToggle = document.getElementById("theme-toggle");
    const themeIcon = document.getElementById("theme-toggle-icon");

    if (themeToggle && themeIcon) {

        const updateThemeIcon = () => {

            if (document.documentElement.classList.contains("dark")) {
                themeIcon.textContent = "☀";
            } else {
                themeIcon.textContent = "☾";
            }

        };


        themeToggle.addEventListener("click", () => {

            const isDark =
                document.documentElement.classList.toggle("dark");

            localStorage.setItem(
                "theme",
                isDark ? "dark" : "light"
            );

            updateThemeIcon();

        });


        updateThemeIcon();

    }

});



