
document.addEventListener("DOMContentLoaded", () => {

    function setupTransactionModal(type) {
        const form = document.getElementById(`${type}-create-form`);
        const accountName = document.getElementById(`${type}-account-name`);

        if (!form || !accountName) return;

        document.querySelectorAll(`[data-${type}-url]`).forEach(button => {
            button.addEventListener("click", () => {

                // Configurar la cuenta seleccionada
                form.dataset.apiUrl = button.dataset[`${type}Url`];
                accountName.textContent = button.dataset.accountName;

                // Limpiar el formulario
                form.reset();

                // Limpiar errores anteriores
                form.querySelectorAll('[id$="-error"]').forEach(error => {
                    error.textContent = "";
                    error.classList.add("hidden");
                });

            });
        });
    }

    setupTransactionModal("payment");
    setupTransactionModal("charge");

});
