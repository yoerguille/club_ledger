
    document.addEventListener("DOMContentLoaded", () => {
        console.log("Script de nueva cuenta cargado");

        const form = document.getElementById("new-account-form");
        console.log("Formulario encontrado:", form);

        if (!form) return;

        const submitButton = document.getElementById("new-account-submit-btn");
        const errorContainer = document.getElementById("new-account-form-error");

        form.addEventListener("submit", async (event) => {
            event.preventDefault();

            console.log("Formulario enviado");

            errorContainer.classList.add("hidden");
            errorContainer.textContent = "";

            submitButton.disabled = true;
            submitButton.textContent = "Guardando...";

            const formData = new FormData(form);

            const accountData = {
                name: formData.get("name"),
                season: formData.get("season"),
                notes: formData.get("notes"),
            };

            try {
                const response = await fetch(form.dataset.apiUrl, {
                    method: "POST",
                    credentials: "same-origin",
                    headers: {
                        "Content-Type": "application/json",
                        "Accept": "application/json",
                        "X-CSRFToken": formData.get("csrfmiddlewaretoken"),
                    },
                    body: JSON.stringify(accountData),
                });

                const result = await response.json();

                if (!response.ok) {
                    const messages = [];

                    for (const [field, errors] of Object.entries(result)) {
                        const details = Array.isArray(errors)
                            ? errors.join(", ")
                            : String(errors);

                        messages.push(`${field}: ${details}`);
                    }

                    throw new Error(
                        messages.join("\n") ||
                        "No se ha podido crear la cuenta."
                    );
                }

                if (response.status !== 201) {
                    throw new Error("Respuesta inesperada del servidor.");
                }

                window.location.reload();

            } catch (error) {
                errorContainer.textContent = error.message;
                errorContainer.classList.remove("hidden");

            } finally {
                submitButton.disabled = false;
                submitButton.textContent = "Crear Cuenta";
            }
        });
    });
