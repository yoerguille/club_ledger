document.addEventListener("DOMContentLoaded", () => {

    const customerFilters = document.getElementById("customer-filters");

    if (!customerFilters) {
        return;
    }

    const selects = customerFilters.querySelectorAll("select");

    selects.forEach((select) => {
        select.addEventListener("change", () => {
            customerFilters.submit();
        });
    });

});