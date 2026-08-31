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

});