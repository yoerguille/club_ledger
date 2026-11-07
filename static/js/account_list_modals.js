
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
    setupAccountEditModal();
    setupAccountEditSubmit();

});


function setupAccountEditModal() {
    const form = document.getElementById("account-edit-form");
    const nameInput = form.elements.namedItem("name");

    if (!form || !nameInput) return;

    const editButtons = document.querySelectorAll("[data-edit-url]");

    editButtons.forEach(button => {
        button.addEventListener("click", () => {

            // 1. Obtener los datos de la cuenta seleccionada
            const url = button.dataset.editUrl;
            const name = button.dataset.accountName;

            // 2. Configurar el formulario
            form.dataset.apiUrl = url;
            nameInput.value = name;

            // 3. Limpiar errores anteriores
            clearFormErrors(form);
        });
    });
}


function setupAccountEditSubmit() {
    const form = document.getElementById("account-edit-form");

    if (!form) return;

    form.addEventListener("submit", async (event) => {
        // Evita el envío tradicional del formulario
        event.preventDefault();

        clearFormErrors(form);

        const url = form.dataset.apiUrl;
        if (!url) return;

        // Recoge los datos del formulario
        const formData = new FormData(form);

        try {
            // Envía la petición HTTP a Django
            const response = await fetch(url, {
                method: "POST",
                body: formData,
                credentials: "same-origin",
            });

            // Convierte la respuesta JSON en un objeto JavaScript
            const data = await response.json();

            if (!response.ok) {
                showFormErrors(form, data.errors);
                return;
            }

            // Actualización correcta
            const nameElement = [...document.querySelectorAll(
                "[data-account-name-display]"
            )].find(element =>
                element.dataset.accountNameDisplay === String(data.account.id)
            );

            if (nameElement) {
                nameElement.textContent = data.account.name;
            }

            document.querySelectorAll("[data-edit-url]").forEach(button => {
                if (button.dataset.editUrl === url) {
                    button.dataset.accountName = data.account.name;
                }
            });

            const modalElement = document.getElementById("account-edit-modal");
            const modal = FlowbiteInstances.getInstance("Modal", "account-edit-modal");

            if (modal) {
                modal.hide();
            }

        } catch (error) {
            showFormErrors(form, {
                "__all__": [
                    { "message": "No se pudo conectar con el servidor." }
                ]
            });
        }
    });
}



function clearFormErrors(form) {

    // Limpiar errores de cada campo
    form.querySelectorAll('[id$="-error"]').forEach(element => {
        element.textContent = "";
        element.classList.add("hidden");
    });

    // Limpiar errores generales
    const generalErrors = form.querySelector("[data-form-errors]");

    if (generalErrors) {
        generalErrors.textContent = "";
        generalErrors.classList.add("hidden");
    }
}




function showFormErrors(form, errors = {}) {
    const generalErrors = form.querySelector("[data-form-errors]");

    for (const [field, messages] of Object.entries(errors)) {

        // Buscar el elemento donde mostrar el error
        const fieldError = form.querySelector(
            `[id="${field}-error"]`
        );

        // Si no existe, utilizar el contenedor de errores generales
        const target = fieldError || generalErrors;

        if (!target) continue;

        target.textContent = messages
            .map(error =>
                typeof error === "string" ? error : error.message
            )
            .join("\n");

        target.classList.remove("hidden");
    }
}