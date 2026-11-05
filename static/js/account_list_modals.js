document.addEventListener("DOMContentLoaded", () => {

    const paymentForm = document.getElementById("payment-create-form");
    const paymentAccountName = document.getElementById("payment-account-name");

    if (!paymentForm || !paymentAccountName) return;

    document.querySelectorAll("[data-payment-url]").forEach(button => {

        button.addEventListener("click", () => {

            // URL de la cuenta seleccionada
            paymentForm.dataset.apiUrl = button.dataset.paymentUrl;

            // Nombre visible en el modal
            paymentAccountName.textContent = button.dataset.accountName;

            // Limpiar valores de una apertura anterior
            paymentForm.reset();

            // Limpiar posibles errores generales
            const generalError = document.getElementById("payment-form-error");

            if (generalError) {
                generalError.textContent = "";
                generalError.classList.add("hidden");
            }

            // Limpiar errores individuales de los campos
            paymentForm.querySelectorAll('[id$="-error"]').forEach(error => {
                error.textContent = "";
                error.classList.add("hidden");
            });

        });

    });

});